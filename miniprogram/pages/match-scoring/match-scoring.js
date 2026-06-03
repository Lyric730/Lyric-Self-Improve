const { ensureOk } = require("../../services/api-client");
const { getCurrentMatch, getMatchSetup } = require("../../services/match-service");

function formatDuration(totalSeconds) {
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
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
    settlementLocked: false
  },

  onLoad(options) {
    const setup = ensureOk(getMatchSetup(options));
    const initialElapsed = Math.max(1, Number(options.elapsed || 1));

    this.matchStartedAt = Date.now() - (initialElapsed - 1) * 1000;
    this.setData({
      setup,
      elapsedSeconds: initialElapsed
    }, () => this.refreshTimeState());
  },

  onShow() {
    this.setData({ settlementLocked: false });
    this.startTimer();
  },

  onHide() {
    this.stopTimer();
  },

  onUnload() {
    this.stopTimer();
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

  changeScore(event) {
    if (this.data.settlementLocked) {
      return;
    }

    const side = event.currentTarget.dataset.side;
    const delta = Number(event.currentTarget.dataset.delta);
    const key = side === "a" ? "scoreA" : "scoreB";
    const targetWins = this.data.setup.mode.targetWins;
    const next = Math.max(0, Math.min(targetWins, this.data[key] + delta));

    this.setData({ [key]: next }, () => {
      if (next >= targetWins) {
        this.setData({ settlementLocked: true });
        this.handleTargetReached(side);
      }
    });
  },

  handleTargetReached(winnerSide) {
    const { setup, elapsedSeconds, elapsedText, scoreA, scoreB } = this.data;
    const query = [
      `matchId=${this.data.match.id || this.data.match.matchId || ""}`,
      `modeId=${setup.mode.modeId}`,
      `base=${setup.selectedBase}`,
      `multiplier=${setup.selectedMultiplier}`,
      `risk=${setup.riskPoints}`,
      `elapsed=${elapsedSeconds}`,
      `elapsedText=${encodeURIComponent(elapsedText)}`,
      `scoreA=${scoreA}`,
      `scoreB=${scoreB}`,
      `winner=${winnerSide}`
    ].join("&");

    if (!this.data.timeReady) {
      wx.navigateTo({ url: `/pages/time-insufficient/time-insufficient?${query}` });
      return;
    }

    wx.navigateTo({ url: `/pages/settlement/settlement?${query}` });
  }
});
