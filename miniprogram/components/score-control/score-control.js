Component({
  properties: {
    playerAName: {
      type: String,
      value: "云瀚·阿杰"
    },
    playerBName: {
      type: String,
      value: "台球小宇"
    },
    scoreA: {
      type: Number,
      value: 5
    },
    scoreB: {
      type: Number,
      value: 3
    },
    targetWins: {
      type: Number,
      value: 5
    },
    currentRack: {
      type: Number,
      value: 8
    },
    dueTime: {
      type: String,
      value: "22:30"
    },
    elapsedLabel: {
      type: String,
      value: "00:28:35"
    },
    minimumLabel: {
      type: String,
      value: "40:00"
    },
    remainingLabel: {
      type: String,
      value: "11:25"
    },
    timerTone: {
      type: String,
      value: "warning"
    }
  },

  data: {
    localScoreA: 5,
    localScoreB: 3,
    rackLabel: "2 : 1",
    settleLabel: "时间未满"
  },

  observers: {
    "scoreA, scoreB, currentRack, targetWins": function syncScore(scoreA, scoreB, currentRack, targetWins) {
      this.setData({
        localScoreA: Number(scoreA || 0),
        localScoreB: Number(scoreB || 0),
        rackLabel: this.buildRackLabel(currentRack),
        settleLabel: this.buildSettleLabel(scoreA, scoreB, targetWins)
      });
    }
  },

  lifetimes: {
    attached() {
      this.setData({
        localScoreA: this.properties.scoreA,
        localScoreB: this.properties.scoreB,
        rackLabel: this.buildRackLabel(this.properties.currentRack),
        settleLabel: this.buildSettleLabel(
          this.properties.scoreA,
          this.properties.scoreB,
          this.properties.targetWins
        )
      });
    }
  },

  methods: {
    buildRackLabel(currentRack) {
      const rack = Math.max(Number(currentRack || 1), 1);
      const left = Math.max(Math.ceil(rack / 2), 1);
      const right = Math.max(Math.floor(rack / 2), 0);
      return `${left} : ${right}`;
    },

    buildSettleLabel(scoreA, scoreB, targetWins) {
      const target = Number(targetWins || 0);
      if (Number(scoreA || 0) >= target || Number(scoreB || 0) >= target) return "已达胜盘";
      return "比赛进行中";
    },

    changeScore(side, delta) {
      const key = side === "a" ? "localScoreA" : "localScoreB";
      const next = Math.max(Number(this.data[key] || 0) + delta, 0);
      this.setData({
        [key]: next,
        settleLabel: this.buildSettleLabel(
          side === "a" ? next : this.data.localScoreA,
          side === "b" ? next : this.data.localScoreB,
          this.properties.targetWins
        )
      });
      this.triggerEvent("scorechange", {
        side,
        scoreA: side === "a" ? next : this.data.localScoreA,
        scoreB: side === "b" ? next : this.data.localScoreB
      });
    },

    increaseA() {
      this.changeScore("a", 1);
    },

    decreaseA() {
      this.changeScore("a", -1);
    },

    increaseB() {
      this.changeScore("b", 1);
    },

    decreaseB() {
      this.changeScore("b", -1);
    }
  }
});
