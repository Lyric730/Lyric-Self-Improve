Component({
  externalClasses: ["custom-class"],

  properties: {
    text: {
      type: String,
      value: ""
    },
    variant: {
      type: String,
      value: "primary"
    },
    size: {
      type: String,
      value: "md"
    },
    icon: {
      type: String,
      value: ""
    },
    iconOnly: {
      type: Boolean,
      value: false
    },
    block: {
      type: Boolean,
      value: false
    },
    disabled: {
      type: Boolean,
      value: false
    },
    loading: {
      type: Boolean,
      value: false
    }
  },

  methods: {
    handleTap() {
      if (this.data.disabled || this.data.loading) return;
      this.triggerEvent("tap");
    }
  }
});
