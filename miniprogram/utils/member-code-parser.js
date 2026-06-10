function parseMemberOpenid(rawValue) {
  const raw = String(rawValue || "").trim();

  if (!raw) {
    return "";
  }

  try {
    const parsed = JSON.parse(raw);

    if (parsed.openid) return String(parsed.openid).trim();
    if (parsed.openId) return String(parsed.openId).trim();
  } catch (error) {
    // Non-JSON QR content is handled below.
  }

  const queryMatch = raw.match(/[?&](openid|openId)=([^&]+)/);
  if (queryMatch) return decodeURIComponent(queryMatch[2]).trim();

  const labelMatch = raw.match(/(?:openid|openId):([^\s;]+)/);
  if (labelMatch) return labelMatch[1].trim();

  return raw;
}

module.exports = {
  parseMemberOpenid
};
