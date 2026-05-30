const { requireRole } = require("../../utils/access-control");
const { ensureOk } = require("../../services/api-client");
const { getAdminConfig, saveAdminConfig } = require("../../services/admin-service");

Page({
  data: {
    accessReady: false,
    adminConfig: ensureOk(getAdminConfig()),
    saving: false
  },

  onLoad() {
    const accessReady = requireRole(["owner"]);

    this.setData({ accessReady });
  },

  async saveConfig() {
    if (!this.data.accessReady || this.data.saving) {
      return;
    }

    this.setData({ saving: true });

    try {
      ensureOk(await saveAdminConfig(this.data.adminConfig));

      wx.showToast({ title: "配置已保存", icon: "success" });
    } catch (error) {
      wx.showToast({ title: error.message || "保存失败", icon: "none" });
    } finally {
      this.setData({ saving: false });
    }
  }
});
