const { ensureOk } = require("../../services/api-client");
const { getIncomingChallenge } = require("../../services/player-service");
const { getWaitingRoomState, joinChallengeRoom } = require("../../services/match-service");

function buildInviteFromRoom(roomState, fallbackInvite) {
  const fallback = fallbackInvite || {};

  return {
    roomNo: roomState.roomNo || fallback.roomNo || "",
    tableNo: roomState.tableNo || fallback.tableNo || "",
    dueTime: roomState.dueTime || fallback.dueTime || "",
    statusText: roomState.statusText || fallback.statusText || "待确认",
    host: roomState.host || fallback.host,
    challenger: roomState.guest || fallback.challenger,
    acceptHint: fallback.acceptHint || "接受后进入玩法选择。",
    rejectHint: fallback.rejectHint || "拒绝后回到挑战首页。"
  };
}

Page({
  data: {
    matchId: "",
    incomingChallenge: null,
    inviteError: "",
    loadingInvite: true,
    joining: false
  },

  async onLoad(options) {
    const matchId = options.matchId ? decodeURIComponent(options.matchId) : "";

    this.setData({ matchId });
    await this.loadInvite();
  },

  async loadInvite() {
    this.setData({
      inviteError: "",
      loadingInvite: true
    });

    try {
      const fallbackInvite = ensureOk(getIncomingChallenge());

      if (!this.data.matchId) {
        this.setData({ incomingChallenge: fallbackInvite });
        return;
      }

      const roomState = ensureOk(await getWaitingRoomState({
        matchId: this.data.matchId
      }));

      this.setData({
        incomingChallenge: buildInviteFromRoom(roomState, fallbackInvite)
      });
    } catch (error) {
      this.setData({
        inviteError: error.message || "邀请读取失败"
      });

      wx.showToast({
        title: error.message || "邀请读取失败",
        icon: "none"
      });
    } finally {
      this.setData({ loadingInvite: false });
    }
  },

  async accept() {
    if (this.data.joining) {
      return;
    }

    this.setData({ joining: true });

    try {
      const result = ensureOk(await joinChallengeRoom({
        matchId: this.data.matchId
      }));
      const matchId = result.matchId || this.data.matchId;
      const query = matchId ? `?matchId=${encodeURIComponent(matchId)}` : "";

      wx.navigateTo({ url: `/pages/mode-select/mode-select${query}` });
    } catch (error) {
      wx.showToast({
        title: error.message || "加入失败",
        icon: "none"
      });
    } finally {
      this.setData({ joining: false });
    }
  },

  reject() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  }
});
