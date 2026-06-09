const cloud = require("wx-server-sdk");
const QRCode = require("qrcode");
const { assertValidAdminConfig } = require("./admin-config-validator");
const { assertValidMemberProfile } = require("./member-profile");
const {
  DEFAULT_MODES,
  formatRankTitle,
  normalizeRankState
} = require("./settlement-engine");
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

const DEFAULT_SCREEN_CONFIG = {
  storeBoard: "店内总榜",
  bountyBoard: "赏金猎人",
  refreshText: "60 秒刷新",
  activityTitle: "今晚活动",
  activityText: "完成有效挑战，随机奖励提升"
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

async function getOwnerReady(storeId) {
  try {
    return Boolean(await getExistingOwner(storeId));
  } catch (error) {
    return false;
  }
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

  let existingOwner = null;

  try {
    existingOwner = await getExistingOwner(storeId);
  } catch (error) {
    return fail("请先创建 store_members 集合后再初始化老板账号", "STORE_MEMBERS_COLLECTION_REQUIRED");
  }

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

async function applyRankStateUpdates(pointChanges, rankChanges, storeId) {
  const rows = [];

  for (const change of pointChanges) {
    const rankChange = rankChanges && rankChanges[change.side];

    if (!rankChange || !rankChange.after) {
      continue;
    }

    const rankState = normalizeRankState(rankChange.after);
    const rankTitle = formatRankTitle(rankState);
    const memberResult = await db.collection("store_members")
      .where({
        storeId,
        openid: change.openid
      })
      .limit(1)
      .get();
    const member = memberResult.data && memberResult.data.length > 0 ? memberResult.data[0] : null;

    if (member) {
      await db.collection("store_members").doc(member._id).update({
        data: {
          rankState,
          rankTitle,
          lastRankUpdatedAt: db.serverDate(),
          updatedAt: db.serverDate()
        }
      });
    } else {
      await db.collection("store_members").add({
        data: {
          storeId,
          openid: change.openid,
          role: "player",
          status: "active",
          rankState,
          rankTitle,
          lastRankUpdatedAt: db.serverDate(),
          createdAt: db.serverDate(),
          updatedAt: db.serverDate()
        }
      });
    }

    rows.push({
      openid: change.openid,
      side: change.side,
      result: change.result,
      rankState,
      rankTitle,
      deltaStars: Number(rankChange.deltaStars || 0),
      protected: Boolean(rankChange.protected)
    });
  }

  return rows;
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
    const rankState = normalizeRankState();

    return {
      name: "当前会员",
      shortName: "我",
      rankTitle: "会员",
      rankState
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
    const rankState = normalizeRankState(member && member.rankState ? member.rankState : {});

    return {
      name,
      shortName: getShortName(name),
      rankTitle: member && member.rankTitle ? member.rankTitle : formatRankTitle(rankState),
      rankState
    };
  } catch (error) {
    const rankState = normalizeRankState();

    return {
      name: "当前会员",
      shortName: "我",
      rankTitle: "会员",
      rankState
    };
  }
}

function formatRoomState(match, hostSnapshot, guestSnapshot) {
  const opponentJoined = Boolean(match.guestOpenid);
  const startedAtMs = Number(match.startedAtMs || 0);
  const elapsedSeconds = startedAtMs > 0 ? Math.max(1, Math.floor((Date.now() - startedAtMs) / 1000) + 1) : 0;

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
    playState: match.status === "playing" || match.status === "settlement_pending" || startedAtMs > 0 ? {
      scoreA: Number(match.scoreA || 0),
      scoreB: Number(match.scoreB || 0),
      startedAtMs,
      elapsedSeconds,
      targetWins: Number(match.targetWins || 0),
      minimumMinutes: Number(match.minimumMinutes || 0),
      timeReady: Number(match.minimumMinutes || 0) > 0 ? elapsedSeconds >= Number(match.minimumMinutes || 0) * 60 : false,
      winnerSide: match.winnerSide || ""
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

function buildPlayState(match) {
  const startedAtMs = Number(match.startedAtMs || Date.now());
  const elapsedSeconds = Math.max(1, Math.floor((Date.now() - startedAtMs) / 1000) + 1);
  const minimumMinutes = Number(match.minimumMinutes || 0);
  const targetWins = Number(match.targetWins || 0);
  const scoreA = Number(match.scoreA || 0);
  const scoreB = Number(match.scoreB || 0);
  const winnerSide = match.winnerSide || (targetWins > 0 && scoreA >= targetWins ? "a" : targetWins > 0 && scoreB >= targetWins ? "b" : "");

  return {
    matchId: match._id || match.matchId || "",
    status: match.status || "playing",
    scoreA,
    scoreB,
    startedAtMs,
    elapsedSeconds,
    targetWins,
    minimumMinutes,
    timeReady: minimumMinutes > 0 ? elapsedSeconds >= minimumMinutes * 60 : false,
    winnerSide
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
    const configError = new Error("玩法配置读取失败，请稍后重试");
    configError.code = "MODE_CONFIG_READ_FAILED";
    throw configError;
  }

  return DEFAULT_MODES.map(normalizeConfigMode);
}

function buildModeSetup(mode, payload = {}) {
  const requestedBase = Number(payload.selectedBase ?? payload.base);
  const requestedMultiplier = Number(payload.selectedMultiplier ?? payload.multiplier);
  const selectedBase = mode.baseOptions.includes(requestedBase)
    ? requestedBase
    : Number(mode.baseOptions[1] || mode.baseOptions[0] || 0);
  const selectedMultiplier = mode.multipliers.includes(requestedMultiplier)
    ? requestedMultiplier
    : Number(mode.multipliers[0] || 1);

  return {
    mode,
    selectedBase,
    selectedMultiplier,
    riskPoints: selectedBase * selectedMultiplier
  };
}

async function getStoreModeSetup(payload, storeId) {
  const modeList = await getStoreModes(storeId);
  const selectedMode = payload.modeId
    ? modeList.find((mode) => mode.modeId === payload.modeId)
    : modeList.find((mode) => mode.enabled !== false) || modeList[0];

  if (!selectedMode) {
    return fail("当前门店暂未配置可用玩法", "MODE_CONFIG_EMPTY");
  }

  return {
    modes: modeList,
    setup: buildModeSetup(selectedMode, payload)
  };
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

async function startMatchRoom(payload, storeId, operatorOpenid) {
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

  if (operatorOpenid !== match.hostOpenid && operatorOpenid !== match.guestOpenid) {
    return fail("只有本场双方可以开始比赛", "MATCH_PLAYER_REQUIRED");
  }

  if (!match.hostOpenid || !match.guestOpenid) {
    return fail("双方到齐后才能开始比赛", "MATCH_PLAYERS_NOT_READY");
  }

  if (!match.modeId || !match.base || !match.multiplier || !match.targetWins || !match.minimumMinutes) {
    return fail("请先确认玩法和风险积分", "MATCH_SETUP_REQUIRED");
  }

  if (match.status === "playing" || match.status === "settlement_pending") {
    return {
      matchId: match._id,
      playState: buildPlayState(match),
      roomState: formatRoomState(
        match,
        await getMemberSnapshot(match.hostOpenid, storeId),
        await getMemberSnapshot(match.guestOpenid, storeId)
      )
    };
  }

  if (match.status !== "configured") {
    return fail("当前房间状态不能开始比赛", "MATCH_STATUS_INVALID");
  }

  const startedAtMs = Date.now();
  const startData = {
    status: "playing",
    scoreA: Number(match.scoreA || 0),
    scoreB: Number(match.scoreB || 0),
    winnerSide: "",
    startedAt: db.serverDate(),
    startedAtMs,
    updatedAt: db.serverDate()
  };
  const updateResult = await db.collection("matches")
    .where({
      _id: match._id,
      storeId,
      status: "configured"
    })
    .update({
      data: startData
    });

  if (!updateResult.stats || updateResult.stats.updated < 1) {
    const refreshed = await db.collection("matches").doc(match._id).get();
    const refreshedMatch = refreshed.data;

    if (refreshedMatch && (refreshedMatch.status === "playing" || refreshedMatch.status === "settlement_pending")) {
      return {
        matchId: refreshedMatch._id,
        playState: buildPlayState(refreshedMatch),
        roomState: formatRoomState(
          refreshedMatch,
          await getMemberSnapshot(refreshedMatch.hostOpenid, storeId),
          await getMemberSnapshot(refreshedMatch.guestOpenid, storeId)
        )
      };
    }

    return fail("比赛开始失败，请重试", "MATCH_START_FAILED");
  }

  const startedMatch = {
    ...match,
    ...startData
  };
  const hostSnapshot = await getMemberSnapshot(startedMatch.hostOpenid, storeId);
  const guestSnapshot = await getMemberSnapshot(startedMatch.guestOpenid, storeId);

  return {
    matchId: startedMatch._id,
    playState: buildPlayState(startedMatch),
    roomState: formatRoomState(startedMatch, hostSnapshot, guestSnapshot)
  };
}

async function recordMatchScore(payload, storeId, operatorOpenid) {
  requirePayloadValue(payload, "matchId", "请选择比赛房间", "MATCH_ID_REQUIRED");
  requirePayloadValue(payload, "side", "请选择计分方", "MATCH_SCORE_SIDE_REQUIRED");

  const side = payload.side === "b" ? "b" : "a";
  const delta = Number(payload.delta || 0);

  if (delta !== 1 && delta !== -1) {
    return fail("盘数只能单次加一或减一", "MATCH_SCORE_DELTA_INVALID");
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

  if (operatorOpenid !== match.hostOpenid && operatorOpenid !== match.guestOpenid) {
    return fail("只有本场双方可以修改盘数", "MATCH_PLAYER_REQUIRED");
  }

  if (match.status !== "playing" && match.status !== "settlement_pending") {
    return fail("比赛尚未开始，不能计分", "MATCH_NOT_PLAYING");
  }

  const targetWins = Number(match.targetWins || 0);
  const currentScoreA = Number(match.scoreA || 0);
  const currentScoreB = Number(match.scoreB || 0);
  const nextScoreA = side === "a" ? Math.max(0, Math.min(targetWins, currentScoreA + delta)) : currentScoreA;
  const nextScoreB = side === "b" ? Math.max(0, Math.min(targetWins, currentScoreB + delta)) : currentScoreB;
  const winnerSide = targetWins > 0 && nextScoreA >= targetWins ? "a" : targetWins > 0 && nextScoreB >= targetWins ? "b" : "";
  const nextStatus = winnerSide ? "settlement_pending" : "playing";
  const updateData = {
    scoreA: nextScoreA,
    scoreB: nextScoreB,
    winnerSide,
    status: nextStatus,
    updatedAt: db.serverDate()
  };
  const updateResult = await db.collection("matches").doc(match._id).update({
    data: updateData
  });

  if (!updateResult.stats || updateResult.stats.updated < 1) {
    return fail("盘数保存失败，请重试", "MATCH_SCORE_UPDATE_FAILED");
  }

  await db.collection("match_score_events").add({
    data: {
      storeId,
      matchId: match._id,
      operatorOpenid,
      side,
      delta,
      scoreA: nextScoreA,
      scoreB: nextScoreB,
      createdAt: db.serverDate()
    }
  });

  const nextMatch = {
    ...match,
    ...updateData
  };

  return {
    matchId: nextMatch._id,
    playState: buildPlayState(nextMatch)
  };
}

async function buildCloudSettlementPayload(payload, match, storeId) {
  const startedAtMs = Number(match.startedAtMs || 0);
  const elapsedSeconds = startedAtMs > 0
    ? Math.max(1, Math.floor((Date.now() - startedAtMs) / 1000) + 1)
    : Number(payload.elapsedSeconds || payload.elapsed || 0);
  const playerAOpenid = match.hostOpenid || payload.playerAOpenid;
  const playerBOpenid = match.guestOpenid || payload.playerBOpenid;
  const [playerASnapshot, playerBSnapshot] = await Promise.all([
    getMemberSnapshot(playerAOpenid, storeId),
    getMemberSnapshot(playerBOpenid, storeId)
  ]);

  return {
    ...payload,
    ...match,
    matchId: payload.matchId,
    playerAOpenid,
    playerBOpenid,
    selectedBase: match.base || payload.selectedBase || payload.base,
    selectedMultiplier: match.multiplier || payload.selectedMultiplier || payload.multiplier,
    rankStateA: playerASnapshot.rankState,
    rankStateB: playerBSnapshot.rankState,
    elapsedSeconds
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

  const cloudSettlementPayload = await buildCloudSettlementPayload(payload, matchResult.match, storeId);
  const preview = buildSettlementPreview(cloudSettlementPayload);

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

  const cloudSettlementPayload = await buildCloudSettlementPayload(payload, matchResult.match, storeId);
  const plan = buildSettlementWritePlan(cloudSettlementPayload);

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
  const rankResults = await applyRankStateUpdates(plan.pointChanges, plan.rankChanges, storeId);

  await db.collection("settlements").doc(settlementDocId).update({
    data: {
      status: "settled",
      balances,
      rankResults,
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
    rankResults,
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

async function getPlayerIdentity(openid, storeId) {
  const snapshot = await getMemberSnapshot(openid, storeId);
  const account = await ensureMemberPointAccount(openid, storeId);

  return {
    openid,
    name: snapshot.name,
    shortName: snapshot.shortName,
    rankTitle: snapshot.rankTitle,
    rankState: snapshot.rankState,
    points: account.balance
  };
}

function buildEmptyPlayerStats() {
  return {
    seasonWinRate: "0%",
    validMatches: 0,
    winStreak: 0,
    storeRank: "-",
    sameRankRank: "-",
    friendRank: "-",
    bestStreak: 0
  };
}

async function getRecentPlayerSettlements(openid, storeId) {
  const result = await db.collection("settlements")
    .where({
      storeId,
      status: "settled"
    })
    .limit(80)
    .get();
  const rows = result.data || [];

  return rows.filter((settlement) => Array.isArray(settlement.pointChanges)
    && settlement.pointChanges.some((change) => change.openid === openid));
}

function buildStatsFromSettlements(openid, settlements = {}) {
  const rows = Array.isArray(settlements) ? settlements : [];
  const validMatches = rows.length;
  const wins = rows.filter((settlement) => {
    const change = settlement.pointChanges.find((item) => item.openid === openid);

    return change && change.result === "win";
  }).length;

  return {
    ...buildEmptyPlayerStats(),
    seasonWinRate: validMatches > 0 ? `${Math.round((wins / validMatches) * 100)}%` : "0%",
    validMatches
  };
}

async function getRankingRows(storeId, limit = 30) {
  const result = await db.collection("member_points")
    .where({ storeId })
    .orderBy("balance", "desc")
    .limit(limit)
    .get();
  const accounts = result.data || [];
  const rows = [];

  for (let index = 0; index < accounts.length; index += 1) {
    const account = accounts[index];
    const snapshot = await getMemberSnapshot(account.openid, storeId);

    rows.push({
      id: account.openid || account._id,
      openid: account.openid || "",
      no: index + 1,
      name: snapshot.name,
      rank: snapshot.rankTitle,
      points: Number(account.balance || 0),
      trend: "0"
    });
  }

  return rows;
}

async function getPlayerProfileData(openid, storeId) {
  const player = await getPlayerIdentity(openid, storeId);
  const settlements = await getRecentPlayerSettlements(openid, storeId);
  const rankingRows = await getRankingRows(storeId, 50);
  const sameRankRows = rankingRows.filter((row) => row.rank === player.rankTitle);
  const storeRankIndex = rankingRows.findIndex((row) => row.openid === openid);
  const sameRankIndex = sameRankRows.findIndex((row) => row.openid === openid);

  return {
    match: {
      playerA: player
    },
    playerStats: {
      ...buildStatsFromSettlements(openid, settlements),
      storeRank: storeRankIndex >= 0 ? storeRankIndex + 1 : "-",
      sameRankRank: sameRankIndex >= 0 ? sameRankIndex + 1 : "-",
      friendRank: "-"
    }
  };
}

async function getPlayerRankingsData(openid, storeId) {
  const player = await getPlayerIdentity(openid, storeId);
  const storeRows = await getRankingRows(storeId, 50);
  const sameRankRows = storeRows.filter((row) => row.rank === player.rankTitle);

  return [
    { id: "store", label: "店内总榜", rows: storeRows },
    { id: "sameRank", label: "同段位榜", rows: sameRankRows },
    { id: "friends", label: "微信好友榜", rows: [] }
  ];
}

async function getPlayerPointsPerksData(openid, storeId) {
  const player = await getPlayerIdentity(openid, storeId);
  const pointsConfig = await getStorePointsConfig(storeId);

  return {
    match: {
      playerA: player
    },
    pointsPerks: {
      exchangeThreshold: Number(pointsConfig.exchangeThreshold || DEFAULT_POINTS_CONFIG.exchangeThreshold),
      tableOpenBonus: Number(pointsConfig.tableOpenBonus || DEFAULT_POINTS_CONFIG.tableOpenBonus),
      nextRewardText: "当前积分可到前台兑换礼遇",
      counterHint: "到前台出示会员码，工作人员核销积分后发放礼遇。"
    }
  };
}

async function getActiveTableSession(storeId, tableId = "") {
  const query = {
    storeId,
    status: "active"
  };

  if (tableId) {
    query.tableId = tableId;
  }

  const result = await db.collection("table_sessions")
    .where(query)
    .limit(1)
    .get();

  return result.data && result.data.length > 0 ? result.data[0] : null;
}

async function getChallengeHomeData(openid, storeId, payload = {}) {
  const player = await getPlayerIdentity(openid, storeId);
  const tableSession = await getActiveTableSession(storeId, payload.tableId || payload.tableNo || "");
  const tableReady = Boolean(tableSession && tableSession.dueTime);
  const tableNo = tableSession ? tableSession.tableId : payload.tableNo || "未开台";
  const dueTime = tableSession && tableSession.dueTime ? tableSession.dueTime : "--:--";

  return {
    match: {
      clubName: "云瀚台球俱乐部",
      tableNo,
      dueTime,
      playerA: player
    },
    challengeGate: {
      tableSession: {
        tableNo,
        clubName: "云瀚台球俱乐部",
        dueTime,
        openedAt: tableReady ? "已开台" : "联系前台",
        remainingText: tableReady ? `到点 ${dueTime}` : "请先开台",
        statusText: tableReady ? "排位可用" : "暂不可用"
      },
      requiredChecks: [
        {
          key: "auth",
          ready: Boolean(openid),
          userMessage: "请先登录后再发起挑战"
        },
        {
          key: "tableSession",
          ready: tableReady,
          userMessage: "请先联系前台设置球桌到点时间"
        }
      ],
      unavailableMessage: "请先在前台完成开台后再发起挑战"
    }
  };
}

async function getStoreScreenConfig(storeId) {
  const configResult = await db.collection("admin_configs")
    .where({ storeId })
    .limit(1)
    .get();
  const configDoc = configResult.data && configResult.data.length > 0 ? configResult.data[0] : null;
  const screen = configDoc && configDoc.config && configDoc.config.screen ? configDoc.config.screen : {};

  return {
    ...DEFAULT_SCREEN_CONFIG,
    ...screen
  };
}

async function getBountyRows(storeId, limit = 10) {
  const result = await db.collection("settlements")
    .where({
      storeId,
      status: "settled"
    })
    .limit(120)
    .get();
  const totals = {};
  const rows = result.data || [];

  rows.forEach((settlement) => {
    if (!Array.isArray(settlement.pointChanges)) {
      return;
    }

    settlement.pointChanges.forEach((change) => {
      const delta = Number(change.delta || 0);
      const openid = change.openid || "";

      if (!openid || change.result !== "win" || delta <= 0) {
        return;
      }

      if (!totals[openid]) {
        totals[openid] = {
          openid,
          points: 0,
          wins: 0
        };
      }

      totals[openid].points += delta;
      totals[openid].wins += 1;
    });
  });

  const sorted = Object.values(totals)
    .sort((a, b) => b.points - a.points)
    .slice(0, limit);
  const bountyRows = [];

  for (let index = 0; index < sorted.length; index += 1) {
    const item = sorted[index];
    const snapshot = await getMemberSnapshot(item.openid, storeId);

    bountyRows.push({
      id: item.openid,
      openid: item.openid,
      no: index + 1,
      name: snapshot.name,
      rank: snapshot.rankTitle,
      points: item.points,
      trend: `${item.wins} 场`
    });
  }

  return bountyRows;
}

async function validateScreenToken(screenToken, storeId) {
  if (!screenToken) {
    return false;
  }

  const result = await db.collection("screen_tokens")
    .where({
      storeId,
      token: screenToken,
      status: "active"
    })
    .limit(1)
    .get();

  return Boolean(result.data && result.data.length > 0);
}

async function getScreenBoardData(storeId) {
  const [screenConfig, rankingRows, bountyRows] = await Promise.all([
    getStoreScreenConfig(storeId),
    getRankingRows(storeId, 30),
    getBountyRows(storeId, 12)
  ]);

  return {
    match: {
      clubName: "云瀚台球俱乐部"
    },
    screenConfig,
    topRows: rankingRows.slice(0, 3),
    rankingRows: rankingRows.slice(3, 15),
    bountyRows
  };
}

async function handlePlayer(event) {
  const wxContext = getWxContext();
  const storeId = getStoreId(event);

  await assertRole(wxContext, ["player", "staff", "owner"], storeId);

  if (event.action === "getChallengeHome") {
    return ok(await getChallengeHomeData(wxContext.OPENID, storeId, event.payload || {}));
  }

  if (event.action === "getProfile") {
    return ok(await getPlayerProfileData(wxContext.OPENID, storeId));
  }

  if (event.action === "getRankings") {
    return ok({
      tabs: await getPlayerRankingsData(wxContext.OPENID, storeId)
    });
  }

  if (event.action === "getPointsPerks") {
    return ok(await getPlayerPointsPerksData(wxContext.OPENID, storeId));
  }

  return fail("暂不支持该球友端操作", "UNKNOWN_PLAYER_ACTION");
}

async function handleAuth(event) {
  const wxContext = getWxContext();

  if (event.action === "bootstrapOwner") {
    return handleBootstrapOwner(event, wxContext);
  }

  const storeId = getStoreId(event);
  const role = await getMemberRole(wxContext.OPENID, storeId);
  const ownerReady = await getOwnerReady(storeId);

  return ok({
    openid: wxContext.OPENID,
    unionid: wxContext.UNIONID || "",
    appid: wxContext.APPID,
    role,
    ownerReady,
    storeId
  });
}

async function handleMatch(event) {
  const wxContext = getWxContext();
  const storeId = getStoreId(event);

  if (event.action === "getModes") {
    await assertRole(wxContext, ["player", "staff", "owner"], storeId);

    return ok({
      modes: await getStoreModes(storeId)
    });
  }

  if (event.action === "getSetup") {
    await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const result = await getStoreModeSetup(event.payload || {}, storeId);

    if (isFailureResult(result)) {
      return result;
    }

    return ok(result);
  }

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

  if (event.action === "start") {
    const role = await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await startMatchRoom(payload, storeId, wxContext.OPENID);

    if (isFailureResult(result)) {
      return result;
    }

    await writeOperationLog({
      module: "match",
      action: event.action,
      payload: {
        matchId: result.matchId,
        status: result.playState.status,
        scoreA: result.playState.scoreA,
        scoreB: result.playState.scoreB
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

  if (event.action === "recordScore") {
    const role = await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    const payload = event.payload || {};
    const result = await recordMatchScore(payload, storeId, wxContext.OPENID);

    if (isFailureResult(result)) {
      return result;
    }

    await writeOperationLog({
      module: "match",
      action: event.action,
      payload: {
        matchId: result.matchId,
        side: payload.side,
        delta: payload.delta,
        scoreA: result.playState.scoreA,
        scoreB: result.playState.scoreB,
        winnerSide: result.playState.winnerSide
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
  const payload = event.payload || {};
  const wxContext = getWxContext();
  const storeId = getStoreId(event);
  const screenToken = payload.screenToken || event.screenToken || "";

  if (event.action !== "getBoard") {
    return fail("暂不支持该大屏操作", "UNKNOWN_SCREEN_ACTION");
  }

  if (screenToken) {
    const tokenValid = await validateScreenToken(screenToken, storeId);

    if (!tokenValid) {
      return fail("大屏访问凭证无效", "SCREEN_TOKEN_INVALID");
    }
  } else {
    await assertRole(wxContext, ["staff", "owner", "screen"], storeId);
  }

  return ok(await getScreenBoardData(storeId));
}

exports.main = async (event = {}) => {
  try {
    if (event.module === "auth") {
      return handleAuth(event);
    }

    if (event.module === "match") {
      return handleMatch(event);
    }

    if (event.module === "player") {
      return handlePlayer(event);
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
