const assert = require("assert");
const {
  calculateMatchSettlement,
  calculateRankChange,
  getRewardPhase,
  normalizeMode
} = require("../miniprogram/utils/settlement-engine");

function assertSettlement(input, expected) {
  const result = calculateMatchSettlement(input);

  assert.strictEqual(result.ok, true, result.message || "settlement should pass");
  assert.strictEqual(result.riskPoints, expected.riskPoints);
  assert.strictEqual(result.rewardValue, expected.rewardValue);
  assert.strictEqual(result.winnerDelta, expected.winnerDelta);
  assert.strictEqual(result.loserDelta, expected.loserDelta);
  assert.strictEqual(result.starReward, expected.starReward);

  return result;
}

assert.deepStrictEqual(normalizeMode({ modeId: "race5" }).baseOptions, [20, 50, 100]);
assert.strictEqual(getRewardPhase({ roundIndex: 1 }).phase, "normal");
assert.strictEqual(getRewardPhase({ roundIndex: 4 }).phase, "sprint");
assert.strictEqual(getRewardPhase({ forceSprint: true }).phase, "sprint");

assertSettlement(
  {
    modeId: "race5",
    selectedBase: 50,
    selectedMultiplier: 2,
    scoreA: 5,
    scoreB: 3,
    winnerSide: "a",
    elapsedSeconds: 40 * 60,
    rewardValue: 16
  },
  {
    riskPoints: 100,
    rewardValue: 16,
    winnerDelta: 116,
    loserDelta: -84,
    starReward: 1
  }
);

assertSettlement(
  {
    modeId: "race7",
    selectedBase: 100,
    selectedMultiplier: 3,
    scoreA: 4,
    scoreB: 7,
    winnerSide: "b",
    elapsedSeconds: 80 * 60,
    rewardValue: 50
  },
  {
    riskPoints: 300,
    rewardValue: 50,
    winnerDelta: 350,
    loserDelta: -250,
    starReward: 2
  }
);

const timeBlocked = calculateMatchSettlement({
  modeId: "race5",
  selectedBase: 50,
  selectedMultiplier: 2,
  scoreA: 5,
  scoreB: 0,
  elapsedSeconds: 20 * 60,
  rewardValue: 16
});

assert.strictEqual(timeBlocked.ok, false);
assert.strictEqual(timeBlocked.code, "MINIMUM_TIME_NOT_MET");
assert.strictEqual(timeBlocked.remainingSeconds, 20 * 60);

const invalidBase = calculateMatchSettlement({
  modeId: "race5",
  selectedBase: 999,
  selectedMultiplier: 2,
  scoreA: 5,
  scoreB: 0,
  elapsedSeconds: 40 * 60
});

assert.strictEqual(invalidBase.ok, false);
assert.strictEqual(invalidBase.code, "INVALID_BASE_POINTS");

const sprintSettlement = calculateMatchSettlement({
  modeId: "race5",
  selectedBase: 100,
  selectedMultiplier: 3,
  scoreA: 5,
  scoreB: 2,
  elapsedSeconds: 45 * 60,
  roundIndex: 4,
  rewardSeed: 7
});

assert.strictEqual(sprintSettlement.ok, true);
assert.strictEqual(sprintSettlement.rewardPhase, "sprint");
assert.ok(sprintSettlement.rewardValue >= 50 && sprintSettlement.rewardValue <= 100);

const goldLossProtected = calculateRankChange({
  result: "loss",
  rankState: {
    tier: "gold",
    division: 1,
    stars: 0
  }
});

assert.strictEqual(goldLossProtected.after.tier, "gold");
assert.strictEqual(goldLossProtected.after.division, 1);
assert.strictEqual(goldLossProtected.after.stars, 0);
assert.strictEqual(goldLossProtected.protected, true);

const platinumLoss = calculateRankChange({
  result: "loss",
  rankState: {
    tier: "platinum",
    division: 2,
    stars: 2
  }
});

assert.strictEqual(platinumLoss.after.tier, "platinum");
assert.strictEqual(platinumLoss.after.division, 2);
assert.strictEqual(platinumLoss.after.stars, 1);
assert.strictEqual(platinumLoss.protected, false);

const rankUp = calculateRankChange({
  result: "win",
  starReward: 2,
  rankState: {
    tier: "gold",
    division: 3,
    stars: 2
  }
});

assert.strictEqual(rankUp.after.tier, "gold");
assert.strictEqual(rankUp.after.division, 2);
assert.strictEqual(rankUp.after.stars, 1);

console.log("Settlement engine tests OK");
