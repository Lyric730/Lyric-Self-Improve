const CLOUD_FUNCTION_NAME = "yunhanApi";

function success(data) {
  return {
    ok: true,
    data
  };
}

function failure(message, code = "REQUEST_FAILED") {
  return {
    ok: false,
    code,
    message
  };
}

function ensureOk(result) {
  if (!result || !result.ok) {
    const error = new Error(result && result.message ? result.message : "操作失败，请稍后再试");
    error.code = result && result.code ? result.code : "REQUEST_FAILED";
    throw error;
  }

  return result.data;
}

function callCloud(moduleName, action, payload = {}) {
  if (!wx.cloud) {
    return Promise.resolve(failure("当前环境暂不可用", "CLOUD_UNAVAILABLE"));
  }

  return wx.cloud.callFunction({
    name: CLOUD_FUNCTION_NAME,
    data: {
      module: moduleName,
      action,
      payload
    }
  }).then((response) => response.result || failure("请求处理失败"));
}

module.exports = {
  callCloud,
  ensureOk,
  failure,
  success
};
