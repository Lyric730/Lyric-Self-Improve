const { ensureOk } = require("../../services/api-client");
const { getPlayerProfile } = require("../../services/player-service");

const profile = ensureOk(getPlayerProfile());

Page({
  data: {
    match: profile.match,
    playerStats: profile.playerStats
  },

  goHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  goRankings() {
    wx.navigateTo({ url: "/pages/rankings/rankings" });
  },

  goPerks() {
    wx.navigateTo({ url: "/pages/points-perks/points-perks" });
  }
});
