const { ensureOk } = require("../../services/api-client");
const { calculateSettlement, getCurrentMatch, settleCurrentMatch } = require("../../services/match-service");

function buildSettlementQuery(settlement) {
  return [
    `matchId=${settlement.matchId || ""}`,
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
    nextQuery: "",
    settling: false
  },

  onLoad(options) {
    const settlement = ensureOk(calculateSettlement({
      ...options,
      elapsedText: options.elapsedText ? decodeURIComponent(options.elapsedText) : ""
    }));
    settlement.matchId = options.matchId || settlement.matchId || "";

    this.setData({
      settlement,
      nextQuery: buildSettlementQuery(settlement)
    });
  },

  async confirm() {
    if (this.data.settling) {
      return;
    }

    this.setData({ settling: true });

    try {
      const result = ensureOk(await settleCurrentMatch(this.data.settlement));
      const settlement = result.settlement || result;
      settlement.matchId = result.matchId || settlement.matchId || this.data.settlement.matchId || "";
      const nextQuery = buildSettlementQuery(settlement);

      wx.navigateTo({ url: `/pages/match-result/match-result?${nextQuery}` });
    } catch (error) {
      wx.showToast({
        title: error.message || "结算失败",
        icon: "none"
      });
    } finally {
      this.setData({ settling: false });
    }
  },

  refuse() {
    wx.navigateTo({ url: `/pages/refusal/refusal?${this.data.nextQuery}` });
  }
});
