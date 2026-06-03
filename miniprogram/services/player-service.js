const { callCloud, ensureOk, success } = require("./api-client");
const {
  challengeGate,
  friendRows,
  incomingChallenge,
  match,
  playerStats,
  pointsPerks,
  rankingRows,
  roomState,
  sameRankRows
} = require("../utils/ladder-data");
const { isDevtoolsPreview } = require("../utils/dev-preview");

function getLocalChallengeHome() {
  return success({
    match,
    challengeGate
  });
}

function getWaitingRoom() {
  return success(roomState);
}

function getIncomingChallenge() {
  return success(incomingChallenge);
}

function getLocalPlayerProfile() {
  return success({
    match,
    playerStats
  });
}

function getLocalRankingTabs() {
  return success([
    { id: "store", label: "店内总榜", rows: rankingRows },
    { id: "sameRank", label: "同段位榜", rows: sameRankRows },
    { id: "friends", label: "微信好友榜", rows: friendRows }
  ]);
}

function getLocalPointsPerks() {
  return success({
    match,
    pointsPerks
  });
}

async function getPlayerProfile() {
  try {
    const result = ensureOk(await callCloud("player", "getProfile"));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return getLocalPlayerProfile();
}

async function getChallengeHome(params = {}) {
  try {
    const result = ensureOk(await callCloud("player", "getChallengeHome", {
      tableId: params.tableId || "",
      tableNo: params.tableNo || "",
      storeId: params.storeId || "default"
    }));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return getLocalChallengeHome();
}

async function getRankingTabs() {
  try {
    const result = ensureOk(await callCloud("player", "getRankings"));

    return success(result.tabs || []);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return getLocalRankingTabs();
}

async function getPointsPerks() {
  try {
    const result = ensureOk(await callCloud("player", "getPointsPerks"));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return getLocalPointsPerks();
}

module.exports = {
  getChallengeHome,
  getIncomingChallenge,
  getPlayerProfile,
  getPointsPerks,
  getRankingTabs,
  getWaitingRoom
};
