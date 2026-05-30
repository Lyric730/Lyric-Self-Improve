const { callCloud, ensureOk, success } = require("./api-client");

async function getMemberCode(params = {}) {
  const code = ensureOk(await callCloud("member", "getCode", {
    storeId: params.storeId || "default"
  }));

  return success(code);
}

module.exports = {
  getMemberCode
};
