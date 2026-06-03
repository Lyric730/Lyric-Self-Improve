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
const { getAdminConfig, saveAdminConfig } = require("../miniprogram/services/admin-service");
const { getMemberCode } = require("../miniprogram/services/member-service");
const {
  deductMemberPoints,
  getMemberForExchange,
  getStaffDeskData,
  updateTableDueTime,
  voidAbnormalMatch
} = require("../miniprogram/services/staff-service");
const { getScreenBoard } = require("../miniprogram/services/screen-service");

async function main() {
  const adminConfig = ensureOk(getAdminConfig());
  adminConfig.points.tableOpenBonus = 45;
  adminConfig.screen.storeBoard = "门店天梯榜";

  ensureOk(await saveAdminConfig(adminConfig));

  const savedConfig = ensureOk(getAdminConfig());
  assert.strictEqual(savedConfig.points.tableOpenBonus, 45);
  assert.strictEqual(savedConfig.screen.storeBoard, "门店天梯榜");

  const screenBoard = ensureOk(getScreenBoard());
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
