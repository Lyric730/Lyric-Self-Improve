const ROLE_KEY = "yunhanUserRole";

function isDevtoolsPreview() {
  try {
    const systemInfo = wx.getSystemInfoSync();
    return systemInfo.platform === "devtools";
  } catch (error) {
    return false;
  }
}

function setPreviewRole(role) {
  if (!isDevtoolsPreview()) {
    return;
  }

  wx.setStorageSync(ROLE_KEY, role);
}

module.exports = {
  isDevtoolsPreview,
  setPreviewRole
};
