const assert = require("node:assert/strict");

const {
  buildProfileDraft,
  normalizeMemberProfile,
  validateMemberProfile
} = require("../miniprogram/utils/member-profile");

{
  const draft = buildProfileDraft({
    name: " 云瀚-阿杰 ",
    phone: " 138 0000 8888 ",
    note: "  喜欢抢7  ",
    avatarUrl: "  wxfile://avatar-temp.png  "
  });

  assert.deepEqual(draft, {
    name: "云瀚-阿杰",
    phone: "13800008888",
    note: "喜欢抢7",
    avatarUrl: "wxfile://avatar-temp.png"
  });
}

{
  const normalized = normalizeMemberProfile({
    name: "云瀚-阿杰",
    phone: "13800008888",
    note: "周末常来",
    avatarUrl: "cloud://yunhan/avatar.png",
    rankTitle: "走位黄金 III",
    points: 2860
  });

  assert.equal(normalized.name, "云瀚-阿杰");
  assert.equal(normalized.phone, "13800008888");
  assert.equal(normalized.note, "周末常来");
  assert.equal(normalized.avatarUrl, "cloud://yunhan/avatar.png");
  assert.equal(Object.prototype.hasOwnProperty.call(normalized, "rankTitle"), false);
  assert.equal(Object.prototype.hasOwnProperty.call(normalized, "points"), false);
}

{
  const result = validateMemberProfile({
    name: "阿杰",
    phone: "13800008888",
    note: "周末常来",
    avatarUrl: "wxfile://avatar-temp.png"
  });

  assert.equal(result.ok, true);
  assert.deepEqual(result.errors, []);
}

{
  const result = validateMemberProfile({
    name: "",
    phone: "138",
    note: "a".repeat(81)
  });

  assert.equal(result.ok, false);
  assert.ok(result.errors.some((message) => message.includes("昵称")));
  assert.ok(result.errors.some((message) => message.includes("手机号")));
  assert.ok(result.errors.some((message) => message.includes("备注")));
}

console.log("Member profile tests OK");
