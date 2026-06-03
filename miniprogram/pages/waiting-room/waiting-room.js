const { ensureOk } = require("../../services/api-client");
const { getWaitingRoomState } = require("../../services/match-service");

Page({
  data: {
    matchId: "",
    roomState: null,
    loadingRoom: true
  },

  async onLoad(options) {
    const matchId = options.matchId ? decodeURIComponent(options.matchId) : "";

    this.setData({ matchId });
    await this.loadRoom();
  },

  async loadRoom() {
    this.setData({ loadingRoom: true });

    try {
      const roomState = ensureOk(await getWaitingRoomState({
        matchId: this.data.matchId
      }));

      this.setData({
        roomState,
        matchId: roomState.matchId || this.data.matchId
      });
    } catch (error) {
      wx.showToast({
        title: error.message || "房间读取失败",
        icon: "none"
      });
    } finally {
      this.setData({ loadingRoom: false });
    }
  },

  refreshRoom() {
    if (this.data.roomState && this.data.roomState.localPreview && !this.data.roomState.opponentJoined) {
      this.setData({
        "roomState.opponentJoined": true,
        "roomState.statusText": "对手已加入",
        "roomState.statusHint": "双方确认后进入玩法选择"
      });

      wx.showToast({
        title: "对手已加入",
        icon: "none"
      });
      return;
    }

    this.loadRoom();
  },

  cancelRoom() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  continueMatch() {
    if (!this.data.roomState || !this.data.roomState.opponentJoined) {
      return;
    }

    const query = this.data.matchId ? `?matchId=${encodeURIComponent(this.data.matchId)}` : "";

    wx.navigateTo({ url: `/pages/mode-select/mode-select${query}` });
  }
});
