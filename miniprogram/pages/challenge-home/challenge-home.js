const { ensureOk } = require("../../services/api-client");
const { createChallengeRoom } = require("../../services/match-service");
const { getChallengeHome } = require("../../services/player-service");

const DEFAULT_TABLE_SESSION = {
  clubName: "云瀚台球俱乐部",
  tableNo: "读取中",
  dueTime: "--:--",
  openedAt: "读取中"
};

Page({
  data: {
    match: {
      playerA: {
        shortName: "我",
        name: "当前会员",
        rankTitle: "当前段位",
        points: 0
      }
    },
    challengeGate: {
      tableSession: DEFAULT_TABLE_SESSION,
      requiredChecks: [],
      unavailableMessage: ""
    },
    loading: true,
    errorText: "",
    canStartChallenge: false,
    gateMessage: "",
    playableStatusText: "读取中",
    startingChallenge: false
  },

  onLoad(options = {}) {
    this.routeOptions = {
      tableId: options.tableId || options.tableNo || "",
      tableNo: options.tableNo || options.tableId || ""
    };
    this.loadHome();
  },

  async loadHome() {
    this.setData({
      loading: true,
      errorText: "",
      canStartChallenge: false,
      playableStatusText: "读取中"
    });

    try {
      const home = ensureOk(await getChallengeHome(this.routeOptions || {}));

      this.setData({
        match: home.match,
        challengeGate: home.challengeGate,
        loading: false
      });
      this.evaluateChallengeGate();
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "开局状态读取失败，请稍后重试",
        playableStatusText: "暂不可用"
      });
    }
  },

  retryLoad() {
    this.loadHome();
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
