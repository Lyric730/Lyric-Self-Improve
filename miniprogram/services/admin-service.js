const { callCloud, ensureOk, success } = require("./api-client");
const { adminConfig } = require("../utils/ladder-data");
const { assertValidAdminConfig } = require("../utils/admin-config-validator");
const { isDevtoolsPreview } = require("../utils/dev-preview");

const ADMIN_CONFIG_STORAGE_KEY = "yunhan_admin_config";
const LOCAL_ROLE_MEMBERS_STORAGE_KEY = "yunhan_admin_role_members";

let currentAdminConfig = adminConfig;

function canUseStorage() {
  return typeof wx !== "undefined" && wx && wx.getStorageSync && wx.setStorageSync;
}

function readStoredConfig() {
  if (!canUseStorage()) {
    return null;
  }

  try {
    const storedConfig = wx.getStorageSync(ADMIN_CONFIG_STORAGE_KEY);

    return storedConfig && typeof storedConfig === "object" ? storedConfig : null;
  } catch (error) {
    return null;
  }
}

function writeStoredConfig(config) {
  if (!canUseStorage()) {
    return;
  }

  try {
    wx.setStorageSync(ADMIN_CONFIG_STORAGE_KEY, config);
  } catch (error) {
    // Storage failure should not block the current edit session.
  }
}

function readStoredRoleMembers() {
  if (!canUseStorage()) {
    return {};
  }

  try {
    const storedMembers = wx.getStorageSync(LOCAL_ROLE_MEMBERS_STORAGE_KEY);

    return storedMembers && typeof storedMembers === "object" ? storedMembers : {};
  } catch (error) {
    return {};
  }
}

function writeStoredRoleMembers(members) {
  if (!canUseStorage()) {
    return;
  }

  try {
    wx.setStorageSync(LOCAL_ROLE_MEMBERS_STORAGE_KEY, members);
  } catch (error) {
    // Local preview storage should not block permission editing.
  }
}

function getAdminConfig() {
  const storedConfig = readStoredConfig();

  if (storedConfig) {
    currentAdminConfig = storedConfig;
  }

  return success(currentAdminConfig);
}

async function saveAdminConfig(config) {
  assertValidAdminConfig(config);

  try {
    ensureOk(await callCloud("admin", "saveConfig", {
      config,
      storeId: config.storeId || "default"
    }));
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
  }

  currentAdminConfig = config;
  writeStoredConfig(config);

  return success({
    savedAt: new Date().toISOString()
  });
}

async function getMemberForRole(params = {}) {
  const openid = String(params.openid || "").trim();

  if (!openid) {
    return {
      ok: false,
      code: "MEMBER_OPENID_REQUIRED",
      message: "请先选择会员"
    };
  }

  try {
    const member = ensureOk(await callCloud("admin", "getMemberForRole", {
      openid,
      storeId: params.storeId || "default"
    }));

    return success(member);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }

    const members = readStoredRoleMembers();
    const storedMember = members[openid] || {};

    return success({
      openid,
      name: storedMember.name || params.name || "待授权会员",
      role: storedMember.role || "player",
      status: storedMember.status || "active",
      points: Number(storedMember.points || 0)
    });
  }
}

async function setMemberRole(params = {}) {
  const openid = String(params.openid || "").trim();
  const targetRole = String(params.targetRole || "").trim();
  const allowedRoles = ["player", "staff", "screen"];

  if (!openid) {
    return {
      ok: false,
      code: "MEMBER_OPENID_REQUIRED",
      message: "请先选择会员"
    };
  }

  if (!allowedRoles.includes(targetRole)) {
    return {
      ok: false,
      code: "INVALID_TARGET_ROLE",
      message: "请选择正确的身份"
    };
  }

  try {
    const member = ensureOk(await callCloud("admin", "setMemberRole", {
      openid,
      targetRole,
      storeId: params.storeId || "default"
    }));

    return success(member);
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }

    const members = readStoredRoleMembers();
    const nextMember = {
      ...(members[openid] || {}),
      openid,
      name: params.name || (members[openid] && members[openid].name) || "待授权会员",
      role: targetRole,
      status: "active"
    };

    members[openid] = nextMember;
    writeStoredRoleMembers(members);

    return success(nextMember);
  }
}

module.exports = {
  getAdminConfig,
  getMemberForRole,
  saveAdminConfig,
  setMemberRole
};
