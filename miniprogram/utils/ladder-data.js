const {
  calculateMatchSettlement
} = require("./settlement-engine");

const modes = [
  {
    modeId: "race5",
    name: "抢5",
    targetWins: 5,
    minimumMinutes: 40,
    baseOptions: [20, 50, 100],
    multipliers: [1, 2, 3],
    normalReward: "10 ~ 20",
    sprintReward: "50 ~ 100",
    starReward: 1,
    enabled: true,
    tag: "当前开放"
  },
  {
    modeId: "race7",
    name: "抢7",
    targetWins: 7,
    minimumMinutes: 80,
    baseOptions: [50, 100, 200],
    multipliers: [1, 2, 3, 4, 5],
    normalReward: "30 ~ 80",
    sprintReward: "100 ~ 200",
    starReward: 2,
    enabled: true,
    tag: "高收益"
  },
  {
    modeId: "race10",
    name: "抢10",
    targetWins: 10,
    minimumMinutes: 100,
    baseOptions: [100, 200, 300],
    multipliers: [1, 2, 3, 5, 10],
    normalReward: "80 ~ 150",
    sprintReward: "200 ~ 300",
    starReward: 3,
    enabled: false,
    tag: "预留"
  }
];

const selectedMode = modes[0];

function getModeById(modeId) {
  return modes.find((mode) => mode.modeId === modeId) || selectedMode;
}

function buildMatchSetup(params = {}) {
  const mode = getModeById(params.modeId);
  const selectedBase = Number(params.base || mode.baseOptions[1] || mode.baseOptions[0]);
  const selectedMultiplier = Number(params.multiplier || mode.multipliers[0]);
  const riskPoints = selectedBase * selectedMultiplier;

  return {
    mode,
    selectedBase,
    selectedMultiplier,
    riskPoints
  };
}

function formatSignedPoints(value) {
  const numberValue = Number(value || 0);
  return numberValue > 0 ? `+${numberValue}` : `${numberValue}`;
}

function buildSettlement(params = {}) {
  const setup = buildMatchSetup(params);
  const winnerSide = params.winner === "b" ? "b" : "a";
  const winner = winnerSide === "a" ? match.playerA : match.playerB;
  const loser = winnerSide === "a" ? match.playerB : match.playerA;
  const scoreA = Number(params.scoreA || (winnerSide === "a" ? setup.mode.targetWins : match.scoreA));
  const scoreB = Number(params.scoreB || (winnerSide === "b" ? setup.mode.targetWins : match.scoreB));
  const elapsedSeconds = Number(params.elapsed || setup.mode.minimumMinutes * 60);
  const settlement = calculateMatchSettlement({
    mode: setup.mode,
    selectedBase: setup.selectedBase,
    selectedMultiplier: setup.selectedMultiplier,
    scoreA,
    scoreB,
    winnerSide,
    elapsedSeconds,
    rewardValue: params.reward
  });
  const rewardValue = settlement.ok ? settlement.rewardValue : 0;
  const winnerDelta = settlement.ok ? settlement.winnerDelta : 0;
  const loserDelta = settlement.ok ? settlement.loserDelta : 0;
  const winnerAfterPoints = winner.points + winnerDelta;
  const loserAfterPoints = loser.points + loserDelta;
  const starBefore = 3;
  const starAfter = Math.min(5, starBefore + (settlement.ok ? settlement.starReward : 0));

  return {
    ...setup,
    winnerSide,
    winner,
    loser,
    scoreA,
    scoreB,
    scoreText: `${scoreA}:${scoreB}`,
    elapsedSeconds,
    elapsedText: params.elapsedText || match.elapsedText,
    rewardValue,
    rewardRange: settlement.ok ? settlement.rewardRange : setup.mode.normalReward,
    rewardPhase: settlement.ok ? settlement.rewardPhase : "normal",
    winnerDelta,
    loserDelta,
    winnerDeltaText: formatSignedPoints(winnerDelta),
    loserDeltaText: formatSignedPoints(loserDelta),
    loserDeltaVariant: loserDelta < 0 ? "minus" : "reward",
    winnerAfterPoints,
    loserAfterPoints,
    starBefore,
    starAfter,
    starRewardText: `+${settlement.ok ? settlement.starReward : setup.mode.starReward}星`
  };
}

const match = {
  clubName: "云瀚台球俱乐部",
  tableNo: "T03",
  dueTime: "22:30",
  roomNo: "YH-T03-0527",
  playerA: {
    name: "云瀚-阿杰",
    role: "发起方",
    shortName: "杰",
    points: 2860,
    rankTitle: "走位黄金 III"
  },
  playerB: {
    name: "台球小宇",
    role: "挑战方",
    shortName: "宇",
    points: 2420,
    rankTitle: "沉稳青铜 I"
  },
  selectedMode,
  selectedBase: 100,
  selectedMultiplier: 3,
  scoreA: 5,
  scoreB: 3,
  elapsedText: "00:42:10",
  rewardValue: 120,
  riskPoints: 300,
  winnerDelta: 420,
  loserDelta: -180
};

const challengeGate = {
  tableSession: {
    tableNo: "T03",
    clubName: "云瀚台球俱乐部",
    dueTime: "22:30",
    openedAt: "20:30",
    remainingText: "约 2 小时",
    statusText: "排位可用"
  },
  requiredChecks: [
    {
      key: "auth",
      ready: true,
      userMessage: "请先登录后再发起挑战"
    },
    {
      key: "location",
      ready: true,
      userMessage: "请回到店内后再发起挑战"
    },
    {
      key: "tableSession",
      ready: true,
      userMessage: "请先完成开台后再发起挑战"
    }
  ],
  unavailableMessage: "请在店内开台后再发起挑战"
};

const roomState = {
  roomNo: "YH-T03-0527",
  tableNo: "T03",
  status: "waiting",
  statusText: "等待对手加入",
  statusHint: "让对手扫描球桌码加入本场挑战",
  expiresText: "房间 10 分钟内有效",
  opponentJoined: false,
  host: match.playerA
};

const incomingChallenge = {
  roomNo: "YH-T03-0527",
  tableNo: "T03",
  dueTime: "22:30",
  statusText: "待确认",
  host: match.playerA,
  challenger: match.playerB,
  acceptHint: "接受后进入玩法选择，双方确认底分和倍率后才开始计分。",
  rejectHint: "拒绝后不会产生积分变化。"
};

const rankingRows = [
  { id: "r1", no: 1, name: "泰森练练", rank: "走位黄金 III", points: 3560, trend: "+5" },
  { id: "r2", no: 2, name: "文哥 GG", rank: "推杆白银 II", points: 3240, trend: "+3" },
  { id: "r3", no: 3, name: "刘战平", rank: "沉稳青铜 I", points: 3100, trend: "+2" },
  { id: "r4", no: 4, name: "孙总", rank: "推杆白银 II", points: 2860, trend: "+1" },
  { id: "r5", no: 5, name: "Jackson", rank: "沉稳青铜 I", points: 2780, trend: "0" }
];

const sameRankRows = [
  { id: "s1", no: 1, name: "泰森练练", rank: "走位黄金 III", points: 3560, trend: "+5" },
  { id: "s2", no: 2, name: "云瀚-阿杰", rank: "走位黄金 III", points: 2860, trend: "+2" },
  { id: "s3", no: 3, name: "小北", rank: "走位黄金 III", points: 2710, trend: "+1" },
  { id: "s4", no: 4, name: "阿豪", rank: "走位黄金 III", points: 2520, trend: "0" }
];

const friendRows = [
  { id: "f1", no: 1, name: "云瀚-阿杰", rank: "走位黄金 III", points: 2860, trend: "+2" },
  { id: "f2", no: 2, name: "台球小宇", rank: "沉稳青铜 I", points: 2420, trend: "+1" },
  { id: "f3", no: 3, name: "阿泽", rank: "推杆白银 I", points: 2310, trend: "0" }
];

const playerStats = {
  seasonWinRate: "68%",
  validMatches: 24,
  winStreak: 3,
  storeRank: 4,
  sameRankRank: 2,
  friendRank: 1,
  bestStreak: 6
};

const pointsPerks = {
  exchangeThreshold: 1000,
  tableOpenBonus: 30,
  nextRewardText: "可到前台兑换饮品或台费券",
  counterHint: "到前台出示会员码，工作人员核销积分后发放礼遇。"
};

const staffTables = [
  { id: "T01", name: "T01", dueTime: "21:30", status: "进行中", roomCount: 1 },
  { id: "T02", name: "T02", dueTime: "22:00", status: "空台", roomCount: 0 },
  { id: "T03", name: "T03", dueTime: "22:30", status: "挑战中", roomCount: 1 },
  { id: "T05", name: "T05", dueTime: "23:00", status: "进行中", roomCount: 0 }
];

const staffExchangeUser = {
  name: "云瀚-阿杰",
  points: 2860,
  lastVisit: "今日已开台"
};

const abnormalMatches = [
  { id: "A01", tableNo: "T03", title: "不服待处理", detail: "双方可退出本场或再战", time: "21:48" },
  { id: "A02", tableNo: "T01", title: "盘数修正", detail: "等待前台确认备注", time: "20:35" }
];

const adminConfig = {
  modes: modes.map((mode) => ({
    ...mode,
    baseText: mode.baseOptions.join(" / "),
    multiplierText: `x1 - x${mode.multipliers[mode.multipliers.length - 1]}`
  })),
  points: {
    newUser: 300,
    checkIn: 0,
    tableOpenBonus: 30,
    exchangeThreshold: 1000
  },
  antiCheat: {
    geoFence: "100 米",
    storeLatitude: "",
    storeLongitude: "",
    tableDueRequired: "必须设置",
    minimumTimeRequired: "必须满足"
  },
  screen: {
    storeBoard: "店内总榜",
    bountyBoard: "赏金猎人",
    refreshText: "60 秒刷新"
  }
};

const bountyRows = [
  { id: "b1", no: 1, name: "刘战平", rank: "沉稳青铜 I", points: 620, trend: "+180" },
  { id: "b2", no: 2, name: "泰森练练", rank: "走位黄金 III", points: 540, trend: "+150" },
  { id: "b3", no: 3, name: "孙总", rank: "推杆白银 II", points: 410, trend: "+120" },
  { id: "b4", no: 4, name: "台球小宇", rank: "沉稳青铜 I", points: 320, trend: "+90" }
];

module.exports = {
  modes,
  match,
  challengeGate,
  roomState,
  incomingChallenge,
  getModeById,
  buildMatchSetup,
  buildSettlement,
  rankingRows,
  sameRankRows,
  friendRows,
  playerStats,
  pointsPerks,
  staffTables,
  staffExchangeUser,
  abnormalMatches,
  adminConfig,
  bountyRows,
  topRows: rankingRows.slice(0, 3)
};
