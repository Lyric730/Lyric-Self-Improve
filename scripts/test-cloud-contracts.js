const assert = require("assert");

const miniAdmin = require("../miniprogram/utils/admin-config-validator");
const cloudAdmin = require("../cloudfunctions/yunhanApi/admin-config-validator");
const miniMember = require("../miniprogram/utils/member-profile");
const cloudMember = require("../cloudfunctions/yunhanApi/member-profile");
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

console.log("Cloud contract tests OK");
