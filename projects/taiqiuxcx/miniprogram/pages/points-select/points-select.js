const { ensureOk } = require("../../services/api-client");
const { getMatchSetup } = require("../../services/match-service");

Page({
  data: {
    ...ensureOk(getMatchSetup())
  },

  onLoad(options) {
    const setup = ensureOk(getMatchSetup({ modeId: options.modeId }));
    this.setData(setup);
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
    wx.navigateTo({
      url: `/pages/match-confirm/match-confirm?modeId=${mode.modeId}&base=${selectedBase}&multiplier=${selectedMultiplier}&risk=${riskPoints}`
    });
  }
});
