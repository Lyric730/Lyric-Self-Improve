const { ensureOk } = require("../../services/api-client");
const { getRankingTabs } = require("../../services/player-service");

const tabs = ensureOk(getRankingTabs());

Page({
  data: {
    tabs,
    activeTab: "store",
    activeRows: tabs[0].rows
  },

  switchTab(event) {
    const activeTab = event.currentTarget.dataset.tab;
    const active = tabs.find((item) => item.id === activeTab) || tabs[0];

    this.setData({
      activeTab: active.id,
      activeRows: active.rows
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
