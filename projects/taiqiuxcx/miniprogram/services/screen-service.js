const { success } = require("./api-client");
const { rankingRows, bountyRows, topRows, match } = require("../utils/ladder-data");

function getScreenBoard() {
  return success({
    match,
    topRows,
    rankingRows: rankingRows.slice(3),
    bountyRows
  });
}

module.exports = {
  getScreenBoard
};
