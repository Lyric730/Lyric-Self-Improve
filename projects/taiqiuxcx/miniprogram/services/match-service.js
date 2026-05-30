const { success } = require("./api-client");
const { buildMatchSetup, buildSettlement, match, modes } = require("../utils/ladder-data");

function getModes() {
  return success(modes);
}

function getCurrentMatch() {
  return success(match);
}

function getMatchSetup(params = {}) {
  return success(buildMatchSetup(params));
}

function calculateSettlement(params = {}) {
  return success(buildSettlement(params));
}

module.exports = {
  calculateSettlement,
  getCurrentMatch,
  getMatchSetup,
  getModes
};
