<!-- src/components/ThemeSelector.vue -->

<template>
  <div class="theme-selector">
    <label for="themeSelect" class="form-label me-2">Theme:</label>
    <select id="themeSelect" class="form-select" @change="changeTheme($event)">
      <option v-for="theme in themes" :key="theme.value" :value="theme.value">
        {{ theme.name }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "ThemeSelector",
  data() {
    return {
      themes: [
        { name: "Default", value: "default" },
        { name: "Dark", value: "dark" },
      ],
    };
  },
  methods: {
    changeTheme(event) {
      const themeName = event.target.value;
      const themeLink = document.getElementById("theme-link");
      themeLink.href = `assets/themes/${themeName}.css`; // Adjusted path
    },
  },
};
</script>

<style scoped>
.theme-selector {
  display: flex;
  align-items: center;
}
</style>
