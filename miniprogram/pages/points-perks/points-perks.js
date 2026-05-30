const { ensureOk } = require("../../services/api-client");
const { getPointsPerks } = require("../../services/player-service");

const perks = ensureOk(getPointsPerks());

Page({
  data: {
    match: perks.match,
    pointsPerks: perks.pointsPerks
  },

  goHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  goData() {
    wx.navigateTo({ url: "/pages/my-data/my-data" });
  },

  goRankings() {
    wx.navigateTo({ url: "/pages/rankings/rankings" });
  },

  goMemberCode() {
    wx.navigateTo({ url: "/pages/member-code/member-code" });
  }
});
