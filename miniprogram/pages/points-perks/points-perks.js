const { ensureOk } = require("../../services/api-client");
const { getPointsPerks } = require("../../services/player-service");

Page({
  data: {
    match: null,
    pointsPerks: null,
    loading: true,
    errorText: ""
  },

  onLoad() {
    this.loadPerks();
  },

  async loadPerks() {
    this.setData({
      loading: true,
      errorText: ""
    });

    try {
      const perks = ensureOk(await getPointsPerks());

      this.setData({
        match: perks.match,
        pointsPerks: perks.pointsPerks,
        loading: false
      });
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "积分礼遇读取失败，请稍后重试"
      });
    }
  },

  retryLoad() {
    this.loadPerks();
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
