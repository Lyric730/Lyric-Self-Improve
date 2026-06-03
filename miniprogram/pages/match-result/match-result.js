const { ensureOk } = require("../../services/api-client");
const { calculateSettlement, getCurrentMatch, getSettlementResult } = require("../../services/match-service");
const { isDevtoolsPreview } = require("../../utils/dev-preview");

function buildParams(options = {}) {
  return {
    ...options,
    elapsedText: options.elapsedText ? decodeURIComponent(options.elapsedText) : ""
  };
}

function buildErrorState(error) {
  const code = error && error.code ? error.code : "REQUEST_FAILED";

  if (code === "MATCH_ID_REQUIRED") {
    return {
      resultTitle: "缺少结算记录",
      resultSubtitle: "本场比赛没有有效的结算编号",
      errorText: "请从比赛结算确认页进入，或回到首页重新发起挑战。"
    };
  }

  if (code === "SETTLEMENT_NOT_FOUND") {
    return {
      resultTitle: "结算记录不存在",
      resultSubtitle: "服务端暂未找到本场结算单",
      errorText: "请确认双方已完成结算确认；如果刚刚结算，请稍后重试。"
    };
  }

  return {
    resultTitle: "结算读取失败",
    resultSubtitle: "服务端结算记录暂时无法读取",
    errorText: error && error.message ? error.message : "请稍后重试，或联系前台确认本场积分是否已结算。"
  };
}

Page({
  data: {
    match: ensureOk(getCurrentMatch()),
    settlement: null,
    settlementParams: {},
    resultStatus: "loading",
    resultTitle: "读取结算中",
    resultSubtitle: "正在读取服务端结算记录",
    errorText: "",
    loadingSettlement: true
  },

  async onLoad(options) {
    const params = buildParams(options);

    this.setData({
      settlementParams: params
    });

    await this.loadSettlement(params);
  },

  async loadSettlement(params = {}) {
    const canPreviewLocally = isDevtoolsPreview();

    if (canPreviewLocally) {
      this.setData({
        settlement: ensureOk(calculateSettlement(params))
      });
    } else {
      this.setData({
        settlement: null
      });
    }

    this.setData({
      resultStatus: "loading",
      resultTitle: "读取结算中",
      resultSubtitle: "正在读取服务端结算记录",
      errorText: "",
      loadingSettlement: true
    });

    try {
      const settlement = ensureOk(await getSettlementResult(params));

      this.setData({
        settlement,
        resultStatus: "ready",
        resultTitle: "结算已生效",
        resultSubtitle: `${settlement.winner.name} 胜 · ${settlement.winnerDeltaText} 积分`
      });
    } catch (error) {
      const errorState = buildErrorState(error);

      this.setData({
        settlement: canPreviewLocally ? this.data.settlement : null,
        resultStatus: canPreviewLocally && this.data.settlement ? "ready" : "error",
        resultTitle: canPreviewLocally && this.data.settlement ? "结算预览" : errorState.resultTitle,
        resultSubtitle: canPreviewLocally && this.data.settlement ? "开发者工具本地预览数据" : errorState.resultSubtitle,
        errorText: canPreviewLocally && this.data.settlement ? "" : errorState.errorText
      });
    } finally {
      this.setData({ loadingSettlement: false });
    }
  },

  retrySettlement() {
    this.loadSettlement(this.data.settlementParams);
  },

  goHome() {
    wx.reLaunch({ url: "/pages/challenge-home/challenge-home" });
  },

  replay() {
    wx.navigateTo({ url: "/pages/mode-select/mode-select" });
  }
});
