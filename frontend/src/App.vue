<!-- src/App.vue -->

<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Cheat Sheet Tool</router-link>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/create">Create Cheat Sheet</router-link>
            </li>
          </ul>
          <ThemeSelector />
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import ThemeSelector from './components/ThemeSelector.vue';

export default {
  name: 'App',
  components: {
    ThemeSelector
  }
};
</script>

<style>
/* Global styles can go here */
</style>

