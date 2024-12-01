<!-- src/components/CheatsheetList.vue -->

<template>
  <div>
    <h1>Cheat Sheets</h1>
    <ul class="list-group">
      <li v-for="cheatsheet in cheatsheets" :key="cheatsheet" class="list-group-item d-flex justify-content-between align-items-center">
        <router-link :to="`/cheatsheet/${cheatsheet}`">{{ cheatsheet }}</router-link>
        <div>
          <router-link :to="`/cheatsheet/${cheatsheet}/edit`" class="btn btn-sm btn-primary me-2">Edit</router-link>
          <button @click="deleteCheatsheet(cheatsheet)" class="btn btn-sm btn-danger">Delete</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CheatsheetList',
  data() {
    return {
      cheatsheets: []
    };
  },
  methods: {
    fetchCheatsheets() {
      axios.get('/api/cheatsheets')
        .then(response => {
          this.cheatsheets = response.data.cheatsheets;
        })
        .catch(error => {
          console.error('Error fetching cheat sheets:', error);
        });
    },
    deleteCheatsheet(name) {
      if (confirm(`Are you sure you want to delete '${name}'?`)) {
        axios.delete(`/api/cheatsheets/${name}`)
          .then(() => {
            this.fetchCheatsheets();
          })
          .catch(error => {
            console.error('Error deleting cheat sheet:', error);
          });
      }
    }
  },
  created() {
    this.fetchCheatsheets();
  }
};
</script>

<style scoped>
.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

