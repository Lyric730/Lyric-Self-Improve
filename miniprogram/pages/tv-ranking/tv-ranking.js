const { requireRole } = require("../../utils/access-control");
const { ensureOk } = require("../../services/api-client");
const { getScreenBoard } = require("../../services/screen-service");

Page({
  data: {
    accessReady: false,
    loading: true,
    errorText: "",
    match: {
      clubName: "云瀚台球俱乐部"
    },
    screenConfig: {
      storeBoard: "店内总榜",
      bountyBoard: "赏金猎人",
      refreshText: "60 秒刷新",
      activityTitle: "今晚活动",
      activityText: "完成有效挑战，随机奖励提升"
    },
    topRows: [],
    rankingRows: [],
    bountyRows: [],
    topRowsEmpty: true,
    rankingRowsEmpty: true,
    bountyRowsEmpty: true
  },

  onLoad() {
    const accessReady = requireRole(["staff", "owner", "screen"]);

    this.hasAccess = accessReady;
    this.setData({ accessReady });
  },

  onShow() {
    if (!this.hasAccess) {
      return;
    }

    this.clearRefreshTimer();
    this.loadBoard();
    this.refreshTimer = setInterval(() => {
      this.loadBoard({ silent: true });
    }, 60000);
  },

  onHide() {
    this.clearRefreshTimer();
  },

  onUnload() {
    this.clearRefreshTimer();
  },

  async loadBoard(options = {}) {
    if (!options.silent) {
      this.setData({
        loading: true,
        errorText: ""
      });
    }

    try {
      const board = ensureOk(await getScreenBoard());
      const topRows = board.topRows || [];
      const rankingRows = board.rankingRows || [];
      const bountyRows = board.bountyRows || [];

      this.setData({
        match: board.match,
        screenConfig: board.screenConfig,
        topRows,
        rankingRows,
        bountyRows,
        topRowsEmpty: topRows.length === 0,
        rankingRowsEmpty: rankingRows.length === 0,
        bountyRowsEmpty: bountyRows.length === 0,
        loading: false,
        errorText: ""
      });
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "大屏数据读取失败，请稍后重试"
      });
    }
  },

  retryLoad() {
    this.loadBoard();
  },

  clearRefreshTimer() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
      this.refreshTimer = null;
    }
  }
});
