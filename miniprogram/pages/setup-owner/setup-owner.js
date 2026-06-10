const { ensureOk } = require("../../services/api-client");
const { bootstrapOwner, getAuthInfo } = require("../../services/auth-service");
const { setCurrentRole } = require("../../utils/access-control");

Page({
  data: {
    storeId: "default",
    nickname: "云瀚老板",
    bootstrapSecret: "",
    authInfo: null,
    loading: true,
    submitting: false,
    errorText: "",
    resultText: ""
  },

  onLoad() {
    this.loadAuthInfo();
  },

  async loadAuthInfo() {
    this.setData({
      loading: true,
      errorText: "",
      resultText: ""
    });

    try {
      const authInfo = ensureOk(await getAuthInfo(this.data.storeId));

      this.setData({
        authInfo,
        loading: false,
        resultText: authInfo.ownerReady ? "当前门店已有老板账号" : ""
      });

      if (authInfo && authInfo.role) {
        setCurrentRole(authInfo.role);
      }
    } catch (error) {
      this.setData({
        loading: false,
        errorText: error.message || "读取初始化状态失败"
      });
    }
  },

  handleInput(event) {
    const field = event.currentTarget.dataset.field;

    this.setData({
      [field]: event.detail.value,
      errorText: "",
      resultText: ""
    });
  },

  async submitBootstrap() {
    if (this.data.submitting || this.data.loading) {
      return;
    }

    const bootstrapSecret = String(this.data.bootstrapSecret || "").trim();
    const nickname = String(this.data.nickname || "").trim();

    if (!bootstrapSecret) {
      this.setData({ errorText: "请输入初始化密钥" });
      return;
    }

    this.setData({
      submitting: true,
      errorText: "",
      resultText: ""
    });

    try {
      const result = ensureOk(await bootstrapOwner({
        storeId: this.data.storeId,
        nickname,
        bootstrapSecret
      }));

      this.setData({
        authInfo: {
          ...(this.data.authInfo || {}),
          openid: result.openid,
          role: result.role,
          ownerReady: true,
          storeId: result.storeId
        },
        bootstrapSecret: "",
        resultText: "老板账号已绑定"
      });
      setCurrentRole("owner");

      wx.showToast({ title: "初始化成功", icon: "none" });
    } catch (error) {
      this.setData({
        errorText: error.message || "初始化失败"
      });
    } finally {
      this.setData({ submitting: false });
    }
  }
});
