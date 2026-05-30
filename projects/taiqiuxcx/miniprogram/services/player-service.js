const { success } = require("./api-client");
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

function getChallengeHome() {
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

function getPlayerProfile() {
  return success({
    match,
    playerStats
  });
}

function getRankingTabs() {
  return success([
    { id: "store", label: "店内总榜", rows: rankingRows },
    { id: "sameRank", label: "同段位榜", rows: sameRankRows },
    { id: "friends", label: "好友榜", rows: friendRows }
  ]);
}

function getPointsPerks() {
  return success({
    match,
    pointsPerks
  });
}

module.exports = {
  getChallengeHome,
  getIncomingChallenge,
  getPlayerProfile,
  getPointsPerks,
  getRankingTabs,
  getWaitingRoom
};
