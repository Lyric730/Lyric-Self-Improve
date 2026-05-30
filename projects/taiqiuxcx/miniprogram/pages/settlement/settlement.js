const { ensureOk } = require("../../services/api-client");
const { calculateSettlement, getCurrentMatch } = require("../../services/match-service");

function buildSettlementQuery(settlement) {
  return [
    `modeId=${settlement.mode.modeId}`,
    `base=${settlement.selectedBase}`,
    `multiplier=${settlement.selectedMultiplier}`,
    `risk=${settlement.riskPoints}`,
    `elapsed=${settlement.elapsedSeconds}`,
    `elapsedText=${encodeURIComponent(settlement.elapsedText)}`,
    `scoreA=${settlement.scoreA}`,
    `scoreB=${settlement.scoreB}`,
    `winner=${settlement.winnerSide}`,
    `reward=${settlement.rewardValue}`
  ].join("&");
}

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    settlement: ensureOk(calculateSettlement()),
    nextQuery: ""
  },

  onLoad(options) {
    const settlement = ensureOk(calculateSettlement({
      ...options,
      elapsedText: options.elapsedText ? decodeURIComponent(options.elapsedText) : ""
    }));

    this.setData({
      settlement,
      nextQuery: buildSettlementQuery(settlement)
    });
  },

  confirm() {
    wx.navigateTo({ url: `/pages/match-result/match-result?${this.data.nextQuery}` });
  },

  refuse() {
    wx.navigateTo({ url: `/pages/refusal/refusal?${this.data.nextQuery}` });
  }
});
