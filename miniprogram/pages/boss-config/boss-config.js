const { requireRole } = require("../../utils/access-control");
const { ensureOk } = require("../../services/api-client");
const {
  getAdminConfig,
  getMemberForRole,
  saveAdminConfig,
  setMemberRole
} = require("../../services/admin-service");
const { validateAdminConfig } = require("../../utils/admin-config-validator");
const { parseMemberOpenid } = require("../../utils/member-code-parser");

function cloneConfig(config) {
  return JSON.parse(JSON.stringify(config));
}

function parseNumberList(value) {
  return String(value || "")
    .match(/\d+/g)
    ? String(value || "").match(/\d+/g).map((item) => Number(item))
    : [];
}

function normalizeModeForEdit(mode) {
  const baseOptions = Array.isArray(mode.baseOptions) ? mode.baseOptions : parseNumberList(mode.baseText);
  const multipliers = Array.isArray(mode.multipliers) ? mode.multipliers : parseNumberList(mode.multiplierText);

  return {
    ...mode,
    baseOptions,
    multipliers,
    baseText: baseOptions.join(" / "),
    multiplierText: multipliers.map((item) => `x${item}`).join(" / ")
  };
}

function normalizeConfigForEdit(config) {
  const cloned = cloneConfig(config);

  return {
    ...cloned,
    modes: cloned.modes.map(normalizeModeForEdit)
  };
}

function normalizeConfigForSave(config) {
  const cloned = cloneConfig(config);

  return {
    ...cloned,
    modes: cloned.modes.map((mode) => ({
      ...mode,
      targetWins: Number(mode.targetWins),
      minimumMinutes: Number(mode.minimumMinutes),
      starReward: Number(mode.starReward),
      baseOptions: parseNumberList(mode.baseText).length > 0 ? parseNumberList(mode.baseText) : mode.baseOptions,
      multipliers: parseNumberList(mode.multiplierText).length > 0 ? parseNumberList(mode.multiplierText) : mode.multipliers
    })),
    points: {
      newUser: Number(cloned.points.newUser),
      checkIn: Number(cloned.points.checkIn),
      tableOpenBonus: Number(cloned.points.tableOpenBonus),
      exchangeThreshold: Number(cloned.points.exchangeThreshold)
    }
  };
}

function scanCode() {
  return new Promise((resolve, reject) => {
    wx.scanCode({
      scanType: ["qrCode"],
      success: resolve,
      fail: reject
    });
  });
}

Page({
  data: {
    accessReady: false,
    adminConfig: normalizeConfigForEdit(ensureOk(getAdminConfig())),
    saving: false,
    roleMember: null,
    roleMemberText: "扫码选择会员后设置员工或大屏权限",
    roleTarget: "staff",
    roleTargetLabel: "员工",
    roleTargetIndex: 0,
    roleOptions: [
      { role: "staff", label: "员工" },
      { role: "screen", label: "大屏" },
      { role: "player", label: "普通球友" }
    ],
    scanningRoleMember: false,
    savingRole: false
  },

  onLoad() {
    const accessReady = requireRole(["owner"]);

    this.setData({ accessReady });
  },

  toggleMode(event) {
    const index = event.currentTarget.dataset.index;
    const key = `adminConfig.modes[${index}].enabled`;

    this.setData({ [key]: event.detail.value });
  },

  changeModeField(event) {
    const { index, field } = event.currentTarget.dataset;
    const value = event.detail.value;
    const updates = {
      [`adminConfig.modes[${index}].${field}`]: value
    };

    if (field === "baseText") {
      updates[`adminConfig.modes[${index}].baseOptions`] = parseNumberList(value);
    }

    if (field === "multiplierText") {
      updates[`adminConfig.modes[${index}].multipliers`] = parseNumberList(value);
    }

    this.setData(updates);
  },

  changePointsField(event) {
    const key = event.currentTarget.dataset.key;

    this.setData({
      [`adminConfig.points.${key}`]: event.detail.value
    });
  },

  changeAntiCheatField(event) {
    const key = event.currentTarget.dataset.key;

    this.setData({
      [`adminConfig.antiCheat.${key}`]: event.detail.value
    });
  },

  changeScreenField(event) {
    const key = event.currentTarget.dataset.key;

    this.setData({
      [`adminConfig.screen.${key}`]: event.detail.value
    });
  },

  chooseRoleTarget(event) {
    const index = Number(event.detail.value || 0);
    const option = this.data.roleOptions[index] || this.data.roleOptions[0];

    this.setData({
      roleTarget: option.role,
      roleTargetLabel: option.label,
      roleTargetIndex: index
    });
  },

  async scanRoleMember() {
    if (!this.data.accessReady || this.data.scanningRoleMember) {
      return;
    }

    this.setData({ scanningRoleMember: true });

    try {
      const scanResult = await scanCode();
      const openid = parseMemberOpenid(scanResult.result);

      if (!openid) {
        wx.showToast({ title: "未识别到会员", icon: "none" });
        return;
      }

      const member = ensureOk(await getMemberForRole({ openid }));

      this.setData({
        roleMember: member,
        roleMemberText: `${member.name} · 当前身份 ${member.role}`
      });

      wx.showToast({ title: "已选择会员", icon: "none" });
    } catch (error) {
      const isCancel = error && error.errMsg && error.errMsg.includes("cancel");
      wx.showToast({ title: isCancel ? "未选择会员" : error.message || "识别失败", icon: "none" });
    } finally {
      this.setData({ scanningRoleMember: false });
    }
  },

  async saveMemberRole() {
    if (!this.data.accessReady || this.data.savingRole) {
      return;
    }

    if (!this.data.roleMember) {
      wx.showToast({ title: "请先扫码选择会员", icon: "none" });
      return;
    }

    this.setData({ savingRole: true });

    try {
      const member = ensureOk(await setMemberRole({
        openid: this.data.roleMember.openid,
        targetRole: this.data.roleTarget,
        name: this.data.roleMember.name
      }));

      this.setData({
        roleMember: member,
        roleMemberText: `${member.name} · 当前身份 ${member.role}`
      });

      wx.showToast({ title: "身份已更新", icon: "none" });
    } catch (error) {
      wx.showToast({ title: error.message || "更新失败", icon: "none" });
    } finally {
      this.setData({ savingRole: false });
    }
  },

  async saveConfig() {
    if (!this.data.accessReady || this.data.saving) {
      return;
    }

    const configToSave = normalizeConfigForSave(this.data.adminConfig);
    const validation = validateAdminConfig(configToSave);

    if (!validation.ok) {
      wx.showModal({
        title: "配置需要调整",
        content: validation.errors[0],
        showCancel: false,
        confirmText: "知道了"
      });
      return;
    }

    this.setData({ saving: true });

    try {
      ensureOk(await saveAdminConfig(configToSave));

      this.setData({
        adminConfig: normalizeConfigForEdit(configToSave)
      });

      wx.showToast({ title: "配置已保存", icon: "none" });
    } catch (error) {
      wx.showToast({ title: error.message || "保存失败", icon: "none" });
    } finally {
      this.setData({ saving: false });
    }
  }
});
