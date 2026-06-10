const assert = require("assert");

const storage = {};

global.wx = {
  getSystemInfoSync() {
    return { platform: "devtools" };
  },
  getStorageSync(key) {
    return storage[key];
  },
  setStorageSync(key, value) {
    storage[key] = value;
  }
};

const { ensureOk } = require("../miniprogram/services/api-client");
const {
  getAdminConfig,
  getMemberForRole,
  saveAdminConfig,
  setMemberRole
} = require("../miniprogram/services/admin-service");
const { getMemberCode } = require("../miniprogram/services/member-service");
const { getAvailableModes, getConfigurableMatchSetup } = require("../miniprogram/services/match-service");
const {
  deductMemberPoints,
  getMemberForExchange,
  getStaffDeskData,
  updateTableDueTime,
  voidAbnormalMatch
} = require("../miniprogram/services/staff-service");
const { getScreenBoard } = require("../miniprogram/services/screen-service");
const { parseMemberOpenid } = require("../miniprogram/utils/member-code-parser");

async function main() {
  const adminConfig = ensureOk(getAdminConfig());
  adminConfig.points.tableOpenBonus = 45;
  adminConfig.screen.storeBoard = "门店天梯榜";
  adminConfig.modes[0].baseOptions = [25, 50, 75];
  adminConfig.modes[0].multipliers = [1, 2, 4];

  ensureOk(await saveAdminConfig(adminConfig));

  const savedConfig = ensureOk(getAdminConfig());
  assert.strictEqual(savedConfig.points.tableOpenBonus, 45);
  assert.strictEqual(savedConfig.screen.storeBoard, "门店天梯榜");

  assert.strictEqual(parseMemberOpenid('{"openid":"member-001"}'), "member-001");
  assert.strictEqual(parseMemberOpenid("https://club.test/member?openid=member-002"), "member-002");
  assert.strictEqual(parseMemberOpenid("openid:member-003"), "member-003");

  const roleMember = ensureOk(await getMemberForRole({ openid: "staff-member" }));
  assert.strictEqual(roleMember.role, "player");

  const updatedRoleMember = ensureOk(await setMemberRole({
    openid: roleMember.openid,
    targetRole: "staff",
    name: roleMember.name
  }));
  assert.strictEqual(updatedRoleMember.role, "staff");

  const screenRoleMember = ensureOk(await setMemberRole({
    openid: roleMember.openid,
    targetRole: "screen",
    name: roleMember.name
  }));
  assert.strictEqual(screenRoleMember.role, "screen");

  const availableModes = ensureOk(await getAvailableModes());
  assert.deepStrictEqual(availableModes[0].baseOptions, [25, 50, 75]);

  const configurableSetup = ensureOk(await getConfigurableMatchSetup({ modeId: "race5" }));
  assert.strictEqual(configurableSetup.selectedBase, 50);
  assert.strictEqual(configurableSetup.selectedMultiplier, 1);
  assert.strictEqual(configurableSetup.riskPoints, 50);

  const screenBoard = ensureOk(await getScreenBoard());
  assert.strictEqual(screenBoard.screenConfig.storeBoard, "门店天梯榜");

  const deskData = ensureOk(getStaffDeskData());
  const selectedTable = deskData.staffTables[0];
  const dueResult = ensureOk(await updateTableDueTime({
    tables: deskData.staffTables,
    tableId: selectedTable.id,
    dueTime: "23:45"
  }));

  assert.strictEqual(dueResult.selectedTable.dueTime, "23:45");
  assert.strictEqual(ensureOk(getStaffDeskData()).staffTables[0].dueTime, "23:45");

  const bonusDueResult = ensureOk(await updateTableDueTime({
    tables: dueResult.staffTables,
    tableId: selectedTable.id,
    dueTime: "23:50",
    memberOpenid: "local-member"
  }));

  assert.strictEqual(bonusDueResult.tableBonus.granted, true);
  assert.strictEqual(bonusDueResult.tableBonus.bonusPoints, 30);

  const member = ensureOk(await getMemberForExchange({ openid: "local-member" }));
  assert.ok(member.name);
  assert.ok(member.points > 0);

  const deductResult = ensureOk(await deductMemberPoints({
    openid: member.openid,
    userName: member.name,
    points: 100
  }));
  assert.strictEqual(deductResult.points, 100);

  const abnormal = ensureOk(getStaffDeskData()).abnormalMatches[0];
  const voidResult = ensureOk(await voidAbnormalMatch({
    matchId: abnormal.id,
    tableNo: abnormal.tableNo
  }));
  assert.strictEqual(voidResult.matchId, abnormal.id);
  assert.strictEqual(ensureOk(getStaffDeskData()).abnormalMatches.some((item) => item.id === abnormal.id), false);

  const memberCode = ensureOk(await getMemberCode());
  assert.strictEqual(memberCode.qrCodeDataUrl, "");
  assert.strictEqual(memberCode.codeCells.length, 49);
  assert.ok(memberCode.codeText.startsWith("YH-"));

  console.log("Ops service fallback tests OK");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
