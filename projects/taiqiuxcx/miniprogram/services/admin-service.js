const { callCloud, ensureOk, success } = require("./api-client");
const { adminConfig } = require("../utils/ladder-data");

function getAdminConfig() {
  return success(adminConfig);
}

async function saveAdminConfig(config) {
  ensureOk(await callCloud("admin", "saveConfig", {
    config,
    storeId: config.storeId || "default"
  }));

  return success({
    savedAt: new Date().toISOString()
  });
}

module.exports = {
  getAdminConfig,
  saveAdminConfig
};
