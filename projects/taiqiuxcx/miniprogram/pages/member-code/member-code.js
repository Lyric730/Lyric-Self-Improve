const { ensureOk } = require("../../services/api-client");
const { getMemberCode } = require("../../services/member-service");

Page({
  data: {
    loading: true,
    qrCodeDataUrl: "",
    errorText: "",
    pointsText: ""
  },

  onLoad() {
    this.loadMemberCode();
  },

  async loadMemberCode() {
    this.setData({
      loading: true,
      errorText: ""
    });

    try {
      const code = ensureOk(await getMemberCode());

      this.setData({
        qrCodeDataUrl: code.qrCodeDataUrl,
        pointsText: `当前积分 ${code.points}`
      });
    } catch (error) {
      this.setData({
        errorText: error.message || "会员码生成失败"
      });
    } finally {
      this.setData({
        loading: false
      });
    }
  },

  goBack() {
    wx.navigateBack();
  }
});
