const { ensureOk } = require("../../services/api-client");
const {
  getMemberProfile,
  saveMemberProfile
} = require("../../services/member-service");
const { isDevtoolsPreview, setPreviewRole } = require("../../utils/dev-preview");
const { buildProfileDraft } = require("../../utils/member-profile");

const memberProfile = ensureOk(getMemberProfile());

function getInitial(name) {
  const text = String(name || "").trim();

  return text ? text.slice(-1) : "云";
}

Page({
  data: {
    memberProfile,
    profileDraft: buildProfileDraft(memberProfile),
    playerInitial: getInitial(memberProfile.name),
    profileDraftInitial: getInitial(memberProfile.name),
    editingProfile: false,
    savingProfile: false,
    devtoolsPreview: isDevtoolsPreview()
  },

  startEditProfile() {
    this.setData({
      editingProfile: true,
      profileDraft: buildProfileDraft(this.data.memberProfile),
      profileDraftInitial: getInitial(this.data.memberProfile.name)
    });
  },

  cancelEditProfile() {
    this.setData({
      editingProfile: false,
      profileDraft: buildProfileDraft(this.data.memberProfile),
      profileDraftInitial: getInitial(this.data.memberProfile.name)
    });
  },

  handleProfileInput(event) {
    const field = event.currentTarget.dataset.field;
    const value = event.detail.value;

    const nextData = {
      [`profileDraft.${field}`]: value
    };

    if (field === "name") {
      nextData.profileDraftInitial = getInitial(value);
    }

    this.setData(nextData);
  },

  handleChooseAvatar(event) {
    const avatarUrl = event.detail && event.detail.avatarUrl;

    if (!avatarUrl) {
      return;
    }

    this.setData({
      "profileDraft.avatarUrl": avatarUrl
    });
  },

  async saveProfile() {
    if (this.data.savingProfile) {
      return;
    }

    this.setData({ savingProfile: true });

    try {
      const savedProfile = ensureOk(await saveMemberProfile(this.data.profileDraft));

      this.setData({
        memberProfile: savedProfile,
        profileDraft: buildProfileDraft(savedProfile),
        playerInitial: getInitial(savedProfile.name),
        profileDraftInitial: getInitial(savedProfile.name),
        editingProfile: false
      });

      wx.showToast({ title: "资料已保存", icon: "none" });
    } catch (error) {
      wx.showToast({ title: error.message || "保存失败", icon: "none" });
    } finally {
      this.setData({ savingProfile: false });
    }
  },

  goData() {
    wx.navigateTo({ url: "/pages/my-data/my-data" });
  },

  goRankings() {
    wx.navigateTo({ url: "/pages/rankings/rankings" });
  },

  goPerks() {
    wx.navigateTo({ url: "/pages/points-perks/points-perks" });
  },

  goMemberCode() {
    wx.navigateTo({ url: "/pages/member-code/member-code" });
  },

  openRolePage(event) {
    const { role, url } = event.currentTarget.dataset;

    if (this.data.devtoolsPreview) {
      setPreviewRole(role || "player");
    }

    wx.navigateTo({ url });
  }
});
