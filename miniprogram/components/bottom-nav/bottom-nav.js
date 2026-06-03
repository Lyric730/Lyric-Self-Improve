Component({
  properties: {
    active: {
      type: String,
      value: "challenge"
    }
  },

  data: {
    items: [
      { id: "challenge", label: "挑战", icon: "战", url: "/pages/challenge-home/challenge-home" },
      { id: "data", label: "数据", icon: "数", url: "/pages/my-data/my-data" },
      { id: "rankings", label: "排行", icon: "榜", url: "/pages/rankings/rankings" },
      { id: "points", label: "积分", icon: "分", url: "/pages/points-perks/points-perks" },
      { id: "mine", label: "我的", icon: "我", url: "/pages/my-hub/my-hub" }
    ]
  },

  methods: {
    handleTap(event) {
      const { id, url } = event.currentTarget.dataset;

      if (id === this.data.active) {
        return;
      }

      if (id === "challenge") {
        wx.reLaunch({ url });
        return;
      }

      wx.redirectTo({ url });
    }
  }
});
