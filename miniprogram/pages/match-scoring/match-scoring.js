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
    timeReady: false
  },

  onLoad(options) {
    const setup = ensureOk(getMatchSetup(options));
    this.setData({ setup }, () => this.refreshTimeState());
  },

  onShow() {
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
    this.timer = setInterval(() => {
      this.setData({
        elapsedSeconds: this.data.elapsedSeconds + 1
      }, () => this.refreshTimeState());
    }, 1000);
  },

  stopTimer() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
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
    const side = event.currentTarget.dataset.side;
    const delta = Number(event.currentTarget.dataset.delta);
    const key = side === "a" ? "scoreA" : "scoreB";
    const targetWins = this.data.setup.mode.targetWins;
    const next = Math.max(0, Math.min(targetWins, this.data[key] + delta));

    this.setData({ [key]: next }, () => {
      if (next >= targetWins) {
        this.handleTargetReached(side);
      }
    });
  },

  handleTargetReached(winnerSide) {
    const { setup, elapsedSeconds, elapsedText, scoreA, scoreB } = this.data;
    const query = [
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
