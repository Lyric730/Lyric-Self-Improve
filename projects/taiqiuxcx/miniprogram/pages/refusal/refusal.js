const { ensureOk } = require("../../services/api-client");
const { calculateSettlement, getCurrentMatch } = require("../../services/match-service");

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    settlement: ensureOk(calculateSettlement())
  },

  onLoad(options) {
    this.setData({
      settlement: ensureOk(calculateSettlement({
        ...options,
        elapsedText: options.elapsedText ? decodeURIComponent(options.elapsedText) : ""
      }))
    });
  },

  exitMatch() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  rematch() {
    wx.navigateTo({ url: "/pages/mode-select/mode-select" });
  }
});
