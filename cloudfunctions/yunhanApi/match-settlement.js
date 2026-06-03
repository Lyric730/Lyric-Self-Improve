const {
  calculateMatchSettlement,
  calculateRankChange
} = require("./settlement-engine");

function fail(code, message, data = {}) {
  return {
    ok: false,
    code,
    message,
    ...data
  };
}

function normalizeOpenid(value) {
  return String(value || "").trim();
}

function getSideOpenid(payload, side) {
  const playerKey = side === "a" ? "playerA" : "playerB";
  const directKey = side === "a" ? "playerAOpenid" : "playerBOpenid";
  const legacyKey = side === "a" ? "hostOpenid" : "guestOpenid";
  const compactKey = side === "a" ? "openidA" : "openidB";
  const nested = payload[playerKey] && payload[playerKey].openid;

  return normalizeOpenid(payload[directKey] || payload[legacyKey] || payload[compactKey] || nested);
}

function getSideRankState(payload, side) {
  const playerKey = side === "a" ? "playerA" : "playerB";
  const directKey = side === "a" ? "rankStateA" : "rankStateB";
  const nested = payload[playerKey] && payload[playerKey].rankState;

  return payload[directKey] || nested || {};
}

function buildPointChange(openid, side, result, delta, matchId, settlement) {
  return {
    openid,
    side,
    result,
    type: result === "win" ? "match_win" : "match_loss",
    matchId,
    delta,
    riskPoints: settlement.riskPoints,
    rewardValue: settlement.rewardValue,
    rewardPhase: settlement.rewardPhase
  };
}

function buildSettlementWritePlan(payload = {}) {
  const matchId = String(payload.matchId || payload._id || "").trim();

  if (!matchId) {
    return fail("MATCH_ID_REQUIRED", "缺少比赛 ID");
  }

  const playerAOpenid = getSideOpenid(payload, "a");
  const playerBOpenid = getSideOpenid(payload, "b");

  if (!playerAOpenid || !playerBOpenid) {
    return fail("MATCH_PLAYER_REQUIRED", "缺少比赛双方会员身份");
  }

  if (playerAOpenid === playerBOpenid) {
    return fail("MATCH_PLAYERS_DUPLICATED", "比赛双方不能是同一个会员");
  }

  const settlement = calculateMatchSettlement(payload);

  if (!settlement.ok) {
    return settlement;
  }

  const winnerOpenid = settlement.winnerSide === "a" ? playerAOpenid : playerBOpenid;
  const loserOpenid = settlement.loserSide === "a" ? playerAOpenid : playerBOpenid;
  const winnerRankState = getSideRankState(payload, settlement.winnerSide);
  const loserRankState = getSideRankState(payload, settlement.loserSide);
  const winnerRankChange = calculateRankChange({
    result: "win",
    starReward: settlement.starReward,
    rankState: winnerRankState
  });
  const loserRankChange = calculateRankChange({
    result: "loss",
    rankState: loserRankState
  });

  return {
    ok: true,
    matchId,
    settlement,
    players: {
      a: {
        openid: playerAOpenid,
        rankState: getSideRankState(payload, "a")
      },
      b: {
        openid: playerBOpenid,
        rankState: getSideRankState(payload, "b")
      }
    },
    pointChanges: [
      buildPointChange(winnerOpenid, settlement.winnerSide, "win", settlement.winnerDelta, matchId, settlement),
      buildPointChange(loserOpenid, settlement.loserSide, "loss", settlement.loserDelta, matchId, settlement)
    ],
    rankChanges: {
      [settlement.winnerSide]: winnerRankChange,
      [settlement.loserSide]: loserRankChange
    }
  };
}

module.exports = {
  buildSettlementWritePlan
};
