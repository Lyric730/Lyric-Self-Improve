const ROLE_ORDER = {
  player: 1,
  staff: 2,
  screen: 2,
  owner: 3
};
const ROLE_KEY = "yunhanUserRole";

function normalizeRoles(roles) {
  return Array.isArray(roles) ? roles : [roles];
}

function getCurrentRole() {
  const storedRole = wx.getStorageSync(ROLE_KEY);
  return ROLE_ORDER[storedRole] ? storedRole : "player";
}

function setCurrentRole(role) {
  const nextRole = ROLE_ORDER[role] ? role : "player";

  wx.setStorageSync(ROLE_KEY, nextRole);

  return nextRole;
}

function canAccess(allowedRoles) {
  const currentRole = getCurrentRole();
  const roles = normalizeRoles(allowedRoles);

  if (currentRole === "owner") {
    return true;
  }

  return roles.includes(currentRole);
}

function requireRole(allowedRoles, options = {}) {
  if (canAccess(allowedRoles)) {
    return true;
  }

  wx.showToast({
    title: options.message || "当前账号暂无权限",
    icon: "none"
  });

  setTimeout(() => {
    wx.reLaunch({
      url: options.redirectUrl || "/pages/challenge-home/challenge-home"
    });
  }, 800);

  return false;
}

module.exports = {
  canAccess,
  getCurrentRole,
  requireRole,
  setCurrentRole
};
