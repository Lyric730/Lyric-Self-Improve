const { callCloud, ensureOk, success } = require("./api-client");
const { staffTables, abnormalMatches, staffExchangeUser } = require("../utils/ladder-data");
const { isDevtoolsPreview } = require("../utils/dev-preview");

const STAFF_TABLES_STORAGE_KEY = "yunhan_staff_tables";
const ABNORMAL_MATCHES_STORAGE_KEY = "yunhan_abnormal_matches";

let currentStaffTables = staffTables.map((table) => ({ ...table }));
let currentAbnormalMatches = abnormalMatches.map((match) => ({ ...match }));

function canUseStorage() {
  return typeof wx !== "undefined" && wx && wx.getStorageSync && wx.setStorageSync;
}

function readStorage(key, fallback) {
  if (!canUseStorage()) {
    return fallback;
  }

  try {
    const storedValue = wx.getStorageSync(key);

    return Array.isArray(storedValue) ? storedValue : fallback;
  } catch (error) {
    return fallback;
  }
}

function writeStorage(key, value) {
  if (!canUseStorage()) {
    return;
  }

  try {
    wx.setStorageSync(key, value);
  } catch (error) {
    // Local preview storage should not block the front-desk workflow.
  }
}

async function callStaffCloud(action, payload) {
  const result = await callCloud("staff", action, payload);

  if (!result.ok && isDevtoolsPreview()) {
    return success({});
  }

  return result;
}

function getStaffDeskData() {
  currentStaffTables = readStorage(STAFF_TABLES_STORAGE_KEY, currentStaffTables);
  currentAbnormalMatches = readStorage(ABNORMAL_MATCHES_STORAGE_KEY, currentAbnormalMatches);

  return success({
    staffTables: currentStaffTables,
    abnormalMatches: currentAbnormalMatches
  });
}

async function getMemberForExchange(params) {
  const result = await callCloud("staff", "getMemberForExchange", {
    openid: params.openid,
    storeId: params.storeId || "default"
  });

  if (!result.ok && isDevtoolsPreview()) {
    return success({
      openid: params.openid,
      name: staffExchangeUser.name,
      points: staffExchangeUser.points,
      lastVisit: staffExchangeUser.lastVisit
    });
  }

  const member = ensureOk(result);

  return success(member);
}

async function updateTableDueTime(params) {
  ensureOk(await callStaffCloud("updateTableDueTime", {
    tableId: params.tableId,
    dueTime: params.dueTime,
    storeId: params.storeId || "default"
  }));

  const nextTables = params.tables.map((table) => {
    if (table.id !== params.tableId) {
      return table;
    }

    return {
      ...table,
      dueTime: params.dueTime
    };
  });

  currentStaffTables = nextTables;
  writeStorage(STAFF_TABLES_STORAGE_KEY, nextTables);

  return success({
    staffTables: nextTables,
    selectedTable: nextTables.find((table) => table.id === params.tableId)
  });
}

async function deductMemberPoints(params) {
  ensureOk(await callStaffCloud("deductMemberPoints", {
    openid: params.openid || "",
    userName: params.userName,
    points: params.points,
    storeId: params.storeId || "default"
  }));

  return success({
    points: params.points
  });
}

async function voidAbnormalMatch(params) {
  ensureOk(await callStaffCloud("voidAbnormalMatch", {
    matchId: params.matchId,
    tableNo: params.tableNo,
    storeId: params.storeId || "default"
  }));

  currentAbnormalMatches = currentAbnormalMatches.filter((match) => match.id !== params.matchId);
  writeStorage(ABNORMAL_MATCHES_STORAGE_KEY, currentAbnormalMatches);

  return success({
    matchId: params.matchId
  });
}

module.exports = {
  deductMemberPoints,
  getMemberForExchange,
  getStaffDeskData,
  updateTableDueTime,
  voidAbnormalMatch
};
