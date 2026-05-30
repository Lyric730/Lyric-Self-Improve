const RANK_ASSETS = {
  bronze: "/assets/ui-kit/rank-bronze.png",
  silver: "/assets/ui-kit/rank-silver.png",
  gold: "/assets/ui-kit/rank-gold.png",
  goldFeatured: "/assets/ui-kit/rank-gold-iii-featured.png",
  platinum: "/assets/ui-kit/rank-platinum.png",
  diamond: "/assets/ui-kit/rank-diamond.png",
  starGlory: "/assets/ui-kit/rank-star-glory.png",
  king: "/assets/ui-kit/rank-king.png"
};

Component({
  properties: {
    tier: {
      type: String,
      value: "gold",
      observer: "resolveAsset"
    },
    title: {
      type: String,
      value: "走位黄金 III"
    },
    points: {
      type: String,
      value: "2860 / 3000"
    },
    hint: {
      type: String,
      value: "再得 140 分升至走位黄金 II"
    },
    featured: {
      type: Boolean,
      value: false,
      observer: "resolveAsset"
    }
  },

  data: {
    assetSrc: RANK_ASSETS.gold
  },

  lifetimes: {
    attached() {
      this.resolveAsset();
    }
  },

  methods: {
    resolveAsset() {
      const { tier, featured } = this.properties;
      const key = featured && tier === "gold" ? "goldFeatured" : tier;
      this.setData({
        assetSrc: RANK_ASSETS[key] || RANK_ASSETS.gold
      });
    }
  }
});
