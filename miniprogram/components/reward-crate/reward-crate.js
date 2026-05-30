Component({
  properties: {
    type: {
      type: String,
      value: "normal",
      observer: "resolveAsset"
    },
    title: {
      type: String,
      value: "随机奖励"
    },
    range: {
      type: String,
      value: "80 ~ 150 积分"
    },
    subtitle: {
      type: String,
      value: "双方同享，结算后发放"
    }
  },

  data: {
    assetSrc: "/assets/ui-kit/reward-crate-normal.png"
  },

  lifetimes: {
    attached() {
      this.resolveAsset();
    }
  },

  methods: {
    resolveAsset() {
      const src = this.properties.type === "sprint"
        ? "/assets/ui-kit/reward-crate-sprint.png"
        : "/assets/ui-kit/reward-crate-normal.png";
      this.setData({ assetSrc: src });
    }
  }
});
