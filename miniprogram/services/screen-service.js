const { callCloud, ensureOk, success } = require("./api-client");
const { getAdminConfig } = require("./admin-service");
const { isDevtoolsPreview } = require("../utils/dev-preview");
const { rankingRows, bountyRows, topRows, match } = require("../utils/ladder-data");

function getLocalScreenBoard() {
  const adminConfig = ensureOk(getAdminConfig());

  return success({
    match,
    screenConfig: adminConfig.screen,
    topRows,
    rankingRows: rankingRows.slice(3),
    bountyRows
  });
}

async function getScreenBoard(params = {}) {
  try {
    const board = ensureOk(await callCloud("screen", "getBoard", {
      storeId: params.storeId || "default",
      screenToken: params.screenToken || ""
    }));

    return success(board);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return getLocalScreenBoard();
}

module.exports = {
  getScreenBoard
};
