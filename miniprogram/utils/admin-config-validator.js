function pushError(errors, message) {
  errors.push(message);
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function toNumber(value) {
  if (typeof value === "number") {
    return value;
  }

  if (typeof value === "string" && value.trim() !== "") {
    return Number(value.trim());
  }

  return Number.NaN;
}

function isPositiveInteger(value) {
  const numberValue = toNumber(value);
  return Number.isInteger(numberValue) && numberValue > 0;
}

function isNonNegativeInteger(value) {
  const numberValue = toNumber(value);
  return Number.isInteger(numberValue) && numberValue >= 0;
}

function parseRewardRange(rangeText) {
  if (Array.isArray(rangeText) && rangeText.length === 2) {
    const min = toNumber(rangeText[0]);
    const max = toNumber(rangeText[1]);

    if (Number.isFinite(min) && Number.isFinite(max)) {
      return { min, max };
    }
  }

  const text = String(rangeText || "").replace(/分/g, " ");
  const values = text.match(/\d+/g);

  if (!values || values.length < 2) {
    return null;
  }

  return {
    min: Number(values[0]),
    max: Number(values[1])
  };
}

function validateNumberList(values, label, errors) {
  if (!Array.isArray(values) || values.length === 0) {
    pushError(errors, `${label}不能为空`);
    return;
  }

  const seen = {};

  values.forEach((value) => {
    if (!isPositiveInteger(value)) {
      pushError(errors, `${label}只能填写正整数`);
      return;
    }

    const numberValue = toNumber(value);

    if (seen[numberValue]) {
      pushError(errors, `${label}不能重复`);
    }

    seen[numberValue] = true;
  });
}

function validateRewardRange(value, label, errors) {
  const range = parseRewardRange(value);

  if (!range) {
    pushError(errors, `${label}需要填写为“10 ~ 20”这种区间`);
    return;
  }

  if (!Number.isInteger(range.min) || !Number.isInteger(range.max)) {
    pushError(errors, `${label}只能填写整数`);
    return;
  }

  if (range.min < 0 || range.max < 0) {
    pushError(errors, `${label}不能小于 0`);
  }

  if (range.min > range.max) {
    pushError(errors, `${label}的最小值不能大于最大值`);
  }
}

function validateMode(mode, index, errors) {
  const label = mode && mode.name ? mode.name : `玩法 ${index + 1}`;

  if (!isPlainObject(mode)) {
    pushError(errors, `${label}配置不完整`);
    return;
  }

  if (!mode.modeId) {
    pushError(errors, `${label}缺少玩法 ID`);
  }

  if (mode.modeId === "race9" || mode.name === "抢9") {
    pushError(errors, "抢9当前不开放，不能加入玩法模板");
  }

  if (!mode.name) {
    pushError(errors, `${label}缺少玩法名称`);
  }

  if (!isPositiveInteger(mode.targetWins)) {
    pushError(errors, `${label}的目标盘数需要大于 0`);
  }

  if (!isPositiveInteger(mode.minimumMinutes)) {
    pushError(errors, `${label}的最低有效时间需要大于 0`);
  }

  if (!isPositiveInteger(mode.starReward)) {
    pushError(errors, `${label}的胜方加星需要大于 0`);
  }

  validateNumberList(mode.baseOptions, `${label}底分`, errors);
  validateNumberList(mode.multipliers, `${label}倍率`, errors);
  validateRewardRange(mode.normalReward, `${label}普通随机奖励`, errors);
  validateRewardRange(mode.sprintReward, `${label}续时冲刺奖励`, errors);
}

function validatePoints(points, errors) {
  if (!isPlainObject(points)) {
    pushError(errors, "积分补给配置不完整");
    return;
  }

  if (!isNonNegativeInteger(points.newUser)) {
    pushError(errors, "新用户初始积分不能小于 0");
  }

  if (!isNonNegativeInteger(points.checkIn)) {
    pushError(errors, "到店登录积分不能小于 0");
  }

  if (!isNonNegativeInteger(points.tableOpenBonus)) {
    pushError(errors, "开台赠分不能小于 0");
  }

  if (!isPositiveInteger(points.exchangeThreshold)) {
    pushError(errors, "积分兑换门槛需要大于 0");
  }
}

function parseFirstInteger(value) {
  const match = String(value || "").match(/\d+/);
  return match ? Number(match[0]) : Number.NaN;
}

function validateAntiCheat(antiCheat, errors) {
  if (!isPlainObject(antiCheat)) {
    pushError(errors, "防刷分配置不完整");
    return;
  }

  const geoFence = parseFirstInteger(antiCheat.geoFence);

  if (!Number.isInteger(geoFence) || geoFence <= 0) {
    pushError(errors, "店内定位范围需要大于 0 米");
  }
}

function validateScreen(screen, errors) {
  if (!isPlainObject(screen)) {
    pushError(errors, "大屏配置不完整");
    return;
  }

  if (!screen.storeBoard) {
    pushError(errors, "大屏主榜不能为空");
  }

  if (!screen.bountyBoard) {
    pushError(errors, "大屏副榜不能为空");
  }

  const refreshSeconds = parseFirstInteger(screen.refreshText);

  if (!Number.isInteger(refreshSeconds) || refreshSeconds < 10) {
    pushError(errors, "大屏刷新间隔不能低于 10 秒");
  }
}

function validateAdminConfig(config) {
  const errors = [];

  if (!isPlainObject(config)) {
    return {
      ok: false,
      errors: ["门店参数配置不完整"]
    };
  }

  if (!Array.isArray(config.modes) || config.modes.length === 0) {
    pushError(errors, "至少需要配置一个玩法模板");
  } else {
    config.modes.forEach((mode, index) => validateMode(mode, index, errors));

    if (!config.modes.some((mode) => mode && mode.enabled)) {
      pushError(errors, "至少需要启用一个玩法");
    }
  }

  validatePoints(config.points, errors);
  validateAntiCheat(config.antiCheat, errors);
  validateScreen(config.screen, errors);

  return {
    ok: errors.length === 0,
    errors
  };
}

function assertValidAdminConfig(config) {
  const validation = validateAdminConfig(config);

  if (!validation.ok) {
    const error = new Error(validation.errors[0] || "门店参数需要调整");
    error.validationErrors = validation.errors;
    throw error;
  }

  return config;
}

module.exports = {
  assertValidAdminConfig,
  parseRewardRange,
  validateAdminConfig
};
