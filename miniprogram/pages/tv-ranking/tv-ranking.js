const { requireRole } = require("../../utils/access-control");
const { ensureOk } = require("../../services/api-client");
const { getScreenBoard } = require("../../services/screen-service");

const initialBoard = ensureOk(getScreenBoard());

Page({
  data: {
    accessReady: false,
    match: initialBoard.match,
    screenConfig: initialBoard.screenConfig,
    topRows: initialBoard.topRows,
    rankingRows: initialBoard.rankingRows,
    bountyRows: initialBoard.bountyRows
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
    this.refreshTimer = setInterval(() => {
      const board = ensureOk(getScreenBoard());

      this.setData({
        match: board.match,
        screenConfig: board.screenConfig,
        topRows: board.topRows,
        rankingRows: board.rankingRows,
        bountyRows: board.bountyRows
      });
    }, 60000);
  },

  onHide() {
    this.clearRefreshTimer();
  },

  onUnload() {
    this.clearRefreshTimer();
  },

  clearRefreshTimer() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
      this.refreshTimer = null;
    }
  }
});
