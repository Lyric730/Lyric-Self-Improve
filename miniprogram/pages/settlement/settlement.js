const { ensureOk } = require("../../services/api-client");
const { getCurrentMatch, previewSettlement, settleCurrentMatch } = require("../../services/match-service");

function buildParams(options = {}) {
  return {
    ...options,
    elapsedText: options.elapsedText ? decodeURIComponent(options.elapsedText) : ""
  };
}

function buildPreviewErrorState(error) {
  const code = error && error.code ? error.code : "REQUEST_FAILED";

  if (code === "MATCH_ID_REQUIRED") {
    return {
      previewTitle: "缺少比赛记录",
      previewSubtitle: "无法读取本场结算预览",
      previewErrorText: "请从计分页完成比赛后进入结算确认。"
    };
  }

  if (code === "MATCH_NOT_FOUND") {
    return {
      previewTitle: "比赛不存在",
      previewSubtitle: "服务端未找到本场比赛",
      previewErrorText: "请回到首页重新发起挑战，或联系前台确认本场比赛是否已被作废。"
    };
  }

  if (code === "MATCH_ALREADY_SETTLED") {
    return {
      previewTitle: "比赛已结算",
      previewSubtitle: "本场不能重复结算",
      previewErrorText: "请返回首页查看排行榜或个人积分变化。"
    };
  }

  if (code === "POINTS_BALANCE_NOT_ENOUGH") {
    return {
      previewTitle: "积分不足",
      previewSubtitle: "本场暂时不能结算",
      previewErrorText: "败方积分不足以覆盖风险积分，请调整底分倍率或联系前台处理。"
    };
  }

  return {
    previewTitle: "结算预览失败",
    previewSubtitle: "服务端暂时无法计算本场结果",
    previewErrorText: error && error.message ? error.message : "请稍后重试，或联系前台确认比赛状态。"
  };
}

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
    settlement: null,
    settlementParams: {},
    nextQuery: "",
    previewStatus: "loading",
    previewTitle: "结算预览中",
    previewSubtitle: "正在读取服务端结算预览",
    previewErrorText: "",
    previewing: true,
    settling: false
  },

  async onLoad(options) {
    const params = buildParams(options);

    this.setData({
      settlementParams: params
    });

    await this.loadPreview(params);
  },

  async loadPreview(params = {}) {
    this.setData({
      settlement: null,
      nextQuery: "",
      previewStatus: "loading",
      previewTitle: "结算预览中",
      previewSubtitle: "正在读取服务端结算预览",
      previewErrorText: "",
      previewing: true
    });

    try {
      const settlement = ensureOk(await previewSettlement(params));
      settlement.matchId = params.matchId || settlement.matchId || "";

      this.setData({
        settlement,
        nextQuery: buildSettlementQuery(settlement),
        previewStatus: "ready",
        previewTitle: "结算确认",
        previewSubtitle: `${settlement.mode.name} · ${settlement.scoreText} · ${settlement.elapsedText}`
      });
    } catch (error) {
      const errorState = buildPreviewErrorState(error);

      this.setData({
        previewStatus: "error",
        ...errorState
      });
    } finally {
      this.setData({ previewing: false });
    }
  },

  retryPreview() {
    this.loadPreview(this.data.settlementParams);
  },

  async confirm() {
    if (this.data.settling || this.data.previewStatus !== "ready" || !this.data.settlement) {
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
    if (this.data.previewStatus !== "ready" || !this.data.nextQuery) {
      return;
    }

    wx.navigateTo({ url: `/pages/refusal/refusal?${this.data.nextQuery}` });
  },

  goHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  }
});
