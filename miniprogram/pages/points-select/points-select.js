const { ensureOk } = require("../../services/api-client");
const { getConfigurableMatchSetup } = require("../../services/match-service");

Page({
  data: {
    mode: {
      modeId: "",
      name: "",
      targetWins: 0,
      minimumMinutes: 0,
      baseOptions: [],
      multipliers: [],
      normalReward: "",
      sprintReward: ""
    },
    selectedBase: 0,
    selectedMultiplier: 1,
    riskPoints: 0,
    matchId: "",
    loading: true,
    errorText: ""
  },

  onLoad(options) {
    this.routeOptions = {
      matchId: options.matchId ? decodeURIComponent(options.matchId) : "",
      modeId: options.modeId || ""
    };

    this.setData({
      matchId: this.routeOptions.matchId
    });
    this.loadSetup();
  },

  async loadSetup() {
    this.setData({
      loading: true,
      errorText: ""
    });

    try {
      const setup = ensureOk(await getConfigurableMatchSetup(this.routeOptions));

      this.setData({
        ...setup,
        loading: false
      });
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "底分倍率读取失败，请稍后重试"
      });
    }
  },

  retryLoad() {
    this.loadSetup();
  },

  chooseBase(event) {
    this.setData({ selectedBase: Number(event.currentTarget.dataset.value) }, () => this.refreshRisk());
  },

  chooseMultiplier(event) {
    this.setData({ selectedMultiplier: Number(event.currentTarget.dataset.value) }, () => this.refreshRisk());
  },

  refreshRisk() {
    this.setData({
      riskPoints: this.data.selectedBase * this.data.selectedMultiplier
    });
  },

  next() {
    const { mode, selectedBase, selectedMultiplier, riskPoints } = this.data;

    if (!mode.modeId || !selectedBase || !selectedMultiplier) {
      wx.showToast({
        title: "请先确认底分和倍率",
        icon: "none"
      });
      return;
    }

    const query = [
      `matchId=${encodeURIComponent(this.data.matchId)}`,
      `modeId=${mode.modeId}`,
      `base=${selectedBase}`,
      `multiplier=${selectedMultiplier}`,
      `risk=${riskPoints}`
    ].join("&");

    wx.navigateTo({
      url: `/pages/match-confirm/match-confirm?${query}`
    });
  }
});
