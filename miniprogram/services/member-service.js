const { callCloud, ensureOk, success } = require("./api-client");
const {
  buildProfileDraft,
  validateMemberProfile
} = require("../utils/member-profile");
const { match } = require("../utils/ladder-data");
const { isDevtoolsPreview } = require("../utils/dev-preview");

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

function buildCodeCells(seedText) {
  const text = String(seedText || "YUNHAN");
  let hash = 0;

  for (let index = 0; index < text.length; index += 1) {
    hash = (hash * 31 + text.charCodeAt(index)) % 9973;
  }

  return Array.from({ length: 49 }).map((_, index) => {
    const row = Math.floor(index / 7);
    const col = index % 7;
    const inCorner =
      (row < 2 && col < 2) ||
      (row < 2 && col > 4) ||
      (row > 4 && col < 2);

    return inCorner || ((hash + row * 7 + col * 11 + index) % 3 === 0);
  });
}

function buildLocalMemberCode() {
  const profile = getCurrentMemberProfile();
  const codeText = `YH-${String(profile.name || "MEMBER").slice(-4)}-${profile.points}`;

  return {
    qrCodeDataUrl: "",
    codeText,
    codeCells: buildCodeCells(codeText),
    points: profile.points
  };
}

async function getMemberCode(params = {}) {
  const result = await callCloud("member", "getCode", {
    storeId: params.storeId || "default"
  });

  if (!result.ok && isDevtoolsPreview()) {
    return success(buildLocalMemberCode());
  }

  const code = ensureOk(result);

  return success(code);
}

function getMemberProfile() {
  const profile = getCurrentMemberProfile();

  return success({
    ...profile,
    draft: buildProfileDraft(profile)
  });
}

async function saveMemberProfile(profile = {}) {
  const validation = validateMemberProfile(profile);

  if (!validation.ok) {
    return {
      ok: false,
      code: "INVALID_MEMBER_PROFILE",
      message: validation.errors[0],
      errors: validation.errors
    };
  }

  try {
    ensureOk(await callCloud("member", "saveProfile", {
      profile: validation.value,
      storeId: "default"
    }));
  } catch (error) {
    if (!isDevtoolsPreview()) {
      throw error;
    }
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
