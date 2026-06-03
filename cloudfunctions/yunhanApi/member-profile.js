function toTrimmedString(value) {
  return String(value || "").trim();
}

function buildProfileDraft(profile = {}) {
  return {
    name: toTrimmedString(profile.name),
    phone: toTrimmedString(profile.phone).replace(/[^\d]/g, ""),
    note: toTrimmedString(profile.note),
    avatarUrl: toTrimmedString(profile.avatarUrl)
  };
}

function normalizeMemberProfile(profile = {}) {
  const draft = buildProfileDraft(profile);

  return {
    name: draft.name,
    phone: draft.phone,
    note: draft.note,
    avatarUrl: draft.avatarUrl
  };
}

function validateMemberProfile(profile = {}) {
  const draft = buildProfileDraft(profile);
  const errors = [];

  if (!draft.name) {
    errors.push("昵称不能为空");
  }

  if (draft.name.length > 12) {
    errors.push("昵称最多 12 个字");
  }

  if (draft.phone && !/^1\d{10}$/.test(draft.phone)) {
    errors.push("手机号需要填写 11 位大陆手机号");
  }

  if (draft.note.length > 80) {
    errors.push("备注最多 80 个字");
  }

  if (draft.avatarUrl.length > 500) {
    errors.push("头像地址过长");
  }

  return {
    ok: errors.length === 0,
    errors,
    value: normalizeMemberProfile(draft)
  };
}

function assertValidMemberProfile(profile = {}) {
  const validation = validateMemberProfile(profile);

  if (!validation.ok) {
    const error = new Error(validation.errors[0] || "会员资料需要调整");
    error.code = "INVALID_MEMBER_PROFILE";
    error.validationErrors = validation.errors;
    throw error;
  }

  return validation.value;
}

module.exports = {
  assertValidMemberProfile,
  buildProfileDraft,
  normalizeMemberProfile,
  validateMemberProfile
};
