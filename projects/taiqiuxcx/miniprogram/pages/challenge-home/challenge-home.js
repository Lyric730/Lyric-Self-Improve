const { ensureOk } = require("../../services/api-client");
const { getChallengeHome } = require("../../services/player-service");

const initialHome = ensureOk(getChallengeHome());

Page({
  data: {
    match: initialHome.match,
    challengeGate: initialHome.challengeGate,
    canStartChallenge: false,
    gateMessage: "",
    playableStatusText: "排位可用"
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

  goWaitingRoom() {
    if (!this.data.canStartChallenge) {
      wx.showToast({
        title: this.data.gateMessage || "暂不能开始",
        icon: "none"
      });
      return;
    }

    wx.navigateTo({ url: "/pages/waiting-room/waiting-room" });
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
