const DEFAULT_MODES = [
  {
    modeId: "race5",
    name: "抢5",
    targetWins: 5,
    minimumMinutes: 40,
    baseOptions: [20, 50, 100],
    multipliers: [1, 2, 3],
    normalReward: "10 ~ 20",
    sprintReward: "50 ~ 100",
    starReward: 1,
    enabled: true,
    rankedEnabled: true
  },
  {
    modeId: "race7",
    name: "抢7",
    targetWins: 7,
    minimumMinutes: 80,
    baseOptions: [50, 100, 200],
    multipliers: [1, 2, 3, 4, 5],
    normalReward: "30 ~ 80",
    sprintReward: "100 ~ 200",
    starReward: 2,
    enabled: true,
    rankedEnabled: true
  },
  {
    modeId: "race10",
    name: "抢10",
    targetWins: 10,
    minimumMinutes: 100,
    baseOptions: [100, 200, 300],
    multipliers: [1, 2, 3, 5, 10],
    normalReward: "80 ~ 150",
    sprintReward: "200 ~ 300",
    starReward: 3,
    enabled: false,
    rankedEnabled: true
  }
];

const RANK_TIERS = [
  { id: "bronze", label: "青铜", lossProtected: true },
  { id: "silver", label: "白银", lossProtected: true },
  { id: "gold", label: "黄金", lossProtected: true },
  { id: "platinum", label: "铂金", lossProtected: false },
  { id: "diamond", label: "钻石", lossProtected: false },
  { id: "starGlory", label: "星耀", lossProtected: false },
  { id: "king", label: "王者", lossProtected: false, king: true }
];

const DIVISION_LABELS = {
  1: "I",
  2: "II",
  3: "III"
};

const STARS_PER_DIVISION = 3;

function numberOrDefault(value, fallback) {
  const numberValue = Number(value);

  return Number.isFinite(numberValue) ? numberValue : fallback;
}

function resultOk(data) {
  return {
    ok: true,
    ...data
  };
}

function resultFail(code, message, data = {}) {
  return {
    ok: false,
    code,
    message,
    ...data
  };
}

function getModeById(modeId, modeList = DEFAULT_MODES) {
  return modeList.find((mode) => mode.modeId === modeId) || modeList[0];
}

function normalizeMode(input = {}, modeList = DEFAULT_MODES) {
  const rawMode = input.mode || getModeById(input.modeId, modeList);

  return {
    ...rawMode,
    targetWins: numberOrDefault(rawMode.targetWins, 5),
    minimumMinutes: numberOrDefault(rawMode.minimumMinutes, 40),
    baseOptions: Array.isArray(rawMode.baseOptions) ? rawMode.baseOptions.map(Number) : [],
    multipliers: Array.isArray(rawMode.multipliers) ? rawMode.multipliers.map(Number) : [],
    starReward: numberOrDefault(rawMode.starReward, 0),
    enabled: rawMode.enabled !== false,
    rankedEnabled: rawMode.rankedEnabled !== false
  };
}

function parseRewardRange(rangeText) {
  if (Array.isArray(rangeText)) {
    const min = numberOrDefault(rangeText[0], 0);
    const max = numberOrDefault(rangeText[1], min);

    return min <= max ? { min, max } : { min: max, max: min };
  }

  const values = String(rangeText || "")
    .match(/\d+/g)
    ?.map((value) => Number(value)) || [0, 0];
  const min = values[0] || 0;
  const max = values[1] || min;

  return min <= max ? { min, max } : { min: max, max: min };
}

function calculateRewardValue(rangeText, seed = 0) {
  const { min, max } = parseRewardRange(rangeText);
  const span = Math.max(max - min + 1, 1);

  return min + (Math.abs(Number(seed || 0)) % span);
}

function getRewardPhase(params = {}) {
  if (params.forceSprint) {
    return {
      phase: "sprint",
      reason: "forceSprint"
    };
  }

  if (numberOrDefault(params.roundIndex, 1) >= 4) {
    return {
      phase: "sprint",
      reason: "fourthRound"
    };
  }

  return {
    phase: "normal",
    reason: "normalRound"
  };
}

function validateBaseAndMultiplier(mode, selectedBase, selectedMultiplier) {
  if (!mode.baseOptions.includes(selectedBase)) {
    return resultFail("INVALID_BASE_POINTS", "挑战底分不在当前玩法范围内");
  }

  if (!mode.multipliers.includes(selectedMultiplier)) {
    return resultFail("INVALID_MULTIPLIER", "积分倍率不在当前玩法范围内");
  }

  return resultOk();
}

function deriveWinnerSide(params, targetWins) {
  if (params.winnerSide === "b" || params.winner === "b") {
    return "b";
  }

  if (params.winnerSide === "a" || params.winner === "a") {
    return "a";
  }

  const scoreA = numberOrDefault(params.scoreA, 0);
  const scoreB = numberOrDefault(params.scoreB, 0);

  return scoreB >= targetWins && scoreB > scoreA ? "b" : "a";
}

function calculateMatchSettlement(params = {}) {
  const mode = normalizeMode(params, params.modeList || DEFAULT_MODES);
  const selectedBase = numberOrDefault(params.selectedBase ?? params.base, mode.baseOptions[0]);
  const selectedMultiplier = numberOrDefault(params.selectedMultiplier ?? params.multiplier, mode.multipliers[0]);
  const validation = validateBaseAndMultiplier(mode, selectedBase, selectedMultiplier);

  if (!validation.ok) {
    return validation;
  }

  const riskPoints = selectedBase * selectedMultiplier;
  const scoreA = numberOrDefault(params.scoreA, 0);
  const scoreB = numberOrDefault(params.scoreB, 0);
  const winnerSide = deriveWinnerSide(params, mode.targetWins);
  const winnerScore = winnerSide === "a" ? scoreA : scoreB;

  if (winnerScore < mode.targetWins) {
    return resultFail("TARGET_SCORE_NOT_REACHED", "尚未达到胜利盘数", {
      targetWins: mode.targetWins,
      scoreA,
      scoreB
    });
  }

  const elapsedSeconds = numberOrDefault(params.elapsedSeconds ?? params.elapsed, mode.minimumMinutes * 60);
  const minimumSeconds = mode.minimumMinutes * 60;

  if (elapsedSeconds < minimumSeconds) {
    return resultFail("MINIMUM_TIME_NOT_MET", "本场未满最低有效时间，暂不能清算", {
      elapsedSeconds,
      minimumSeconds,
      remainingSeconds: minimumSeconds - elapsedSeconds
    });
  }

  const rewardPhase = getRewardPhase(params);
  const rewardRange = rewardPhase.phase === "sprint" ? mode.sprintReward : mode.normalReward;
  const rewardSeed = numberOrDefault(
    params.rewardSeed,
    elapsedSeconds + selectedBase + selectedMultiplier + scoreA + scoreB
  );
  const rewardValue = params.rewardValue !== undefined || params.reward !== undefined
    ? numberOrDefault(params.rewardValue ?? params.reward, 0)
    : calculateRewardValue(rewardRange, rewardSeed);
  const winnerDelta = riskPoints + rewardValue;
  const loserDelta = rewardValue - riskPoints;

  return resultOk({
    mode,
    selectedBase,
    selectedMultiplier,
    riskPoints,
    scoreA,
    scoreB,
    scoreText: `${scoreA}:${scoreB}`,
    winnerSide,
    loserSide: winnerSide === "a" ? "b" : "a",
    elapsedSeconds,
    minimumSeconds,
    rewardPhase: rewardPhase.phase,
    rewardPhaseReason: rewardPhase.reason,
    rewardRange,
    rewardValue,
    winnerDelta,
    loserDelta,
    starReward: mode.rankedEnabled ? mode.starReward : 0
  });
}

function getTierIndex(tierId) {
  const index = RANK_TIERS.findIndex((tier) => tier.id === tierId);

  return index >= 0 ? index : 0;
}

function normalizeRankState(rankState = {}) {
  const tierIndex = getTierIndex(rankState.tier || "bronze");
  const tier = RANK_TIERS[tierIndex];

  return {
    tier: tier.id,
    division: Math.min(Math.max(numberOrDefault(rankState.division, 3), 1), 3),
    stars: Math.min(Math.max(numberOrDefault(rankState.stars, 0), 0), STARS_PER_DIVISION - 1)
  };
}

function advanceOneStar(state) {
  if (state.tier === "king") {
    return state;
  }

  const next = { ...state, stars: state.stars + 1 };

  if (next.stars < STARS_PER_DIVISION) {
    return next;
  }

  next.stars = 0;

  if (next.division > 1) {
    next.division -= 1;
    return next;
  }

  const nextTierIndex = Math.min(getTierIndex(next.tier) + 1, RANK_TIERS.length - 1);
  next.tier = RANK_TIERS[nextTierIndex].id;
  next.division = next.tier === "king" ? 1 : 3;

  return next;
}

function loseOneStar(state) {
  const tier = RANK_TIERS[getTierIndex(state.tier)];

  if (tier.lossProtected) {
    return {
      after: state,
      protected: true
    };
  }

  if (state.stars > 0) {
    return {
      after: {
        ...state,
        stars: state.stars - 1
      },
      protected: false
    };
  }

  if (state.division < 3) {
    return {
      after: {
        ...state,
        division: state.division + 1,
        stars: STARS_PER_DIVISION - 1
      },
      protected: false
    };
  }

  const currentTierIndex = getTierIndex(state.tier);
  const previousTierIndex = Math.max(currentTierIndex - 1, 0);
  const previousTier = RANK_TIERS[previousTierIndex];

  return {
    after: {
      tier: previousTier.id,
      division: previousTier.id === "king" ? 1 : 1,
      stars: STARS_PER_DIVISION - 1
    },
    protected: false
  };
}

function calculateRankChange(params = {}) {
  const before = normalizeRankState(params.rankState);

  if (params.result !== "win") {
    const loss = loseOneStar(before);

    return {
      before,
      after: loss.after,
      protected: loss.protected,
      deltaStars: loss.protected ? 0 : -1
    };
  }

  const reward = Math.max(numberOrDefault(params.starReward, 1), 0);
  let after = before;

  for (let index = 0; index < reward; index += 1) {
    after = advanceOneStar(after);
  }

  return {
    before,
    after,
    protected: false,
    deltaStars: reward
  };
}

function formatRankTitle(rankState = {}) {
  const state = normalizeRankState(rankState);
  const tier = RANK_TIERS[getTierIndex(state.tier)];

  if (tier.king) {
    return tier.label;
  }

  return `${tier.label} ${DIVISION_LABELS[state.division] || "III"}`;
}

module.exports = {
  DEFAULT_MODES,
  RANK_TIERS,
  STARS_PER_DIVISION,
  calculateMatchSettlement,
  calculateRankChange,
  calculateRewardValue,
  formatRankTitle,
  getModeById,
  getRewardPhase,
  normalizeMode,
  normalizeRankState,
  parseRewardRange
};
