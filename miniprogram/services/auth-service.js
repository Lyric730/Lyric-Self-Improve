const { callCloud } = require("./api-client");

const DEFAULT_STORE_ID = "default";

function getAuthInfo(storeId = DEFAULT_STORE_ID) {
  return callCloud("auth", "whoami", {
    storeId
  });
}

function bootstrapOwner(params = {}) {
  return callCloud("auth", "bootstrapOwner", {
    storeId: params.storeId || DEFAULT_STORE_ID,
    nickname: params.nickname || "",
    bootstrapSecret: params.bootstrapSecret || ""
  });
}

module.exports = {
  bootstrapOwner,
  getAuthInfo
};
