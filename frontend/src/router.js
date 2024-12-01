// src/router.js

import { createRouter, createWebHistory } from 'vue-router';
import CheatsheetList from './components/CheatsheetList.vue';
import Cheatsheet from './components/Cheatsheet.vue';
import Editor from './components/Editor.vue';

const routes = [
  { path: '/', component: CheatsheetList },
  { path: '/cheatsheet/:name', component: Cheatsheet, props: true },
  { path: '/cheatsheet/:name/edit', component: Editor, props: true },
  { path: '/create', component: Editor }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

