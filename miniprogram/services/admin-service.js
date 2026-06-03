const { callCloud, ensureOk, success } = require("./api-client");
const { adminConfig } = require("../utils/ladder-data");
const { assertValidAdminConfig } = require("../utils/admin-config-validator");
const { isDevtoolsPreview } = require("../utils/dev-preview");

let currentAdminConfig = adminConfig;

function getAdminConfig() {
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

  return success({
    savedAt: new Date().toISOString()
  });
}

module.exports = {
  getAdminConfig,
  saveAdminConfig
};
