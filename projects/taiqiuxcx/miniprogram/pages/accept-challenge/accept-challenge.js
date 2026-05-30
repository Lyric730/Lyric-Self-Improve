const { ensureOk } = require("../../services/api-client");
const { getIncomingChallenge } = require("../../services/player-service");

Page({
  data: {
    incomingChallenge: ensureOk(getIncomingChallenge())
  },

  accept() {
    wx.navigateTo({ url: "/pages/mode-select/mode-select" });
  },

  reject() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  }
});
