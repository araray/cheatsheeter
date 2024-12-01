<!-- src/components/Editor.vue -->

<template>
  <div>
    <h1>{{ isEditMode ? 'Edit' : 'Create' }} Cheat Sheet</h1>
    <form @submit.prevent="saveCheatsheet">
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input v-model="cheatsheet.name" type="text" class="form-control" id="name" :readonly="isEditMode" required />
      </div>
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input v-model="cheatsheet.data.title" type="text" class="form-control" id="title" required />
      </div>
      <div v-for="(category, index) in cheatsheet.data.categories" :key="index" class="mb-3">
        <label class="form-label">Category Name</label>
        <input v-model="category.name" type="text" class="form-control mb-2" required />
        <div v-for="(item, idx) in category.items" :key="idx" class="mb-2">
          <div class="input-group">
            <input v-model="item.command" type="text" class="form-control" placeholder="Command" required />
            <input v-model="item.description" type="text" class="form-control" placeholder="Description" required />
            <button @click="removeItem(index, idx)" type="button" class="btn btn-danger">Remove</button>
          </div>
        </div>
        <button @click="addItem(index)" type="button" class="btn btn-secondary btn-sm">Add Item</button>
        <hr />
      </div>
      <button @click="addCategory" type="button" class="btn btn-secondary">Add Category</button>
      <button type="submit" class="btn btn-primary ms-2">Save</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Editor',
  props: ['name'],
  data() {
    return {
      isEditMode: false,
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
          this.isEditMode = true;
        })
        .catch(error => {
          console.error('Error fetching cheat sheet:', error);
        });
    },
    saveCheatsheet() {
      const method = this.isEditMode ? 'put' : 'post';
      const url = this.isEditMode ? `/api/cheatsheets/${this.cheatsheet.name}` : '/api/cheatsheets';
      axios[method](url, this.cheatsheet)
        .then(() => {
          this.$router.push(`/cheatsheet/${this.cheatsheet.name}`);
        })
        .catch(error => {
          console.error('Error saving cheat sheet:', error);
        });
    },
    addCategory() {
      this.cheatsheet.data.categories.push({ name: '', items: [] });
    },
    addItem(categoryIndex) {
      this.cheatsheet.data.categories[categoryIndex].items.push({ command: '', description: '' });
    },
    removeItem(categoryIndex, itemIndex) {
      this.cheatsheet.data.categories[categoryIndex].items.splice(itemIndex, 1);
    }
  },
  created() {
    if (this.name) {
      this.fetchCheatsheet();
    }
  }
};
</script>

<style scoped>
.input-group {
  margin-bottom: 5px;
}
</style>

