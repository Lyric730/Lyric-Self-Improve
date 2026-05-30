const { callCloud, ensureOk, success } = require("./api-client");
const { staffTables, abnormalMatches } = require("../utils/ladder-data");

function getStaffDeskData() {
  return success({
    staffTables,
    abnormalMatches
  });
}

async function getMemberForExchange(params) {
  const member = ensureOk(await callCloud("staff", "getMemberForExchange", {
    openid: params.openid,
    storeId: params.storeId || "default"
  }));

  return success(member);
}

async function updateTableDueTime(params) {
  ensureOk(await callCloud("staff", "updateTableDueTime", {
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

  return success({
    staffTables: nextTables,
    selectedTable: nextTables.find((table) => table.id === params.tableId)
  });
}

async function deductMemberPoints(params) {
  ensureOk(await callCloud("staff", "deductMemberPoints", {
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
  ensureOk(await callCloud("staff", "voidAbnormalMatch", {
    matchId: params.matchId,
    tableNo: params.tableNo,
    storeId: params.storeId || "default"
  }));

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
