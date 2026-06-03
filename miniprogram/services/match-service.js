const { callCloud, ensureOk, success } = require("./api-client");
const { buildMatchSetup, buildSettlement, incomingChallenge, match, modes, roomState } = require("../utils/ladder-data");
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

function buildLocalRoomState(params = {}) {
  const opponentJoined = Boolean(params.opponentJoined);

  return {
    ...roomState,
    matchId: params.matchId || roomState.matchId || roomState.roomNo,
    tableNo: params.tableNo || roomState.tableNo,
    dueTime: params.dueTime || roomState.dueTime || "",
    status: opponentJoined ? "joined" : roomState.status,
    statusText: opponentJoined ? "对手已加入" : roomState.statusText,
    statusHint: opponentJoined ? "双方确认后进入玩法选择" : roomState.statusHint,
    opponentJoined,
    guest: opponentJoined ? incomingChallenge.challenger : null,
    localPreview: true
  };
}

function buildLocalPlayState(params = {}) {
  const startedAtMs = Number(params.startedAtMs || Date.now());
  const elapsedSeconds = Math.max(1, Math.floor((Date.now() - startedAtMs) / 1000) + 1);
  const targetWins = Number(params.targetWins || (params.mode && params.mode.targetWins) || 5);
  const minimumMinutes = Number(params.minimumMinutes || (params.mode && params.mode.minimumMinutes) || 40);
  const scoreA = Number(params.scoreA || 0);
  const scoreB = Number(params.scoreB || 0);
  const winnerSide = params.winnerSide || (targetWins > 0 && scoreA >= targetWins ? "a" : targetWins > 0 && scoreB >= targetWins ? "b" : "");

  return {
    matchId: params.matchId || "",
    status: winnerSide ? "settlement_pending" : "playing",
    scoreA,
    scoreB,
    startedAtMs,
    elapsedSeconds,
    targetWins,
    minimumMinutes,
    timeReady: minimumMinutes > 0 ? elapsedSeconds >= minimumMinutes * 60 : false,
    winnerSide
  };
}

function formatSignedPoints(value) {
  const numberValue = Number(value || 0);
  return numberValue > 0 ? `+${numberValue}` : `${numberValue}`;
}

async function createChallengeRoom(params = {}) {
  const payload = {
    tableNo: params.tableNo || match.tableNo || "T03",
    dueTime: params.dueTime || match.dueTime || "",
    openedAt: params.openedAt || ""
  };

  try {
    const result = ensureOk(await callCloud("match", "createRoom", payload));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  const localRoomState = buildLocalRoomState(payload);

  return success({
    matchId: localRoomState.matchId,
    roomState: localRoomState
  });
}

async function getWaitingRoomState(params = {}) {
  if (params.matchId) {
    try {
      const result = ensureOk(await callCloud("match", "get", {
        matchId: params.matchId
      }));

      return success(result.roomState || result);
    } catch (error) {
      if (!isDevtoolsPreview()) {
        throw error;
      }
    }
  }

  return success(buildLocalRoomState(params));
}

async function joinChallengeRoom(params = {}) {
  const payload = {
    matchId: params.matchId || ""
  };

  try {
    const result = ensureOk(await callCloud("match", "joinRoom", payload));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  const localRoomState = buildLocalRoomState({
    ...params,
    opponentJoined: true
  });

  return success({
    matchId: localRoomState.matchId,
    roomState: localRoomState
  });
}

async function configureMatchSetup(params = {}) {
  const payload = {
    matchId: params.matchId || "",
    modeId: params.modeId || (params.mode && params.mode.modeId) || "",
    selectedBase: Number(params.selectedBase || params.base || 0),
    selectedMultiplier: Number(params.selectedMultiplier || params.multiplier || 0)
  };

  try {
    const result = ensureOk(await callCloud("match", "configure", payload));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  const setup = buildMatchSetup({
    ...payload,
    base: payload.selectedBase,
    multiplier: payload.selectedMultiplier
  });

  return success({
    matchId: payload.matchId,
    setup,
    roomState: {
      ...buildLocalRoomState({
        matchId: payload.matchId,
        opponentJoined: true
      }),
      status: "configured",
      setup: {
        modeId: setup.mode.modeId,
        selectedBase: setup.selectedBase,
        selectedMultiplier: setup.selectedMultiplier,
        riskPoints: setup.riskPoints,
        targetWins: setup.mode.targetWins,
        minimumMinutes: setup.mode.minimumMinutes
      }
    }
  });
}

async function startConfiguredMatch(params = {}) {
  const payload = {
    matchId: params.matchId || ""
  };

  try {
    const result = ensureOk(await callCloud("match", "start", payload));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  const setup = buildMatchSetup({
    ...params,
    base: params.selectedBase || params.base,
    multiplier: params.selectedMultiplier || params.multiplier
  });
  const playState = buildLocalPlayState({
    ...params,
    targetWins: setup.mode.targetWins,
    minimumMinutes: setup.mode.minimumMinutes
  });

  return success({
    matchId: payload.matchId,
    playState,
    roomState: {
      ...buildLocalRoomState({
        matchId: payload.matchId,
        opponentJoined: true
      }),
      status: "playing",
      setup: {
        modeId: setup.mode.modeId,
        selectedBase: setup.selectedBase,
        selectedMultiplier: setup.selectedMultiplier,
        riskPoints: setup.riskPoints,
        targetWins: setup.mode.targetWins,
        minimumMinutes: setup.mode.minimumMinutes
      },
      playState
    }
  });
}

async function recordMatchScore(params = {}) {
  const payload = {
    matchId: params.matchId || "",
    side: params.side === "b" ? "b" : "a",
    delta: Number(params.delta || 0)
  };

  try {
    const result = ensureOk(await callCloud("match", "recordScore", payload));

    return success(result);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  const targetWins = Number(params.targetWins || 5);
  const currentScoreA = Number(params.scoreA || 0);
  const currentScoreB = Number(params.scoreB || 0);
  const scoreA = payload.side === "a" ? Math.max(0, Math.min(targetWins, currentScoreA + payload.delta)) : currentScoreA;
  const scoreB = payload.side === "b" ? Math.max(0, Math.min(targetWins, currentScoreB + payload.delta)) : currentScoreB;
  const playState = buildLocalPlayState({
    ...params,
    scoreA,
    scoreB,
    targetWins
  });

  return success({
    matchId: payload.matchId,
    playState
  });
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
  configureMatchSetup,
  createChallengeRoom,
  getSettlementResult,
  getCurrentMatch,
  getMatchSetup,
  getModes,
  getWaitingRoomState,
  joinChallengeRoom,
  previewSettlement,
  recordMatchScore,
  settleCurrentMatch,
  startConfiguredMatch
};
