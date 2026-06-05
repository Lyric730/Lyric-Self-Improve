const CLOUD_ENV_ID = "cloudbase-d9gg155lc1ee1d72e";

App({
  onLaunch() {
    if (wx.cloud) {
      wx.cloud.init({
        env: CLOUD_ENV_ID,
        traceUser: true
      });
    }
  },

  globalData: {
    clubName: "云瀚台球俱乐部"
  }
});
