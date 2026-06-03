const { ensureOk } = require("../../services/api-client");
const { createChallengeRoom } = require("../../services/match-service");
const { getChallengeHome } = require("../../services/player-service");

const initialHome = ensureOk(getChallengeHome());

Page({
  data: {
    match: initialHome.match,
    challengeGate: initialHome.challengeGate,
    canStartChallenge: false,
    gateMessage: "",
    playableStatusText: "排位可用",
    startingChallenge: false
  },

  onLoad() {
    this.evaluateChallengeGate();
  },

  evaluateChallengeGate() {
    const checks = this.data.challengeGate.requiredChecks || [];
    const blockedCheck = checks.find((item) => !item.ready);
    const canStartChallenge = checks.length > 0 && !blockedCheck;

    this.setData({
      canStartChallenge,
      playableStatusText: canStartChallenge ? "排位可用" : "暂不可用",
      gateMessage: canStartChallenge
        ? ""
        : blockedCheck
          ? blockedCheck.userMessage
          : this.data.challengeGate.unavailableMessage
    });
  },

  async goWaitingRoom() {
    if (!this.data.canStartChallenge) {
      wx.showToast({
        title: this.data.gateMessage || "暂时不能开始",
        icon: "none"
      });
      return;
    }

    if (this.data.startingChallenge) {
      return;
    }

    this.setData({ startingChallenge: true });

    try {
      const tableSession = this.data.challengeGate.tableSession || {};
      const result = ensureOk(await createChallengeRoom({
        tableNo: tableSession.tableNo,
        dueTime: tableSession.dueTime,
        openedAt: tableSession.openedAt
      }));
      const matchId = result.matchId || (result.roomState && result.roomState.matchId) || "";

      wx.navigateTo({
        url: `/pages/waiting-room/waiting-room?matchId=${encodeURIComponent(matchId)}`
      });
    } catch (error) {
      wx.showToast({
        title: error.message || "发起挑战失败",
        icon: "none"
      });
    } finally {
      this.setData({ startingChallenge: false });
    }
  },

  goData() {
    wx.navigateTo({ url: "/pages/my-data/my-data" });
  },

  goRankings() {
    wx.navigateTo({ url: "/pages/rankings/rankings" });
  },

  goPerks() {
    wx.navigateTo({ url: "/pages/points-perks/points-perks" });
  }
});
