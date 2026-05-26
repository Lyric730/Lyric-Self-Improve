Component({
  properties: {
    title: {
      type: String,
      value: "随机奖励"
    },
    normalRange: {
      type: String,
      value: "80 ~ 150"
    },
    sprintRange: {
      type: String,
      value: "200 ~ 300"
    },
    currentStage: {
      type: Number,
      value: 4
    },
    cycleLabel: {
      type: String,
      value: "第 4 大局"
    },
    dueLabel: {
      type: String,
      value: "临近到点"
    },
    boostPercent: {
      type: Number,
      value: 200
    }
  },

  data: {
    stageItems: []
  },

  lifetimes: {
    attached() {
      this.buildStages();
    }
  },

  observers: {
    "currentStage": function () {
      this.buildStages();
    }
  },

  methods: {
    buildStages() {
      const current = Math.max(1, Math.min(Number(this.data.currentStage) || 1, 4));
      const labels = ["第1局", "第2局", "第3局", "冲刺局"];

      this.setData({
        stageItems: labels.map((label, index) => {
          const stage = index + 1;
          const active = stage <= current;
          const sprint = stage === 4;

          return {
            stage,
            label,
            active,
            sprint,
            className: [
              active ? "is-active" : "",
              sprint ? "is-sprint" : "",
              stage === current ? "is-current" : ""
            ].join(" ")
          };
        })
      });
    },

    switchStage(event) {
      const stage = Number(event.currentTarget.dataset.stage) || 1;
      this.setData({ currentStage: stage });
      this.triggerEvent("stagechange", { currentStage: stage });
    }
  }
});
