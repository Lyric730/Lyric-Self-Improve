const assert = require("node:assert/strict");

const {
  parseRewardRange,
  validateAdminConfig
} = require("../miniprogram/utils/admin-config-validator");
const { adminConfig } = require("../miniprogram/utils/ladder-data");

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function assertInvalid(config, expectedText) {
  const result = validateAdminConfig(config);

  assert.equal(result.ok, false);
  assert.ok(
    result.errors.some((message) => message.includes(expectedText)),
    `Expected validation error containing "${expectedText}", got ${result.errors.join(" / ")}`
  );
}

{
  const result = validateAdminConfig(clone(adminConfig));

  assert.equal(result.ok, true);
  assert.deepEqual(result.errors, []);
}

{
  assert.deepEqual(parseRewardRange("10 ~ 20"), { min: 10, max: 20 });
  assert.deepEqual(parseRewardRange("50-100 分"), { min: 50, max: 100 });
  assert.equal(parseRewardRange("高额随机"), null);
}

{
  const config = clone(adminConfig);
  config.modes[0].baseOptions = [];

  assertInvalid(config, "底分不能为空");
}

{
  const config = clone(adminConfig);
  config.modes[0].normalReward = "30 ~ 10";

  assertInvalid(config, "最小值不能大于最大值");
}

{
  const config = clone(adminConfig);
  config.modes.push({
    modeId: "race9",
    name: "抢9",
    targetWins: 9,
    minimumMinutes: 90,
    baseOptions: [100],
    multipliers: [1],
    normalReward: "10 ~ 20",
    sprintReward: "30 ~ 50",
    starReward: 1,
    enabled: true
  });

  assertInvalid(config, "抢9当前不开放");
}

{
  const config = clone(adminConfig);
  config.points.exchangeThreshold = 0;

  assertInvalid(config, "兑换门槛");
}

{
  const config = clone(adminConfig);
  config.antiCheat.geoFence = "0 米";

  assertInvalid(config, "店内定位范围");
}

{
  const config = clone(adminConfig);
  config.antiCheat.storeLatitude = "30.5928";
  config.antiCheat.storeLongitude = "114.3055";

  const result = validateAdminConfig(config);

  assert.equal(result.ok, true);
}

{
  const config = clone(adminConfig);
  config.antiCheat.storeLatitude = "999";
  config.antiCheat.storeLongitude = "114.3055";

  assertInvalid(config, "门店纬度");
}

{
  const config = clone(adminConfig);
  config.screen.refreshText = "5 秒刷新";

  assertInvalid(config, "刷新间隔");
}

console.log("Admin config validator tests OK");
