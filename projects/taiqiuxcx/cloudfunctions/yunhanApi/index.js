const cloud = require("wx-server-sdk");
const QRCode = require("qrcode");

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

  const writeMode = await upsertOne(
    "admin_configs",
    {
      storeId
    },
    {
      config: payload.config,
      updatedBy: operatorOpenid
    }
  );

  return {
    storeId,
    writeMode
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
    return ok({
      matchId: event.matchId || "",
      status: "waiting"
    });
  }

  if (event.action === "settle") {
    await assertRole(wxContext, ["player", "staff", "owner"], storeId);
    return fail("服务端结算规则尚未启用", "SETTLEMENT_NOT_READY");
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
