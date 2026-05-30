const { ensureOk } = require("../../services/api-client");
const { getCurrentMatch, getMatchSetup } = require("../../services/match-service");

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    setup: ensureOk(getMatchSetup())
  },

  onLoad(options) {
    this.setData({
      setup: ensureOk(getMatchSetup(options))
    });
  },

  startMatch() {
    const { mode, selectedBase, selectedMultiplier, riskPoints } = this.data.setup;
    wx.navigateTo({
      url: `/pages/match-scoring/match-scoring?modeId=${mode.modeId}&base=${selectedBase}&multiplier=${selectedMultiplier}&risk=${riskPoints}`
    });
  }
});
