Component({
  externalClasses: ["custom-class"],

  properties: {
    modeId: {
      type: String,
      value: ""
    },
    name: {
      type: String,
      value: "抢5"
    },
    targetWins: {
      type: Number,
      value: 5
    },
    minimumMinutes: {
      type: Number,
      value: 40
    },
    baseOptions: {
      type: Array,
      value: [20, 50, 100],
      observer: "syncBaseText"
    },
    starReward: {
      type: Number,
      value: 1
    },
    selected: {
      type: Boolean,
      value: false
    },
    enabled: {
      type: Boolean,
      value: true
    },
    tag: {
      type: String,
      value: ""
    }
  },

  data: {
    baseText: "20 / 50 / 100"
  },

  lifetimes: {
    attached() {
      this.syncBaseText(this.data.baseOptions);
    }
  },

  methods: {
    syncBaseText(value) {
      const options = Array.isArray(value) ? value : [];
      this.setData({
        baseText: options.join(" / ")
      });
    },

    handleSelect() {
      if (!this.data.enabled) return;
      this.triggerEvent("select", {
        modeId: this.data.modeId
      });
    }
  }
});
