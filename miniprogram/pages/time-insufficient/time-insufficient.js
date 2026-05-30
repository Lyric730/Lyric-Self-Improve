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
    elapsedText: "00:00:01",
    requiredText: "00:40:00"
  },

  onLoad(options) {
    const setup = ensureOk(getMatchSetup(options));
    const elapsedSeconds = Number(options.elapsed || 1);

    this.setData({
      setup,
      elapsedText: formatDuration(elapsedSeconds),
      requiredText: formatDuration(setup.mode.minimumMinutes * 60)
    });
  },

  keepPlaying() {
    wx.navigateBack();
  },

  extendTime() {
    wx.navigateBack();
  }
});
