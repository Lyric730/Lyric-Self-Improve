Component({
  properties: {
    baseOptions: {
      type: Array,
      value: []
    },
    multipliers: {
      type: Array,
      value: []
    },
    selectedBase: {
      type: Number,
      value: 100
    },
    selectedMultiplier: {
      type: Number,
      value: 3
    },
    rewardRange: {
      type: String,
      value: "80 ~ 150"
    },
    sprintRewardRange: {
      type: String,
      value: "200 ~ 300"
    }
  },

  data: {
    riskPoints: 300
  },

  observers: {
    "selectedBase, selectedMultiplier": function updateRiskPoints(base, multiplier) {
      this.setData({
        riskPoints: Number(base || 0) * Number(multiplier || 0)
      });
    }
  },

  methods: {
    selectBase(event) {
      const selectedBase = Number(event.currentTarget.dataset.value);
      this.triggerEvent("change", {
        selectedBase,
        selectedMultiplier: this.properties.selectedMultiplier
      });
    },

    selectMultiplier(event) {
      const selectedMultiplier = Number(event.currentTarget.dataset.value);
      this.triggerEvent("change", {
        selectedBase: this.properties.selectedBase,
        selectedMultiplier
      });
    }
  }
});
