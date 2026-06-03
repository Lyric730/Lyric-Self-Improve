const { ensureOk } = require("../../services/api-client");
const { getAvailableModes } = require("../../services/match-service");

function firstEnabledMode(modes = []) {
  return modes.find((mode) => mode.enabled !== false) || modes[0] || null;
}

Page({
  data: {
    modes: [],
    selectedModeId: "",
    matchId: "",
    loading: true,
    errorText: ""
  },

  onLoad(options) {
    this.routeOptions = {
      matchId: options.matchId ? decodeURIComponent(options.matchId) : ""
    };

    this.setData({
      matchId: this.routeOptions.matchId
    });
    this.loadModes();
  },

  async loadModes() {
    this.setData({
      loading: true,
      errorText: ""
    });

    try {
      const modes = ensureOk(await getAvailableModes());
      const selectedMode = modes.find((mode) => mode.modeId === this.data.selectedModeId) || firstEnabledMode(modes);

      this.setData({
        modes,
        selectedModeId: selectedMode ? selectedMode.modeId : "",
        loading: false
      });
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "玩法配置读取失败，请稍后重试"
      });
    }
  },

  retryLoad() {
    this.loadModes();
  },

  handleModeSelect(event) {
    this.setData({ selectedModeId: event.detail.modeId });
  },

  next() {
    const selectedMode = this.data.modes.find((mode) => mode.modeId === this.data.selectedModeId);

    if (!selectedMode) {
      wx.showToast({
        title: "请选择玩法",
        icon: "none"
      });
      return;
    }

    if (!selectedMode.enabled) {
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
