const { ensureOk } = require("../../services/api-client");
const { getPlayerProfile } = require("../../services/player-service");

Page({
  data: {
    match: null,
    playerStats: null,
    loading: true,
    errorText: ""
  },

  onLoad() {
    this.loadProfile();
  },

  async loadProfile() {
    this.setData({
      loading: true,
      errorText: ""
    });

    try {
      const profile = ensureOk(await getPlayerProfile());

      this.setData({
        match: profile.match,
        playerStats: profile.playerStats,
        loading: false
      });
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "数据读取失败，请稍后重试"
      });
    }
  },

  retryLoad() {
    this.loadProfile();
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
