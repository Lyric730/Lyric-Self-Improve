const { ensureOk, success } = require("./api-client");
const { getAdminConfig } = require("./admin-service");
const { rankingRows, bountyRows, topRows, match } = require("../utils/ladder-data");

function getScreenBoard() {
  const adminConfig = ensureOk(getAdminConfig());

  return success({
    match,
    screenConfig: adminConfig.screen,
    topRows,
    rankingRows: rankingRows.slice(3),
    bountyRows
  });
}

module.exports = {
  getScreenBoard
};
