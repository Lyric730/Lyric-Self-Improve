const { ensureOk } = require("../../services/api-client");
const { configureMatchSetup, getCurrentMatch, getMatchSetup } = require("../../services/match-service");

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    setup: ensureOk(getMatchSetup()),
    matchId: "",
    configuring: false
  },

  onLoad(options) {
    this.setData({
      setup: ensureOk(getMatchSetup(options)),
      matchId: options.matchId ? decodeURIComponent(options.matchId) : ""
    });
  },

  async startMatch() {
    if (this.data.configuring) {
      return;
    }

    const { mode, selectedBase, selectedMultiplier, riskPoints } = this.data.setup;

    this.setData({ configuring: true });

    try {
      const result = ensureOk(await configureMatchSetup({
        matchId: this.data.matchId,
        modeId: mode.modeId,
        selectedBase,
        selectedMultiplier
      }));
      const matchId = result.matchId || this.data.matchId;

      const query = [
        `matchId=${encodeURIComponent(matchId)}`,
        `modeId=${mode.modeId}`,
        `base=${selectedBase}`,
        `multiplier=${selectedMultiplier}`,
        `risk=${riskPoints}`
      ].join("&");

      wx.navigateTo({
        url: `/pages/match-scoring/match-scoring?${query}`
      });
    } catch (error) {
      wx.showToast({
        title: error.message || "参数保存失败",
        icon: "none"
      });
    } finally {
      this.setData({ configuring: false });
    }
  }
});
