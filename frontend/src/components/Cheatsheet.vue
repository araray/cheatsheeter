<!-- src/components/Cheatsheet.vue -->

<template>
  <div>
    <h1>{{ cheatsheet.data.title }}</h1>
    <div v-for="category in cheatsheet.data.categories" :key="category.name">
      <h3>{{ category.name }}</h3>
      <ul class="list-group mb-3">
        <li v-for="item in category.items" :key="item.command" class="list-group-item">
          <strong>{{ item.command }}</strong>: {{ item.description }}
        </li>
      </ul>
    </div>
    <router-link :to="`/cheatsheet/${cheatsheet.name}/edit`" class="btn btn-primary">Edit</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Cheatsheet',
  props: ['name'],
  data() {
    return {
      cheatsheet: {
        name: '',
        data: {
          title: '',
          categories: []
        }
      }
    };
  },
  methods: {
    fetchCheatsheet() {
      axios.get(`/api/cheatsheets/${this.name}`)
        .then(response => {
          this.cheatsheet = response.data;
        })
        .catch(error => {
          console.error('Error fetching cheat sheet:', error);
        });
    }
  },
  created() {
    this.fetchCheatsheet();
  }
};
</script>

<style scoped>
</style>

