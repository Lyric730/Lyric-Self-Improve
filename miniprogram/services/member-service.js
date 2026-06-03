const { callCloud, ensureOk, success } = require("./api-client");
const {
  buildProfileDraft,
  validateMemberProfile
} = require("../utils/member-profile");
const { match } = require("../utils/ladder-data");

const MEMBER_PROFILE_STORAGE_KEY = "yunhan_member_profile";

const baseMemberProfile = {
  name: match.playerA.name,
  phone: "",
  note: "",
  avatarUrl: "",
  rankTitle: match.playerA.rankTitle,
  points: match.playerA.points
};

let currentMemberProfile = { ...baseMemberProfile };

function canUseStorage() {
  return typeof wx !== "undefined" && wx && wx.getStorageSync && wx.setStorageSync;
}

function readStoredMemberProfile() {
  if (!canUseStorage()) {
    return null;
  }

  try {
    const storedProfile = wx.getStorageSync(MEMBER_PROFILE_STORAGE_KEY);

    return storedProfile && typeof storedProfile === "object" ? storedProfile : null;
  } catch (error) {
    return null;
  }
}

function writeStoredMemberProfile(profile) {
  if (!canUseStorage()) {
    return;
  }

  try {
    wx.setStorageSync(MEMBER_PROFILE_STORAGE_KEY, buildProfileDraft(profile));
  } catch (error) {
    // Storage failure should not block editing the in-memory profile.
  }
}

function getCurrentMemberProfile() {
  const storedProfile = readStoredMemberProfile();

  if (storedProfile) {
    currentMemberProfile = {
      ...currentMemberProfile,
      ...buildProfileDraft(storedProfile)
    };
  }

  return currentMemberProfile;
}

async function getMemberCode(params = {}) {
  const code = ensureOk(await callCloud("member", "getCode", {
    storeId: params.storeId || "default"
  }));

  return success(code);
}

function getMemberProfile() {
  const profile = getCurrentMemberProfile();

  return success({
    ...profile,
    draft: buildProfileDraft(profile)
  });
}

function saveMemberProfile(profile = {}) {
  const validation = validateMemberProfile(profile);

  if (!validation.ok) {
    return {
      ok: false,
      code: "INVALID_MEMBER_PROFILE",
      message: validation.errors[0],
      errors: validation.errors
    };
  }

  currentMemberProfile = {
    ...currentMemberProfile,
    ...validation.value
  };

  writeStoredMemberProfile(currentMemberProfile);

  return success({
    ...currentMemberProfile,
    draft: buildProfileDraft(currentMemberProfile)
  });
}

module.exports = {
  getMemberCode,
  getMemberProfile,
  saveMemberProfile
};
