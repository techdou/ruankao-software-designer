import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'

export const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: Dashboard },
    { path: '/notes', name: 'notes', component: () => import('./views/Notes.vue') },
    { path: '/notes/:id', name: 'note', component: () => import('./views/NoteReader.vue') },
    { path: '/drill', name: 'drill', component: () => import('./views/Drill.vue') },
    { path: '/papers', name: 'papers', component: () => import('./views/Papers.vue') },
    { path: '/exam', name: 'exam', component: () => import('./views/Exam.vue') },
    { path: '/cases', name: 'cases', component: () => import('./views/Cases.vue') },
    { path: '/wrong', name: 'wrong', component: () => import('./views/WrongBook.vue') },
    { path: '/favorites', name: 'favorites', component: () => import('./views/Favorites.vue') },
    { path: '/stats', name: 'stats', component: () => import('./views/Stats.vue') },
    { path: '/settings', name: 'settings', component: () => import('./views/Settings.vue') },
  ],
})
