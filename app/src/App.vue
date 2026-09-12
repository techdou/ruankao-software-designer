<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const navs = [
  { to: '/', label: '仪表盘', icon: '◧' },
  { to: '/notes', label: '讲义中心', icon: '书' },
  { to: '/drill', label: '刷题练习', icon: '练' },
  { to: '/papers', label: '真题套卷', icon: '卷' },
  { to: '/exam', label: '模拟考试', icon: '考' },
  { to: '/cases', label: '案例题', icon: '案' },
  { to: '/wrong', label: '错题本', icon: '错' },
  { to: '/favorites', label: '收藏夹', icon: '藏' },
  { to: '/stats', label: '统计', icon: '析' },
  { to: '/settings', label: '存档', icon: '档' },
] as const

const isActive = (to: string) =>
  to === '/' ? route.path === '/' : route.path.startsWith(to)
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">软设备考<small>软件设计师 · 互动学习站</small></div>
      <RouterLink
        v-for="n in navs"
        :key="n.to"
        :to="n.to"
        class="nav-item"
        :class="{ active: isActive(n.to) }"
      >
        <span class="nav-icon" aria-hidden="true">{{ n.icon }}</span>
        <span class="nav-label">{{ n.label }}</span>
      </RouterLink>
    </aside>
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.nav-icon {
  width: 22px;
  height: 22px;
  flex: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  border: 1px solid currentColor;
  border-radius: 5px;
  opacity: 0.75;
}
.nav-item.active .nav-icon { opacity: 1; }
</style>
