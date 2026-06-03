const assert = require("assert");

const miniAdmin = require("../miniprogram/utils/admin-config-validator");
const cloudAdmin = require("../cloudfunctions/yunhanApi/admin-config-validator");
const miniMember = require("../miniprogram/utils/member-profile");
const cloudMember = require("../cloudfunctions/yunhanApi/member-profile");
const miniSettlement = require("../miniprogram/utils/settlement-engine");
const cloudSettlement = require("../cloudfunctions/yunhanApi/settlement-engine");
const { buildSettlementPreview, buildSettlementWritePlan } = require("../cloudfunctions/yunhanApi/match-settlement");
const { adminConfig } = require("../miniprogram/utils/ladder-data");

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function assertSameValidation(miniResult, cloudResult) {
  assert.strictEqual(cloudResult.ok, miniResult.ok);
  assert.deepStrictEqual(cloudResult.errors, miniResult.errors);
}

const validConfig = clone(adminConfig);
assertSameValidation(
  miniAdmin.validateAdminConfig(validConfig),
  cloudAdmin.validateAdminConfig(validConfig)
);

const invalidRace9Config = clone(adminConfig);
invalidRace9Config.modes.push({
  modeId: "race9",
  name: "抢9",
  targetWins: 9,
  minimumMinutes: 90,
  starReward: 2,
  baseOptions: [100],
  multipliers: [1],
  normalReward: "10 ~ 20",
  sprintReward: "50 ~ 100",
  enabled: true
});
assertSameValidation(
  miniAdmin.validateAdminConfig(invalidRace9Config),
  cloudAdmin.validateAdminConfig(invalidRace9Config)
);

const invalidRewardConfig = clone(adminConfig);
invalidRewardConfig.modes[0].normalReward = "80 ~ 10";
assertSameValidation(
  miniAdmin.validateAdminConfig(invalidRewardConfig),
  cloudAdmin.validateAdminConfig(invalidRewardConfig)
);

const validProfile = {
  name: "云瀚-阿杰",
  phone: "13800138000",
  note: "常用 T03",
  avatarUrl: "https://example.com/avatar.png"
};
assertSameValidation(
  miniMember.validateMemberProfile(validProfile),
  cloudMember.validateMemberProfile(validProfile)
);

const invalidProfile = {
  name: "",
  phone: "123",
  note: "备注".repeat(60),
  avatarUrl: "x".repeat(501)
};
assertSameValidation(
  miniMember.validateMemberProfile(invalidProfile),
  cloudMember.validateMemberProfile(invalidProfile)
);

const settlementInput = {
  matchId: "match_001",
  playerAOpenid: "player_a",
  playerBOpenid: "player_b",
  modeId: "race5",
  selectedBase: 100,
  selectedMultiplier: 3,
  scoreA: 5,
  scoreB: 2,
  winnerSide: "a",
  elapsedSeconds: 40 * 60,
  rewardValue: 60,
  rankStateA: {
    tier: "gold",
    division: 3,
    stars: 2
  },
  rankStateB: {
    tier: "platinum",
    division: 2,
    stars: 1
  }
};
const miniSettlementResult = miniSettlement.calculateMatchSettlement(settlementInput);
const cloudSettlementResult = cloudSettlement.calculateMatchSettlement(settlementInput);
assert.strictEqual(cloudSettlementResult.ok, miniSettlementResult.ok);
assert.strictEqual(cloudSettlementResult.riskPoints, miniSettlementResult.riskPoints);
assert.strictEqual(cloudSettlementResult.rewardValue, miniSettlementResult.rewardValue);
assert.strictEqual(cloudSettlementResult.winnerDelta, miniSettlementResult.winnerDelta);
assert.strictEqual(cloudSettlementResult.loserDelta, miniSettlementResult.loserDelta);
assert.strictEqual(cloudSettlementResult.starReward, miniSettlementResult.starReward);

const settlementPlan = buildSettlementWritePlan(settlementInput);
assert.strictEqual(settlementPlan.ok, true);
assert.strictEqual(settlementPlan.pointChanges.length, 2);
assert.deepStrictEqual(
  settlementPlan.pointChanges.map((item) => [item.openid, item.type, item.delta]),
  [
    ["player_a", "match_win", 360],
    ["player_b", "match_loss", -240]
  ]
);
assert.strictEqual(settlementPlan.rankChanges.a.deltaStars, 1);
assert.strictEqual(settlementPlan.rankChanges.b.deltaStars, -1);

const settlementPreview = buildSettlementPreview(settlementInput);
assert.strictEqual(settlementPreview.ok, true);
assert.strictEqual(settlementPreview.matchId, settlementPlan.matchId);
assert.strictEqual(settlementPreview.settlement.winnerDelta, settlementPlan.settlement.winnerDelta);
assert.strictEqual(settlementPreview.settlement.loserDelta, settlementPlan.settlement.loserDelta);
assert.deepStrictEqual(settlementPreview.pointChanges, settlementPlan.pointChanges);
assert.deepStrictEqual(settlementPreview.rankChanges, settlementPlan.rankChanges);

const missingPlayerPlan = buildSettlementWritePlan({
  ...settlementInput,
  playerBOpenid: ""
});
assert.strictEqual(missingPlayerPlan.ok, false);
assert.strictEqual(missingPlayerPlan.code, "MATCH_PLAYER_REQUIRED");

console.log("Cloud contract tests OK");
