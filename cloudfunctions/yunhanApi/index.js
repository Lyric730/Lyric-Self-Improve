const cloud = require("wx-server-sdk");
const QRCode = require("qrcode");
const { assertValidAdminConfig } = require("./admin-config-validator");
const { assertValidMemberProfile } = require("./member-profile");
const { DEFAULT_MODES } = require("./settlement-engine");
const { buildSettlementPreview, buildSettlementWritePlan } = require("./match-settlement");

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

const DEFAULT_POINTS_CONFIG = {
  newUser: 300,
  tableOpenBonus: 30,
  exchangeThreshold: 1000
};

function ok(data = {}) {
  return {
    ok: true,
    data
  };
}

function fail(message, code = "REQUEST_FAILED") {
  return {
    ok: false,
    code,
    message
  };
}

function getWxContext() {
  return cloud.getWXContext();
}

function getStoreId(event) {
  return event.storeId || (event.payload && event.payload.storeId) || "default";
}

async function getMemberRole(openid, storeId) {
  if (!openid) {
    return "anonymous";
  }

  try {
    const result = await db.collection("store_members")
      .where({
        openid,
        storeId,
        status: "active"
      })
      .limit(1)
      .get();
    const member = result.data && result.data.length > 0 ? result.data[0] : null;

    return member && member.role ? member.role : "player";
  } catch (error) {
    return "player";
  }
}

async function getExistingOwner(storeId) {
  const result = await db.collection("store_members")
    .where({
      storeId,
      role: "owner",
      status: "active"
    })
    .limit(1)
    .get();

  return result.data && result.data.length > 0 ? result.data[0] : null;
}

function roleAllowed(role, allowedRoles) {
  if (role === "owner") {
    return true;
  }

  return allowedRoles.includes(role);
}

async function assertRole(wxContext, allowedRoles, storeId) {
  const role = await getMemberRole(wxContext.OPENID, storeId);

  if (!roleAllowed(role, allowedRoles)) {
    const error = new Error("PERMISSION_DENIED");
    error.code = "PERMISSION_DENIED";
    throw error;
  }

  return role;
}

async function handleBootstrapOwner(event, wxContext) {
  const payload = event.payload || {};
  const storeId = getStoreId(event);
  const expectedSecret = process.env.BOOTSTRAP_OWNER_SECRET;

  if (!expectedSecret) {
    return fail("未配置初始化密钥", "BOOTSTRAP_SECRET_NOT_CONFIGURED");
  }

  if (payload.bootstrapSecret !== expectedSecret) {
    return fail("初始化密钥不正确", "BOOTSTRAP_SECRET_INVALID");
  }

  const existingOwner = await getExistingOwner(storeId);

  if (existingOwner) {
    return fail("当前门店已存在老板账号", "OWNER_ALREADY_EXISTS");
  }

  await db.collection("store_members").add({
    data: {
      storeId,
      openid: wxContext.OPENID,
      role: "owner",
      status: "active",
      nickname: payload.nickname || "门店老板",
      createdAt: db.serverDate(),
      updatedAt: db.serverDate()
    }
  });

  let operationLogged = true;

  try {
    await writeOperationLog({
      module: "auth",
      action: "bootstrapOwner",
      payload: {
        storeId
      },
      role: "owner",
      storeId,
      operatorOpenid: wxContext.OPENID
    });
  } catch (error) {
    operationLogged = false;
  }

  return ok({
    openid: wxContext.OPENID,
    role: "owner",
    storeId,
    operationLogged
  });
}

async function writeOperationLog(params) {
  return db.collection("operation_logs").add({
    data: {
      module: params.module,
      action: params.action,
      payload: params.payload || {},
      role: params.role,
      storeId: params.storeId,
      operatorOpenid: params.operatorOpenid,
      createdAt: db.serverDate()
    }
  });
}

function requirePayloadValue(payload, key, message, code) {
  if (!payload || payload[key] === undefined || payload[key] === null || payload[key] === "") {
    const error = new Error(message);
    error.code = code;
    throw error;
  }
}

function isFailureResult(result) {
  return result && result.ok === false;
}

async function upsertOne(collectionName, query, data) {
  const result = await db.collection(collectionName)
    .where(query)
    .limit(1)
    .get();
  const existing = result.data && result.data.length > 0 ? result.data[0] : null;

  if (existing) {
    await db.collection(collectionName).doc(existing._id).update({
      data: {
        ...data,
        updatedAt: db.serverDate()
      }
    });

    return "updated";
  }

  await db.collection(collectionName).add({
    data: {
      ...query,
      ...data,
      createdAt: db.serverDate(),
      updatedAt: db.serverDate()
    }
  });

  return "created";
}

async function updateTableDueTime(payload, storeId, operatorOpenid) {
  requirePayloadValue(payload, "tableId", "请选择球桌", "TABLE_ID_REQUIRED");
  requirePayloadValue(payload, "dueTime", "请选择到点时间", "DUE_TIME_REQUIRED");

  const writeMode = await upsertOne(
    "table_sessions",
    {
      storeId,
      tableId: payload.tableId,
      status: "active"
    },
    {
      dueTime: payload.dueTime,
      updatedBy: operatorOpenid
    }
  );

  return {
    tableId: payload.tableId,
    dueTime: payload.dueTime,
    writeMode
  };
}

async function getMemberForExchange(payload, storeId) {
  requirePayloadValue(payload, "openid", "请先选择会员", "MEMBER_OPENID_REQUIRED");

  const accountResult = await db.collection("member_points")
    .where({
      storeId,
      openid: payload.openid
    })
    .limit(1)
    .get();
  const account = accountResult.data && accountResult.data.length > 0 ? accountResult.data[0] : null;

  if (!account) {
    return fail("会员积分账户不存在", "POINT_ACCOUNT_NOT_FOUND");
  }

  return {
    openid: payload.openid,
    name: account.nickname || account.name || "会员",
    points: Number(account.balance || 0)
  };
}

async function deductMemberPoints(payload, storeId, operatorOpenid) {
  requirePayloadValue(payload, "openid", "请先选择会员", "MEMBER_OPENID_REQUIRED");

  const points = Number(payload.points);

  if (!Number.isFinite(points) || points <= 0) {
    return fail("核销积分必须大于 0", "INVALID_POINTS");
  }

  const accountResult = await db.collection("member_points")
    .where({
      storeId,
      openid: payload.openid
    })
    .limit(1)
    .get();
  const account = accountResult.data && accountResult.data.length > 0 ? accountResult.data[0] : null;

  if (!account) {
    return fail("会员积分账户不存在", "POINT_ACCOUNT_NOT_FOUND");
  }

  const currentBalance = Number(account.balance || 0);

  if (currentBalance < points) {
    return fail("会员积分不足", "POINT_BALANCE_NOT_ENOUGH");
  }

  const balanceAfter = currentBalance - points;

  await db.collection("member_points").doc(account._id).update({
    data: {
      balance: balanceAfter,
      updatedAt: db.serverDate()
    }
  });

  await db.collection("points_ledger").add({
    data: {
      storeId,
      openid: payload.openid,
      matchId: "",
      type: "exchange",
      delta: -points,
      balanceAfter,
      operatorOpenid,
      createdAt: db.serverDate()
    }
  });

  return {
    openid: payload.openid,
    points,
    balanceAfter
  };
}

async function voidAbnormalMatch(payload, storeId, operatorOpenid) {
  requirePayloadValue(payload, "matchId", "请选择要作废的比赛", "MATCH_ID_REQUIRED");

  const matchResult = await db.collection("matches")
    .where({
      _id: payload.matchId,
      storeId
    })
    .limit(1)
    .get();
  const match = matchResult.data && matchResult.data.length > 0 ? matchResult.data[0] : null;

  if (!match) {
    return fail("比赛不存在或已无法作废", "MATCH_NOT_FOUND");
  }

  const updateResult = await db.collection("matches").doc(match._id).update({
    data: {
      status: "voided",
      voidedBy: operatorOpenid,
      voidReason: payload.reason || "staff_void",
      updatedAt: db.serverDate()
    }
  });

  if (!updateResult.stats || updateResult.stats.updated < 1) {
    return fail("比赛状态更新失败", "MATCH_UPDATE_FAILED");
  }

  return {
    matchId: payload.matchId,
    status: "voided"
  };
}

async function saveAdminConfig(payload, storeId, operatorOpenid) {
  requirePayloadValue(payload, "config", "缺少门店配置", "ADMIN_CONFIG_REQUIRED");

  const config = assertValidAdminConfig(payload.config);

  const writeMode = await upsertOne(
    "admin_configs",
    {
      storeId
    },
    {
      config,
      updatedBy: operatorOpenid
    }
  );

  return {
    storeId,
    writeMode
  };
}

async function saveMemberProfile(payload, storeId, openid) {
  const profile = assertValidMemberProfile(payload.profile || payload);
  const memberResult = await db.collection("store_members")
    .where({
      storeId,
      openid
    })
    .limit(1)
    .get();
  const member = memberResult.data && memberResult.data.length > 0 ? memberResult.data[0] : null;

  if (member) {
    await db.collection("store_members").doc(member._id).update({
      data: {
        nickname: profile.name,
        phone: profile.phone,
        note: profile.note,
        avatarUrl: profile.avatarUrl,
        updatedAt: db.serverDate()
      }
    });
  } else {
    await db.collection("store_members").add({
      data: {
        storeId,
        openid,
        role: "player",
        status: "active",
        nickname: profile.name,
        phone: profile.phone,
        note: profile.note,
        avatarUrl: profile.avatarUrl,
        createdAt: db.serverDate(),
        updatedAt: db.serverDate()
      }
    });
  }

  const pointsResult = await db.collection("member_points")
    .where({
      storeId,
      openid
    })
    .limit(1)
    .get();
  const pointsAccount = pointsResult.data && pointsResult.data.length > 0 ? pointsResult.data[0] : null;

  if (pointsAccount) {
    await db.collection("member_points").doc(pointsAccount._id).update({
      data: {
        nickname: profile.name,
        name: profile.name,
        phone: profile.phone,
        note: profile.note,
        avatarUrl: profile.avatarUrl,
        updatedAt: db.serverDate()
      }
    });
  }

  return profile;
}

async function getPointAccountDoc(openid, storeId) {
  const accountResult = await db.collection("member_points")
    .where({
      storeId,
      openid
    })
    .limit(1)
    .get();

  return accountResult.data && accountResult.data.length > 0 ? accountResult.data[0] : null;
}

async function preparePointAccountUpdates(pointChanges, storeId) {
  const rows = [];

  for (const change of pointChanges) {
    const account = await getPointAccountDoc(change.openid, storeId);

    if (!account) {
      return fail("积分账户不存在", "POINT_ACCOUNT_NOT_FOUND", {
        openid: change.openid
      });
    }

    const currentBalance = Number(account.balance || 0);
    const balanceAfter = currentBalance + Number(change.delta || 0);

    if (balanceAfter < 0) {
      return fail("积分余额不足，无法结算", "POINT_BALANCE_NOT_ENOUGH", {
        openid: change.openid,
        currentBalance,
        delta: change.delta
      });
    }

    rows.push({
      account,
      change,
      currentBalance,
      balanceAfter
    });
  }

  return {
    ok: true,
    rows
  };
}

async function applyPointAccountUpdates(rows, storeId, operatorOpenid) {
  const balances = [];

  for (const row of rows) {
    await db.collection("member_points").doc(row.account._id).update({
      data: {
        balance: row.balanceAfter,
        updatedAt: db.serverDate()
      }
    });

    await db.collection("points_ledger").add({
      data: {
        storeId,
        openid: row.change.openid,
        matchId: row.change.matchId,
        type: row.change.type,
        delta: row.change.delta,
        balanceAfter: row.balanceAfter,
        riskPoints: row.change.riskPoints,
        rewardValue: row.change.rewardValue,
        rewardPhase: row.change.rewardPhase,
        operatorOpenid,
        createdAt: db.serverDate()
      }
    });

    balances.push({
      openid: row.change.openid,
      side: row.change.side,
      result: row.change.result,
      delta: row.change.delta,
      balanceAfter: row.balanceAfter
    });
  }

  return balances;
}

function buildRoomNo(tableNo) {
  const safeTableNo = String(tableNo || "T00").replace(/\s+/g, "").toUpperCase();
  const suffix = String(Date.now()).slice(-6);

  return `YH-${safeTableNo}-${suffix}`;
}

function getShortName(name, fallback = "我") {
  const value = String(name || "").trim();

  return value ? value.slice(-1) : fallback;
}

async function getMemberSnapshot(openid, storeId) {
  if (!openid) {
    return {
      name: "当前会员",
      shortName: "我",
      rankTitle: "会员"
    };
  }

  try {
    const result = await db.collection("store_members")
      .where({
        openid,
        storeId,
        status: "active"
      })
      .limit(1)
      .get();
    const member = result.data && result.data.length > 0 ? result.data[0] : null;
    const name = member && (member.nickname || member.name) ? (member.nickname || member.name) : "当前会员";

    return {
      name,
      shortName: getShortName(name),
      rankTitle: member && member.rankTitle ? member.rankTitle : "会员"
    };
  } catch (error) {
    return {
      name: "当前会员",
      shortName: "我",
      rankTitle: "会员"
    };
  }
}

function formatRoomState(match, hostSnapshot, guestSnapshot) {
  const opponentJoined = Boolean(match.guestOpenid);

  return {
    matchId: match._id || match.matchId || "",
    roomNo: match.roomNo || match._id || "",
    tableNo: match.tableNo || "",
    dueTime: match.dueTime || "",
    status: match.status || "waiting",
    statusText: opponentJoined ? "对手已加入" : "等待对手加入",
    statusHint: opponentJoined ? "双方确认后进入玩法选择" : "让对手扫描球桌码加入本场挑战",
    expiresText: "房间 10 分钟内有效",
    opponentJoined,
    setup: match.modeId ? {
      modeId: match.modeId,
      selectedBase: Number(match.base || 0),
      selectedMultiplier: Number(match.multiplier || 0),
      riskPoints: Number(match.riskPoints || 0),
      targetWins: Number(match.targetWins || 0),
      minimumMinutes: Number(match.minimumMinutes || 0)
    } : null,
    host: hostSnapshot || {
      name: "当前会员",
      shortName: "我",
      rankTitle: "会员"
    },
    guest: opponentJoined ? (guestSnapshot || {
      name: opponentJoined ? "对手" : "",
      shortName: opponentJoined ? "客" : "",
      rankTitle: opponentJoined ? "会员" : ""
    }) : null
  };
}

async function createMatchRoom(payload, storeId, hostOpenid) {
  requirePayloadValue(payload, "tableNo", "请选择球桌", "TABLE_NO_REQUIRED");

  const roomNo = buildRoomNo(payload.tableNo);
  const matchData = {
    storeId,
    roomNo,
    tableNo: payload.tableNo,
    dueTime: payload.dueTime || "",
    openedAt: payload.openedAt || "",
    hostOpenid,
    guestOpenid: "",
    status: "waiting",
    source: "miniapp",
    createdAt: db.serverDate(),
    updatedAt: db.serverDate()
  };
  const addResult = await db.collection("matches").add({
    data: matchData
  });
  const hostSnapshot = await getMemberSnapshot(hostOpenid, storeId);
  const match = {
    _id: addResult._id,
    ...matchData
  };

  return {
    matchId: addResult._id,
    roomState: formatRoomState(match, hostSnapshot)
  };
}

async function getMatchRoom(payload, storeId) {
  requirePayloadValue(payload, "matchId", "请选择比赛房间", "MATCH_ID_REQUIRED");

  const result = await db.collection("matches")
    .where({
      _id: payload.matchId,
      storeId
    })
    .limit(1)
    .get();
  const match = result.data && result.data.length > 0 ? result.data[0] : null;

  if (!match) {
    return fail("比赛房间不存在", "MATCH_NOT_FOUND");
  }

  const hostSnapshot = await getMemberSnapshot(match.hostOpenid, storeId);
  const guestSnapshot = match.guestOpenid ? await getMemberSnapshot(match.guestOpenid, storeId) : null;

  return {
    matchId: match._id,
    roomState: formatRoomState(match, hostSnapshot, guestSnapshot)
  };
}

async function joinMatchRoom(payload, storeId, guestOpenid) {
  requirePayloadValue(payload, "matchId", "请选择比赛房间", "MATCH_ID_REQUIRED");

  const result = await db.collection("matches")
    .where({
      _id: payload.matchId,
      storeId
    })
    .limit(1)
    .get();
  const match = result.data && result.data.length > 0 ? result.data[0] : null;

  if (!match) {
    return fail("比赛房间不存在", "MATCH_NOT_FOUND");
  }

  if (match.status !== "waiting" && match.status !== "joined") {
    return fail("比赛房间已不可加入", "MATCH_ROOM_CLOSED");
  }

  if (match.hostOpenid === guestOpenid) {
    return fail("不能加入自己发起的房间", "HOST_CANNOT_JOIN");
  }

  if (match.guestOpenid && match.guestOpenid !== guestOpenid) {
    return fail("本房间已有对手加入", "MATCH_ROOM_OCCUPIED");
  }

  if (!match.guestOpenid) {
    const updateResult = await db.collection("matches")
      .where({
        _id: match._id,
        storeId,
        guestOpenid: ""
      })
      .update({
        data: {
          guestOpenid,
          status: "joined",
          updatedAt: db.serverDate()
        }
      });

    if (!updateResult.stats || updateResult.stats.updated === 0) {
      return fail("本房间已有对手加入", "MATCH_ROOM_OCCUPIED");
    }
  }

  const joinedMatch = {
    ...match,
    guestOpenid,
    status: "joined"
  };
  const hostSnapshot = await getMemberSnapshot(joinedMatch.hostOpenid, storeId);
  const guestSnapshot = await getMemberSnapshot(guestOpenid, storeId);

  return {
    matchId: joinedMatch._id,
    roomState: formatRoomState(joinedMatch, hostSnapshot, guestSnapshot)
  };
}

function normalizeConfigMode(mode = {}) {
  return {
    ...mode,
    targetWins: Number(mode.targetWins || 0),
    minimumMinutes: Number(mode.minimumMinutes || 0),
    baseOptions: Array.isArray(mode.baseOptions) ? mode.baseOptions.map(Number) : [],
    multipliers: Array.isArray(mode.multipliers) ? mode.multipliers.map(Number) : [],
    starReward: Number(mode.starReward || 0),
    enabled: mode.enabled !== false
  };
}

async function getStoreModes(storeId) {
  try {
    const result = await db.collection("admin_configs")
      .where({ storeId })
      .limit(1)
      .get();
    const config = result.data && result.data.length > 0 ? result.data[0].config : null;

    if (config && Array.isArray(config.modes) && config.modes.length > 0) {
      return config.modes.map(normalizeConfigMode);
    }
  } catch (error) {
    return DEFAULT_MODES.map(normalizeConfigMode);
  }

  return DEFAULT_MODES.map(normalizeConfigMode);
}

async function getConfigurableMode(modeId, storeId) {
  const modeList = await getStoreModes(storeId);

  return modeList.find((mode) => mode.modeId === modeId) || null;
}

async function configureMatchRoom(payload, storeId, operatorOpenid) {
  requirePayloadValue(payload, "matchId", "请选择比赛房间", "MATCH_ID_REQUIRED");
  requirePayloadValue(payload, "modeId", "请选择玩法", "MODE_REQUIRED");

  const mode = await getConfigurableMode(payload.modeId, storeId);

  if (!mode || mode.enabled === false) {
    return fail("该玩法暂未开放", "MODE_NOT_ENABLED");
  }

  const selectedBase = Number(payload.selectedBase ?? payload.base);
  const selectedMultiplier = Number(payload.selectedMultiplier ?? payload.multiplier);

  if (!mode.baseOptions.includes(selectedBase)) {
    return fail("挑战底分不在当前玩法范围内", "INVALID_BASE_POINTS");
  }

  if (!mode.multipliers.includes(selectedMultiplier)) {
    return fail("积分倍率不在当前玩法范围内", "INVALID_MULTIPLIER");
  }

  const result = await db.collection("matches")
    .where({
      _id: payload.matchId,
      storeId
    })
    .limit(1)
    .get();
  const match = result.data && result.data.length > 0 ? result.data[0] : null;

  if (!match) {
    return fail("比赛房间不存在", "MATCH_NOT_FOUND");
  }

  if (!match.hostOpenid || !match.guestOpenid) {
    return fail("双方到齐后才能确认玩法", "MATCH_PLAYERS_NOT_READY");
  }

  if (match.status !== "joined" && match.status !== "configured") {
    return fail("当前房间状态不能确认玩法", "MATCH_STATUS_INVALID");
  }

  if (operatorOpenid !== match.hostOpenid && operatorOpenid !== match.guestOpenid) {
    return fail("只有本场双方可以确认玩法", "MATCH_PLAYER_REQUIRED");
  }

  const riskPoints = selectedBase * selectedMultiplier;
  const setupData = {
    modeId: mode.modeId,
    base: selectedBase,
    multiplier: selectedMultiplier,
    riskPoints,
    targetWins: mode.targetWins,
    minimumMinutes: mode.minimumMinutes,
    status: "configured",
    configuredAt: db.serverDate(),
    updatedAt: db.serverDate()
  };
  const updateResult = await db.collection("matches").doc(match._id).update({
    data: setupData
  });

  if (!updateResult.stats || updateResult.stats.updated < 1) {
    return fail("比赛参数保存失败", "MATCH_CONFIG_UPDATE_FAILED");
  }

  const configuredMatch = {
    ...match,
    ...setupData
  };
  const hostSnapshot = await getMemberSnapshot(configuredMatch.hostOpenid, storeId);
  const guestSnapshot = await getMemberSnapshot(configuredMatch.guestOpenid, storeId);

  return {
    matchId: configuredMatch._id,
    setup: {
      modeId: mode.modeId,
      selectedBase,
      selectedMultiplier,
      riskPoints,
      mode: {
        modeId: mode.modeId,
        name: mode.name,
        targetWins: mode.targetWins,
        minimumMinutes: mode.minimumMinutes,
        starReward: mode.starReward,
        normalReward: mode.normalReward,
        sprintReward: mode.sprintReward
      }
    },
    roomState: formatRoomState(configuredMatch, hostSnapshot, guestSnapshot)
  };
}

function buildCloudSettlementPayload(payload, match) {
  return {
    ...payload,
    ...match,
    matchId: payload.matchId,
    playerAOpenid: match.hostOpenid || payload.playerAOpenid,
    playerBOpenid: match.guestOpenid || payload.playerBOpenid,
    selectedBase: match.base || payload.selectedBase || payload.base,
    selectedMultiplier: match.multiplier || payload.selectedMultiplier || payload.multiplier
  };
}

async function getMatchForSettlement(payload, storeId) {
  requirePayloadValue(payload, "matchId", "请选择要结算的比赛", "MATCH_ID_REQUIRED");

  const matchResult = await db.collection("matches")
    .where({
      _id: payload.matchId,
      storeId
    })
    .limit(1)
    .get();
  const match = matchResult.data && matchResult.data.length > 0 ? matchResult.data[0] : null;

  if (!match) {
    return fail("比赛不存在或已无法结算", "MATCH_NOT_FOUND");
  }

  if (match.status === "settled") {
    return fail("比赛已结算，不能重复结算", "MATCH_ALREADY_SETTLED");
  }

  return {
    match
  };
}

async function previewMatchSettlement(payload, storeId) {
  const matchResult = await getMatchForSettlement(payload, storeId);

  if (isFailureResult(matchResult)) {
    return matchResult;
  }

  const preview = buildSettlementPreview(buildCloudSettlementPayload(payload, matchResult.match));

  if (!preview.ok) {
    return preview;
  }

  const accountUpdates = await preparePointAccountUpdates(preview.pointChanges, storeId);

  if (isFailureResult(accountUpdates)) {
    return accountUpdates;
  }

  return {
    matchId: preview.matchId,
    settlement: preview.settlement,
    rankChanges: preview.rankChanges,
    balancesPreview: accountUpdates.rows.map((row) => ({
      openid: row.change.openid,
      side: row.change.side,
      result: row.change.result,
      delta: row.change.delta,
      balanceAfter: row.balanceAfter
    }))
  };
}

async function settleMatch(payload, storeId, operatorOpenid) {
  const matchResult = await getMatchForSettlement(payload, storeId);

  if (isFailureResult(matchResult)) {
    return matchResult;
  }

  const existingSettlementResult = await db.collection("settlements")
    .where({
      storeId,
      matchId: payload.matchId
    })
    .limit(1)
    .get();
  const existingSettlement = existingSettlementResult.data && existingSettlementResult.data.length > 0
    ? existingSettlementResult.data[0]
    : null;

  if (existingSettlement) {
    return fail("比赛已存在结算记录", "MATCH_ALREADY_SETTLED");
  }

  const plan = buildSettlementWritePlan(buildCloudSettlementPayload(payload, matchResult.match));

  if (!plan.ok) {
    return plan;
  }

  const accountUpdates = await preparePointAccountUpdates(plan.pointChanges, storeId);

  if (isFailureResult(accountUpdates)) {
    return accountUpdates;
  }

  const settlementAddResult = await db.collection("settlements").add({
    data: {
      storeId,
      matchId: plan.matchId,
      status: "settling",
      winnerSide: plan.settlement.winnerSide,
      loserSide: plan.settlement.loserSide,
      riskPoints: plan.settlement.riskPoints,
      rewardValue: plan.settlement.rewardValue,
      rewardPhase: plan.settlement.rewardPhase,
      winnerDelta: plan.settlement.winnerDelta,
      loserDelta: plan.settlement.loserDelta,
      scoreA: plan.settlement.scoreA,
      scoreB: plan.settlement.scoreB,
      elapsedSeconds: plan.settlement.elapsedSeconds,
      pointChanges: plan.pointChanges,
      rankChanges: plan.rankChanges,
      settledBy: operatorOpenid,
      createdAt: db.serverDate(),
      updatedAt: db.serverDate()
    }
  });
  const settlementDocId = settlementAddResult._id;
  const balances = await applyPointAccountUpdates(accountUpdates.rows, storeId, operatorOpenid);

  await db.collection("settlements").doc(settlementDocId).update({
    data: {
      status: "settled",
      balances,
      updatedAt: db.serverDate()
    }
  });

  await db.collection("matches").doc(matchResult.match._id).update({
    data: {
      status: "settled",
      settlementSummary: {
        winnerSide: plan.settlement.winnerSide,
        winnerDelta: plan.settlement.winnerDelta,
        loserDelta: plan.settlement.loserDelta,
        rewardValue: plan.settlement.rewardValue
      },
      updatedAt: db.serverDate()
    }
  });

  return {
    matchId: plan.matchId,
    settlement: plan.settlement,
    balances,
    rankChanges: plan.rankChanges
  };
}

async function getSettlement(payload, storeId) {
  requirePayloadValue(payload, "matchId", "请选择要查看的结算记录", "MATCH_ID_REQUIRED");

  const settlementResult = await db.collection("settlements")
    .where({
      storeId,
      matchId: payload.matchId
    })
    .limit(1)
    .get();
  const settlement = settlementResult.data && settlementResult.data.length > 0 ? settlementResult.data[0] : null;

  if (!settlement) {
    return fail("结算记录不存在", "SETTLEMENT_NOT_FOUND");
  }

  return {
    matchId: payload.matchId,
    settlement
  };
}

async function getStorePointsConfig(storeId) {
  const configResult = await db.collection("admin_configs")
    .where({
      storeId
    })
    .limit(1)
    .get();
  const configDoc = configResult.data && configResult.data.length > 0 ? configResult.data[0] : null;
  const points = configDoc && configDoc.config && configDoc.config.points ? configDoc.config.points : {};

  return {
    ...DEFAULT_POINTS_CONFIG,
    ...points
  };
}

async function ensureMemberPointAccount(openid, storeId) {
  const accountResult = await db.collection("member_points")
    .where({
      storeId,
      openid
    })
    .limit(1)
    .get();
  const account = accountResult.data && accountResult.data.length > 0 ? accountResult.data[0] : null;

  if (account) {
    return {
      balance: Number(account.balance || 0),
      created: false
    };
  }

  const pointsConfig = await getStorePointsConfig(storeId);
  const initialPoints = Number(pointsConfig.newUser || 0);

  await db.collection("member_points").add({
    data: {
      storeId,
      openid,
      balance: initialPoints,
      createdAt: db.serverDate(),
      updatedAt: db.serverDate()
    }
  });

  await db.collection("points_ledger").add({
    data: {
      storeId,
      openid,
      matchId: "",
      type: "initial",
      delta: initialPoints,
      balanceAfter: initialPoints,
      createdAt: db.serverDate()
    }
  });

  return {
    balance: initialPoints,
    created: true
  };
}

async function handleAuth(event) {
  const wxContext = getWxContext();

  if (event.action === "bootstrapOwner") {
    return handleBootstrapOwner(event, wxContext);
  }

  const storeId = getStoreId(event);
  const role = await getMemberRole(wxContext.OPENID, storeId);

  return ok({
    openid: wxContext.OPENID,
    unionid: wxContext.UNIONID || "",
    appid: wxContext.APPID,
    role,
    storeId
  });
}

async function handleMatch(event) {
  const wxContext = getWxContext();
  const storeId = getStoreId(event);

  if (event.action === "get") {
    const payload = event.payload || {};

    if (payload.matchId || event.matchId) {
      await assertRole(wxContext, ["player", "staff", "owner"], storeId);
      const result = await getMatchRoom({
        ...payload,
        matchId: payload.matchId || event.matchId
      }, storeId);

      if (isFailureResult(result)) {
        return result;
      }

      return ok({
        action: event.action,
        ...result
      });
    }

    return ok({
      matchId: event.matchId || "",
      status: "waiting"
    });
  }

  if (event.action === "createRoom") {
    const role = await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await createMatchRoom(payload, storeId, wxContext.OPENID);

    if (isFailureResult(result)) {
      return result;
    }

    await writeOperationLog({
      module: "match",
      action: event.action,
      payload: {
        tableNo: payload.tableNo,
        dueTime: payload.dueTime || ""
      },
      role,
      storeId,
      operatorOpenid: wxContext.OPENID
    });

    return ok({
      action: event.action,
      ...result
    });
  }

  if (event.action === "joinRoom") {
    const role = await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await joinMatchRoom(payload, storeId, wxContext.OPENID);

    if (isFailureResult(result)) {
      return result;
    }

    await writeOperationLog({
      module: "match",
      action: event.action,
      payload: {
        matchId: result.matchId,
        roomNo: result.roomState.roomNo
      },
      role,
      storeId,
      operatorOpenid: wxContext.OPENID
    });

    return ok({
      action: event.action,
      ...result
    });
  }

  if (event.action === "configure") {
    const role = await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await configureMatchRoom(payload, storeId, wxContext.OPENID);

    if (isFailureResult(result)) {
      return result;
    }

    await writeOperationLog({
      module: "match",
      action: event.action,
      payload: {
        matchId: result.matchId,
        modeId: result.setup.modeId,
        base: result.setup.selectedBase,
        multiplier: result.setup.selectedMultiplier,
        riskPoints: result.setup.riskPoints
      },
      role,
      storeId,
      operatorOpenid: wxContext.OPENID
    });

    return ok({
      action: event.action,
      ...result
    });
  }

  if (event.action === "previewSettlement") {
    await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await previewMatchSettlement(payload, storeId);

    if (isFailureResult(result)) {
      return result;
    }

    return ok({
      action: event.action,
      ...result
    });
  }

  if (event.action === "settle") {
    const role = await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await settleMatch(payload, storeId, wxContext.OPENID);

    if (isFailureResult(result)) {
      return result;
    }

    await writeOperationLog({
      module: "match",
      action: event.action,
      payload: {
        matchId: payload.matchId
      },
      role,
      storeId,
      operatorOpenid: wxContext.OPENID
    });

    return ok({
      action: event.action,
      ...result
    });
  }

  if (event.action === "getSettlement") {
    await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await getSettlement(payload, storeId);

    if (isFailureResult(result)) {
      return result;
    }

    return ok({
      action: event.action,
      ...result
    });
  }

  return fail("暂不支持该比赛操作", "UNKNOWN_MATCH_ACTION");
}

async function handleStaff(event) {
  const wxContext = getWxContext();
  const storeId = getStoreId(event);
  const payload = event.payload || {};
  const role = await assertRole(wxContext, ["staff", "owner"], storeId);
  let result = {};

  if (event.action === "updateTableDueTime") {
    result = await updateTableDueTime(payload, storeId, wxContext.OPENID);
  } else if (event.action === "getMemberForExchange") {
    result = await getMemberForExchange(payload, storeId);
  } else if (event.action === "deductMemberPoints") {
    result = await deductMemberPoints(payload, storeId, wxContext.OPENID);
  } else if (event.action === "voidAbnormalMatch") {
    result = await voidAbnormalMatch(payload, storeId, wxContext.OPENID);
  } else if (event.action !== "ping") {
    return fail("暂不支持该员工操作", "UNKNOWN_STAFF_ACTION");
  }

  if (isFailureResult(result)) {
    return result;
  }

  await writeOperationLog({
    module: "staff",
    action: event.action,
    payload,
    role,
    storeId,
    operatorOpenid: wxContext.OPENID
  });

  return ok({
    action: event.action,
    ...result
  });
}

async function handleAdmin(event) {
  const wxContext = getWxContext();
  const storeId = getStoreId(event);
  const payload = event.payload || {};
  const role = await assertRole(wxContext, ["owner"], storeId);
  let result = {};

  if (event.action === "saveConfig") {
    result = await saveAdminConfig(payload, storeId, wxContext.OPENID);
  } else if (event.action !== "ping") {
    return fail("暂不支持该老板操作", "UNKNOWN_ADMIN_ACTION");
  }

  if (isFailureResult(result)) {
    return result;
  }

  await writeOperationLog({
    module: "admin",
    action: event.action,
    payload,
    role,
    storeId,
    operatorOpenid: wxContext.OPENID
  });

  return ok({
    action: event.action,
    ...result
  });
}

async function handleMember(event) {
  const wxContext = getWxContext();
  const storeId = getStoreId(event);

  if (event.action === "saveProfile") {
    const profile = await saveMemberProfile(event.payload || {}, storeId, wxContext.OPENID);

    return ok({
      profile
    });
  }

  if (event.action !== "getCode") {
    return fail("暂不支持该会员操作", "UNKNOWN_MEMBER_ACTION");
  }

  const account = await ensureMemberPointAccount(wxContext.OPENID, storeId);
  const codePayload = JSON.stringify({
    type: "yunhan-member",
    version: 1,
    storeId,
    openid: wxContext.OPENID
  });
  const qrCodeDataUrl = await QRCode.toDataURL(codePayload, {
    width: 480,
    margin: 1,
    color: {
      dark: "#16110a",
      light: "#fff6e5"
    }
  });

  return ok({
    qrCodeDataUrl,
    storeId,
    points: account.balance,
    accountCreated: account.created
  });
}

async function handleScreen(event) {
  if (!event.screenToken) {
    return fail("缺少大屏访问凭证", "SCREEN_TOKEN_REQUIRED");
  }

  return ok({
    rankingRows: [],
    bountyRows: []
  });
}

exports.main = async (event = {}) => {
  try {
    if (event.module === "auth") {
      return handleAuth(event);
    }

    if (event.module === "match") {
      return handleMatch(event);
    }

    if (event.module === "staff") {
      return handleStaff(event);
    }

    if (event.module === "admin") {
      return handleAdmin(event);
    }

    if (event.module === "member") {
      return handleMember(event);
    }

    if (event.module === "screen") {
      return handleScreen(event);
    }

    return fail("暂不支持该接口模块", "UNKNOWN_MODULE");
  } catch (error) {
    const code = error.code || "REQUEST_FAILED";
    const message = code === "PERMISSION_DENIED" ? "没有操作权限" : error.message || "请求处理失败";

    return fail(message, code);
  }
};
