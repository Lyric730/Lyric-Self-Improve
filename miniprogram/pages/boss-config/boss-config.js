const { requireRole } = require("../../utils/access-control");
const { ensureOk } = require("../../services/api-client");
const { getAdminConfig, saveAdminConfig } = require("../../services/admin-service");
const { validateAdminConfig } = require("../../utils/admin-config-validator");

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

Page({
  data: {
    accessReady: false,
    adminConfig: normalizeConfigForEdit(ensureOk(getAdminConfig())),
    saving: false
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
