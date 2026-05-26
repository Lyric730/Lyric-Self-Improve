Component({
  externalClasses: ["custom-class"],

  properties: {
    title: {
      type: String,
      value: ""
    },
    subtitle: {
      type: String,
      value: ""
    },
    marker: {
      type: String,
      value: ""
    },
    tone: {
      type: String,
      value: "default"
    },
    cut: {
      type: Boolean,
      value: true
    },
    raised: {
      type: Boolean,
      value: false
    }
  }
});
