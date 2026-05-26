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
    riskPoints: 300,
    baseItems: [],
    multiplierItems: []
  },

  observers: {
    "baseOptions, multipliers, selectedBase, selectedMultiplier": function syncAll(
      baseOptions,
      multipliers,
      selectedBase,
      selectedMultiplier
    ) {
      this.syncOptions(baseOptions, multipliers, selectedBase, selectedMultiplier);
    }
  },

  lifetimes: {
    attached() {
      this.syncOptions(
        this.properties.baseOptions,
        this.properties.multipliers,
        this.properties.selectedBase,
        this.properties.selectedMultiplier
      );
    }
  },

  methods: {
    syncOptions(baseOptions, multipliers, selectedBase, selectedMultiplier) {
      const currentBase = Number(selectedBase || 0);
      const currentMultiplier = Number(selectedMultiplier || 0);

      this.setData({
        riskPoints: currentBase * currentMultiplier,
        baseItems: (Array.isArray(baseOptions) ? baseOptions : []).map((value) => ({
          value,
          selected: Number(value) === currentBase
        })),
        multiplierItems: (Array.isArray(multipliers) ? multipliers : []).map((value) => ({
          value,
          selected: Number(value) === currentMultiplier
        }))
      });
    },

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
