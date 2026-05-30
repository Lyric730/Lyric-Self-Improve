const { ensureOk } = require("../../services/api-client");
const { getWaitingRoom } = require("../../services/player-service");

Page({
  data: {
    roomState: ensureOk(getWaitingRoom())
  },

  refreshRoom() {
    wx.showToast({
      title: "暂无新玩家加入",
      icon: "none"
    });
  },

  cancelRoom() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  }
});
