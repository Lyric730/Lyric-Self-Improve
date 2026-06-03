const { ensureOk } = require("../../services/api-client");
const { calculateSettlement, getCurrentMatch, getSettlementResult } = require("../../services/match-service");

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    settlement: ensureOk(calculateSettlement()),
    loadingSettlement: false
  },

  async onLoad(options) {
    const params = {
      ...options,
      elapsedText: options.elapsedText ? decodeURIComponent(options.elapsedText) : ""
    };
    const previewSettlement = ensureOk(calculateSettlement(params));

    this.setData({
      settlement: previewSettlement,
      loadingSettlement: true
    });

    try {
      const settlement = ensureOk(await getSettlementResult(params));

      this.setData({ settlement });
    } catch (error) {
      wx.showToast({
        title: error.message || "结算记录读取失败",
        icon: "none"
      });
    } finally {
      this.setData({ loadingSettlement: false });
    }
  },

  goHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  replay() {
    wx.navigateTo({ url: "/pages/mode-select/mode-select" });
  }
});
