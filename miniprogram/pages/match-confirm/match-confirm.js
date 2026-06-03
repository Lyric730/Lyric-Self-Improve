const { ensureOk } = require("../../services/api-client");
const { getCurrentMatch, getMatchSetup } = require("../../services/match-service");

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    setup: ensureOk(getMatchSetup()),
    matchId: ""
  },

  onLoad(options) {
    this.setData({
      setup: ensureOk(getMatchSetup(options)),
      matchId: options.matchId ? decodeURIComponent(options.matchId) : ""
    });
  },

  startMatch() {
    const { mode, selectedBase, selectedMultiplier, riskPoints } = this.data.setup;
    const query = [
      `matchId=${encodeURIComponent(this.data.matchId)}`,
      `modeId=${mode.modeId}`,
      `base=${selectedBase}`,
      `multiplier=${selectedMultiplier}`,
      `risk=${riskPoints}`
    ].join("&");

    wx.navigateTo({
      url: `/pages/match-scoring/match-scoring?${query}`
    });
  }
});
