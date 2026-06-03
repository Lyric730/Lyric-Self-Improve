const { ensureOk } = require("../../services/api-client");
const {
  getCurrentMatch,
  getMatchSetup,
  recordMatchScore,
  startConfiguredMatch
} = require("../../services/match-service");

function formatDuration(totalSeconds) {
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
}

function buildQuery(params = {}) {
  return Object.keys(params)
    .map((key) => {
      const value = params[key] === undefined || params[key] === null ? "" : params[key];

      return `${key}=${encodeURIComponent(value)}`;
    })
    .join("&");
}

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    setup: ensureOk(getMatchSetup()),
    scoreA: 0,
    scoreB: 0,
    elapsedSeconds: 1,
    elapsedText: "00:00:01",
    remainingText: "",
    timeReady: false,
    settlementLocked: false,
    matchId: "",
    starting: true,
    scoreUpdating: false,
    startError: ""
  },

  onLoad(options) {
    const setup = ensureOk(getMatchSetup(options));
    const initialElapsed = Math.max(1, Number(options.elapsed || 1));

    this.matchStartedAt = Date.now() - (initialElapsed - 1) * 1000;
    this.setData({
      setup,
      elapsedSeconds: initialElapsed,
      matchId: options.matchId ? decodeURIComponent(options.matchId) : ""
    }, () => {
      this.refreshTimeState();
      this.startRemoteMatch();
    });
  },

  onShow() {
    this.setData({ settlementLocked: false });

    if (!this.data.starting && !this.data.startError) {
      this.startTimer();
    }
  },

  onHide() {
    this.stopTimer();
  },

  onUnload() {
    this.stopTimer();
  },

  async startRemoteMatch() {
    this.stopTimer();
    this.setData({
      starting: true,
      startError: ""
    });

    try {
      const { setup } = this.data;
      const result = ensureOk(await startConfiguredMatch({
        matchId: this.data.matchId,
        modeId: setup.mode.modeId,
        selectedBase: setup.selectedBase,
        selectedMultiplier: setup.selectedMultiplier,
        targetWins: setup.mode.targetWins,
        minimumMinutes: setup.mode.minimumMinutes
      }));

      this.applyRemoteMatchState(result);
      this.setData({ starting: false }, () => this.startTimer());
    } catch (error) {
      this.stopTimer();
      this.setData({
        starting: false,
        startError: error.message || "比赛状态同步失败，请返回后重试"
      });
      wx.showToast({
        title: error.message || "比赛状态同步失败",
        icon: "none"
      });
    }
  },

  applyRemoteMatchState(result = {}) {
    if (result.roomState) {
      this.applyRoomState(result.roomState);
    }

    if (result.playState) {
      this.applyPlayState(result.playState);
    }
  },

  applyRoomState(roomState = {}) {
    this.setData({
      match: {
        ...this.data.match,
        id: roomState.matchId || this.data.match.id,
        matchId: roomState.matchId || this.data.match.matchId,
        roomNo: roomState.roomNo || this.data.match.roomNo,
        tableNo: roomState.tableNo || this.data.match.tableNo,
        dueTime: roomState.dueTime || this.data.match.dueTime,
        playerA: roomState.host || this.data.match.playerA,
        playerB: roomState.guest || this.data.match.playerB
      }
    });
  },

  applyPlayState(playState = {}) {
    const elapsedSeconds = Math.max(1, Number(playState.elapsedSeconds || this.data.elapsedSeconds || 1));

    this.matchStartedAt = Date.now() - (elapsedSeconds - 1) * 1000;
    this.setData({
      scoreA: Number(playState.scoreA || 0),
      scoreB: Number(playState.scoreB || 0),
      elapsedSeconds,
      settlementLocked: Boolean(playState.winnerSide)
    }, () => this.refreshTimeState());
  },

  startTimer() {
    this.stopTimer();

    if (!this.matchStartedAt) {
      this.matchStartedAt = Date.now() - (this.data.elapsedSeconds - 1) * 1000;
    }

    this.syncElapsedTime();
    this.timer = setInterval(() => {
      this.syncElapsedTime();
    }, 1000);
  },

  stopTimer() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  },

  syncElapsedTime() {
    const elapsedSeconds = Math.max(1, Math.floor((Date.now() - this.matchStartedAt) / 1000) + 1);

    this.setData({ elapsedSeconds }, () => this.refreshTimeState());
  },

  refreshTimeState() {
    const minimumSeconds = this.data.setup.mode.minimumMinutes * 60;
    const remainingSeconds = Math.max(0, minimumSeconds - this.data.elapsedSeconds);
    const timeReady = remainingSeconds === 0;

    this.setData({
      timeReady,
      elapsedText: formatDuration(this.data.elapsedSeconds),
      remainingText: timeReady ? "已满足最低有效时间" : `还差 ${formatDuration(remainingSeconds)}`
    });
  },

  async changeScore(event) {
    if (this.data.settlementLocked || this.data.starting || this.data.scoreUpdating || this.data.startError) {
      return;
    }

    const side = event.currentTarget.dataset.side;
    const delta = Number(event.currentTarget.dataset.delta);

    this.setData({ scoreUpdating: true });

    try {
      const result = ensureOk(await recordMatchScore({
        matchId: this.data.matchId,
        side,
        delta,
        scoreA: this.data.scoreA,
        scoreB: this.data.scoreB,
        targetWins: this.data.setup.mode.targetWins,
        minimumMinutes: this.data.setup.mode.minimumMinutes,
        startedAtMs: this.matchStartedAt || 0
      }));
      const playState = result.playState || {};

      this.applyPlayState(playState);

      if (playState.winnerSide) {
        this.stopTimer();
        this.handleTargetReached(playState.winnerSide, playState);
      }
    } catch (error) {
      wx.showToast({
        title: error.message || "盘数同步失败",
        icon: "none"
      });
    } finally {
      this.setData({ scoreUpdating: false });
    }
  },

  handleTargetReached(winnerSide, playState = {}) {
    const { setup } = this.data;
    const elapsedSeconds = Math.max(1, Number(playState.elapsedSeconds || this.data.elapsedSeconds || 1));
    const elapsedText = formatDuration(elapsedSeconds);
    const scoreA = Number(playState.scoreA ?? this.data.scoreA);
    const scoreB = Number(playState.scoreB ?? this.data.scoreB);
    const timeReady = playState.timeReady !== undefined ? Boolean(playState.timeReady) : this.data.timeReady;
    const query = buildQuery({
      matchId: this.data.matchId || this.data.match.id || this.data.match.matchId || "",
      modeId: setup.mode.modeId,
      base: setup.selectedBase,
      multiplier: setup.selectedMultiplier,
      risk: setup.riskPoints,
      elapsed: elapsedSeconds,
      elapsedText,
      scoreA,
      scoreB,
      winner: winnerSide
    });

    if (!timeReady) {
      wx.navigateTo({ url: `/pages/time-insufficient/time-insufficient?${query}` });
      return;
    }

    wx.navigateTo({ url: `/pages/settlement/settlement?${query}` });
  },

  retryStart() {
    this.startRemoteMatch();
  },

  goBackHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  }
});
