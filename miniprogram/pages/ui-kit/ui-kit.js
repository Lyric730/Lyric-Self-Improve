Page({
  data: {
    selectedMode: "race5",
    selectedBase: 100,
    selectedMultiplier: 3,
    selectorBaseOptions: [50, 100, 200],
    selectorMultipliers: [1, 2, 3, 5],
    modes: [
      {
        modeId: "race5",
        name: "抢5",
        targetWins: 5,
        minimumMinutes: 40,
        baseOptions: [20, 50, 100],
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
        starReward: 3,
        enabled: false,
        tag: "预留"
      }
    ]
  },

  handleModeSelect(event) {
    this.setData({
      selectedMode: event.detail.modeId
    });
  },

  handlePointChange(event) {
    this.setData({
      selectedBase: event.detail.selectedBase,
      selectedMultiplier: event.detail.selectedMultiplier
    });
  },

  noop() {}
});
