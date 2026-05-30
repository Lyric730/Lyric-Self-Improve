App({
  onLaunch() {
    if (wx.cloud) {
      wx.cloud.init({
        traceUser: true
      });
    }
  },

  globalData: {
    clubName: "云瀚台球俱乐部"
  }
});
