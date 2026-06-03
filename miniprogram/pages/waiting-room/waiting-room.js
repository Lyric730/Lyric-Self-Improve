const { ensureOk } = require("../../services/api-client");
const { getWaitingRoom } = require("../../services/player-service");

Page({
  data: {
    roomState: ensureOk(getWaitingRoom())
  },

  refreshRoom() {
    if (this.data.roomState.opponentJoined) {
      wx.showToast({
        title: "房间状态已更新",
        icon: "none"
      });
      return;
    }

    this.setData({
      "roomState.opponentJoined": true,
      "roomState.statusText": "对手已加入",
      "roomState.statusHint": "双方确认后进入玩法选择"
    });

    wx.showToast({
      title: "对手已加入",
      icon: "none"
    });
  },

  cancelRoom() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  continueMatch() {
    if (!this.data.roomState.opponentJoined) {
      return;
    }

    wx.navigateTo({ url: "/pages/mode-select/mode-select" });
  }
});
