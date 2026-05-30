const { requireRole } = require("../../utils/access-control");
const { ensureOk } = require("../../services/api-client");
const {
  deductMemberPoints,
  getMemberForExchange,
  getStaffDeskData,
  updateTableDueTime,
  voidAbnormalMatch
} = require("../../services/staff-service");

const initialDeskData = ensureOk(getStaffDeskData());

function scanCode() {
  return new Promise((resolve, reject) => {
    wx.scanCode({
      scanType: ["qrCode"],
      success: resolve,
      fail: reject
    });
  });
}

function parseMemberOpenid(rawValue) {
  const raw = String(rawValue || "").trim();

  if (!raw) {
    return "";
  }

  try {
    const parsed = JSON.parse(raw);

    if (parsed.openid) return parsed.openid;
    if (parsed.openId) return parsed.openId;
  } catch (error) {
    // Non-JSON QR content is handled below.
  }

  const queryMatch = raw.match(/[?&](openid|openId)=([^&]+)/);
  if (queryMatch) return decodeURIComponent(queryMatch[2]);

  const labelMatch = raw.match(/(?:openid|openId):([^\s;]+)/);
  if (labelMatch) return labelMatch[1];

  return raw;
}

Page({
  data: {
    accessReady: false,
    staffTables: initialDeskData.staffTables,
    timeOptions: ["21:30", "22:00", "22:30", "23:00"],
    selectedTableId: initialDeskData.staffTables[0].id,
    selectedTime: initialDeskData.staffTables[0].dueTime,
    selectedTable: initialDeskData.staffTables[0],
    selectedMember: null,
    selectedMemberText: "扫码选择会员后核销",
    deductOptions: [100, 200, 500],
    selectedDeduct: 100,
    abnormalMatches: initialDeskData.abnormalMatches,
    savingDue: false,
    scanningMember: false,
    deducting: false,
    voiding: false
  },

  onLoad() {
    const accessReady = requireRole(["staff", "owner"]);

    this.setData({ accessReady });
  },

  chooseTable(event) {
    const selectedTableId = event.currentTarget.dataset.id;
    const selectedTable = this.data.staffTables.find((item) => item.id === selectedTableId) || this.data.staffTables[0];

    this.setData({
      selectedTableId,
      selectedTable,
      selectedTime: selectedTable.dueTime
    });
  },

  chooseTime(event) {
    this.setData({ selectedTime: event.currentTarget.dataset.time });
  },

  chooseDeduct(event) {
    this.setData({ selectedDeduct: Number(event.currentTarget.dataset.value) });
  },

  async scanMember() {
    if (!this.data.accessReady || this.data.scanningMember) {
      return;
    }

    this.setData({ scanningMember: true });

    try {
      const scanResult = await scanCode();
      const openid = parseMemberOpenid(scanResult.result);

      if (!openid) {
        wx.showToast({ title: "未识别到会员", icon: "none" });
        return;
      }

      const member = ensureOk(await getMemberForExchange({ openid }));

      this.setData({
        selectedMember: member,
        selectedMemberText: `${member.name} · ${member.points} 积分`
      });

      wx.showToast({ title: "已选择会员", icon: "success" });
    } catch (error) {
      const isCancel = error && error.errMsg && error.errMsg.includes("cancel");
      wx.showToast({ title: isCancel ? "未选择会员" : error.message || "识别失败", icon: "none" });
    } finally {
      this.setData({ scanningMember: false });
    }
  },

  async saveDueTime() {
    if (!this.data.accessReady || this.data.savingDue) {
      return;
    }

    this.setData({ savingDue: true });

    try {
      const result = ensureOk(await updateTableDueTime({
        tables: this.data.staffTables,
        tableId: this.data.selectedTableId,
        dueTime: this.data.selectedTime
      }));

      this.setData({
        staffTables: result.staffTables,
        selectedTable: result.selectedTable
      });

      wx.showToast({ title: "到点时间已更新", icon: "success" });
    } catch (error) {
      wx.showToast({ title: error.message || "保存失败", icon: "none" });
    } finally {
      this.setData({ savingDue: false });
    }
  },

  async confirmDeduct() {
    if (!this.data.accessReady || this.data.deducting) {
      return;
    }

    if (!this.data.selectedMember) {
      wx.showToast({ title: "请先选择会员", icon: "none" });
      return;
    }

    this.setData({ deducting: true });

    try {
      ensureOk(await deductMemberPoints({
        openid: this.data.selectedMember.openid,
        userName: this.data.selectedMember.name,
        points: this.data.selectedDeduct
      }));

      wx.showToast({ title: "积分已核销", icon: "success" });
    } catch (error) {
      wx.showToast({ title: error.message || "核销失败", icon: "none" });
    } finally {
      this.setData({ deducting: false });
    }
  },

  async voidMatch() {
    if (!this.data.accessReady || this.data.voiding) {
      return;
    }

    const targetMatch = this.data.abnormalMatches[0];

    this.setData({ voiding: true });

    try {
      ensureOk(await voidAbnormalMatch({
        matchId: targetMatch ? targetMatch.id : "",
        tableNo: targetMatch ? targetMatch.tableNo : ""
      }));

      wx.showToast({ title: "已提交作废", icon: "success" });
    } catch (error) {
      wx.showToast({ title: error.message || "提交失败", icon: "none" });
    } finally {
      this.setData({ voiding: false });
    }
  }
});
