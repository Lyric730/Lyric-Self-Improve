const { callCloud, ensureOk, success } = require("./api-client");
const { buildMatchSetup, buildSettlement, match, modes } = require("../utils/ladder-data");
const { isDevtoolsPreview } = require("../utils/dev-preview");

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

function formatSignedPoints(value) {
  const numberValue = Number(value || 0);
  return numberValue > 0 ? `+${numberValue}` : `${numberValue}`;
}

function buildSettlementPayload(params = {}) {
  return {
    matchId: params.matchId || match.id || match.matchId || match.roomNo,
    playerAOpenid: params.playerAOpenid || (match.playerA && match.playerA.openid),
    playerBOpenid: params.playerBOpenid || (match.playerB && match.playerB.openid),
    modeId: params.modeId || (match.selectedMode && match.selectedMode.modeId),
    selectedBase: Number(params.selectedBase || params.base || match.selectedBase),
    selectedMultiplier: Number(params.selectedMultiplier || params.multiplier || match.selectedMultiplier),
    scoreA: Number(params.scoreA || match.scoreA),
    scoreB: Number(params.scoreB || match.scoreB),
    winnerSide: params.winnerSide || params.winner,
    elapsedSeconds: Number(params.elapsedSeconds || params.elapsed || 0),
    rewardValue: params.rewardValue !== undefined ? Number(params.rewardValue) : Number(params.reward || 0),
    rankStateA: match.playerA && match.playerA.rankState,
    rankStateB: match.playerB && match.playerB.rankState
  };
}

async function settleCurrentMatch(params = {}) {
  const payload = buildSettlementPayload(params);

  try {
    const result = ensureOk(await callCloud("match", "settle", payload));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return calculateSettlement(params);
}

async function previewSettlement(params = {}) {
  if (!params.matchId && !isDevtoolsPreview()) {
    const error = new Error("缺少比赛 ID，无法读取结算预览");
    error.code = "MATCH_ID_REQUIRED";
    throw error;
  }

  const payload = buildSettlementPayload(params);

  try {
    const result = ensureOk(await callCloud("match", "previewSettlement", payload));

    return success(mergeSettlementDisplay(params, result));
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  return calculateSettlement(params);
}

function mergeSettlementDisplay(params = {}, serverResult = {}) {
  const base = buildSettlement(params);
  const serverSettlement = serverResult.settlement || {};
  const matchId = serverResult.matchId || serverSettlement.matchId || params.matchId || "";
  const winnerDelta = Number(serverSettlement.winnerDelta ?? base.winnerDelta);
  const loserDelta = Number(serverSettlement.loserDelta ?? base.loserDelta);
  const rewardValue = Number(serverSettlement.rewardValue ?? base.rewardValue);
  const riskPoints = Number(serverSettlement.riskPoints ?? base.riskPoints);
  const scoreA = Number(serverSettlement.scoreA ?? base.scoreA);
  const scoreB = Number(serverSettlement.scoreB ?? base.scoreB);
  const winnerAfterPoints = base.winner.points + winnerDelta;
  const loserAfterPoints = base.loser.points + loserDelta;

  return {
    ...base,
    matchId,
    scoreA,
    scoreB,
    scoreText: `${scoreA}:${scoreB}`,
    riskPoints,
    rewardValue,
    rewardPhase: serverSettlement.rewardPhase || base.rewardPhase,
    winnerDelta,
    loserDelta,
    winnerDeltaText: formatSignedPoints(winnerDelta),
    loserDeltaText: formatSignedPoints(loserDelta),
    loserDeltaVariant: loserDelta < 0 ? "minus" : "reward",
    winnerAfterPoints,
    loserAfterPoints,
    serverStatus: serverSettlement.status || ""
  };
}

async function getSettlementResult(params = {}) {
  if (!params.matchId && !isDevtoolsPreview()) {
    const error = new Error("缺少比赛 ID，无法读取结算记录");
    error.code = "MATCH_ID_REQUIRED";
    throw error;
  }

  if (params.matchId) {
    try {
      const result = ensureOk(await callCloud("match", "getSettlement", {
        matchId: params.matchId
      }));

      return success(mergeSettlementDisplay(params, result));
    } catch (error) {
      if (!isDevtoolsPreview()) {
        throw error;
      }
    }
  }

  return calculateSettlement(params);
}

module.exports = {
  calculateSettlement,
  getSettlementResult,
  getCurrentMatch,
  getMatchSetup,
  getModes,
  previewSettlement,
  settleCurrentMatch
};
