const { callCloud, ensureOk, success } = require("./api-client");
const { adminConfig } = require("../utils/ladder-data");
const { assertValidAdminConfig } = require("../utils/admin-config-validator");
const { isDevtoolsPreview } = require("../utils/dev-preview");

const ADMIN_CONFIG_STORAGE_KEY = "yunhan_admin_config";

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

module.exports = {
  getAdminConfig,
  saveAdminConfig
};
