Component({
  properties: {
    value: {
      type: Number,
      value: 3,
      observer: "buildStars"
    },
    total: {
      type: Number,
      value: 5,
      observer: "buildStars"
    },
    mode: {
      type: String,
      value: "new",
      observer: "buildStars"
    }
  },

  data: {
    stars: []
  },

  lifetimes: {
    attached() {
      this.buildStars();
    }
  },

  methods: {
    buildStars() {
      const { value, total, mode } = this.properties;
      const safeTotal = Math.max(total, 1);
      const safeValue = Math.min(Math.max(value, 0), safeTotal);
      const stars = Array.from({ length: safeTotal }).map((_, index) => {
        const position = index + 1;
        let state = position <= safeValue ? "earned" : "empty";

        if (mode === "new" && position === safeValue) {
          state = "new";
        }

        if (mode === "protected" && position === safeValue) {
          state = "protected";
        }

        if (mode === "lost" && position === safeValue + 1) {
          state = "lost";
        }

        return {
          id: `star-${position}`,
          state,
          label: state === "empty" ? "☆" : "★"
        };
      });

      this.setData({ stars });
    }
  }
});
