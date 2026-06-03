const { ensureOk } = require("../../services/api-client");
const { getRankingTabs } = require("../../services/player-service");

Page({
  data: {
    tabs: [],
    activeTab: "store",
    activeRows: [],
    activeRowsEmpty: true,
    loading: true,
    errorText: ""
  },

  onLoad() {
    this.loadRankings();
  },

  async loadRankings() {
    this.setData({
      loading: true,
      errorText: ""
    });

    try {
      const tabs = ensureOk(await getRankingTabs());
      const active = tabs[0] || { id: "store", rows: [] };

      this.setData({
        tabs,
        activeTab: active.id,
        activeRows: active.rows,
        activeRowsEmpty: !active.rows || active.rows.length === 0,
        loading: false
      });
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "排行榜读取失败，请稍后重试"
      });
    }
  },

  retryLoad() {
    this.loadRankings();
  },

  switchTab(event) {
    const activeTab = event.currentTarget.dataset.tab;
    const active = this.data.tabs.find((item) => item.id === activeTab) || this.data.tabs[0] || { id: "store", rows: [] };

    this.setData({
      activeTab: active.id,
      activeRows: active.rows,
      activeRowsEmpty: !active.rows || active.rows.length === 0
    });
  },

  goHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  goData() {
    wx.navigateTo({ url: "/pages/my-data/my-data" });
  },

  goPerks() {
    wx.navigateTo({ url: "/pages/points-perks/points-perks" });
  }
});
