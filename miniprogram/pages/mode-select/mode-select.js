const { ensureOk } = require("../../services/api-client");
const { getModes } = require("../../services/match-service");

Page({
  data: {
    modes: ensureOk(getModes()),
    selectedModeId: "race5",
    matchId: ""
  },

  onLoad(options) {
    this.setData({
      matchId: options.matchId ? decodeURIComponent(options.matchId) : ""
    });
  },

  handleModeSelect(event) {
    this.setData({ selectedModeId: event.detail.modeId });
  },

  next() {
    const selectedMode = this.data.modes.find((mode) => mode.modeId === this.data.selectedModeId);

    if (!selectedMode || !selectedMode.enabled) {
      wx.showToast({
        title: "该玩法暂未开放",
        icon: "none"
      });
      return;
    }

    const query = [
      `modeId=${this.data.selectedModeId}`,
      `matchId=${encodeURIComponent(this.data.matchId)}`
    ].join("&");

    wx.navigateTo({ url: `/pages/points-select/points-select?${query}` });
  }
});
