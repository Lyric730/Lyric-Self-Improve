const LOG_STORAGE_KEY = "yunhanOperationLogs";
const MAX_LOG_COUNT = 200;

function readOperationLogs() {
  return wx.getStorageSync(LOG_STORAGE_KEY) || [];
}

function recordOperation(action, payload = {}) {
  const entry = {
    id: `${Date.now()}-${Math.floor(Math.random() * 10000)}`,
    action,
    payload,
    createdAt: new Date().toISOString()
  };
  const nextLogs = [entry, ...readOperationLogs()].slice(0, MAX_LOG_COUNT);

  wx.setStorageSync(LOG_STORAGE_KEY, nextLogs);

  return entry;
}

module.exports = {
  readOperationLogs,
  recordOperation
};
