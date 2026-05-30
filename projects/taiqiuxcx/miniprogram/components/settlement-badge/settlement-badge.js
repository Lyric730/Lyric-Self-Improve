const SETTLEMENT_ASSETS = {
  rankUp: "/assets/ui-kit/settlement-rank-up-card.png",
  plus: "/assets/ui-kit/settlement-points-plus.png",
  minus: "/assets/ui-kit/settlement-points-minus.png",
  reward: "/assets/ui-kit/settlement-reward-card.png"
};

Component({
  properties: {
    variant: {
      type: String,
      value: "plus",
      observer: "resolveAsset"
    },
    label: {
      type: String,
      value: "+180 积分"
    }
  },

  data: {
    assetSrc: SETTLEMENT_ASSETS.plus
  },

  lifetimes: {
    attached() {
      this.resolveAsset();
    }
  },

  methods: {
    resolveAsset() {
      this.setData({
        assetSrc: SETTLEMENT_ASSETS[this.properties.variant] || SETTLEMENT_ASSETS.plus
      });
    }
  }
});
