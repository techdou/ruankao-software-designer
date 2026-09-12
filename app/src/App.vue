<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const navs = [
  { to: '/', label: '仪表盘', icon: '◧' },
  { to: '/notes', label: '讲义', icon: '书' },
  { to: '/drill', label: '刷题', icon: '练' },
  { to: '/papers', label: '真题', icon: '卷' },
  { to: '/exam', label: '模考', icon: '考' },
  { to: '/cases', label: '案例', icon: '案' },
  { to: '/wrong', label: '错题', icon: '错' },
  { to: '/favorites', label: '收藏', icon: '藏' },
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

    <!-- 移动端底部导航 -->
    <nav class="bottomnav">
      <RouterLink
        v-for="n in navs"
        :key="n.to"
        :to="n.to"
        class="bn-item"
        :class="{ active: isActive(n.to) }"
      >
        <span class="bn-icon" aria-hidden="true">{{ n.icon }}</span>
        <span class="bn-label">{{ n.label }}</span>
      </RouterLink>
    </nav>
  </div>
</template>

<style scoped>
.layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 200px;
  flex: none;
  border-right: 1px solid var(--line);
  background: var(--surface);
  padding: 18px 12px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.sidebar .logo {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 17px;
  padding: 4px 10px 14px;
  letter-spacing: 1px;
}
.sidebar .logo small { display: block; font-size: 11px; color: var(--ink-3); font-weight: 400; letter-spacing: 0; }
.nav-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 10px;
  border-radius: var(--radius);
  color: var(--ink-2);
  margin: 1px 0;
}
.nav-item:hover { background: var(--bg); color: var(--ink); text-decoration: none; }
.nav-item.active { background: var(--accent-weak); color: var(--accent); font-weight: 600; }
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
.main { flex: 1; min-width: 0; padding: 26px 32px 60px; max-width: 1080px; }

.bottomnav { display: none; }

/* ---- 移动端：侧栏变底部导航 ---- */
@media (max-width: 860px) {
  .sidebar { display: none; }
  .main { padding: 16px 14px calc(78px + env(safe-area-inset-bottom, 0px)); }
  .bottomnav {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 50;
    background: var(--surface);
    border-top: 1px solid var(--line);
    padding: 5px 4px calc(5px + env(safe-area-inset-bottom, 0px));
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .bottomnav::-webkit-scrollbar { display: none; }
  .bn-item {
    flex: 1 0 52px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 3px 2px;
    border-radius: var(--radius);
    color: var(--ink-3);
    font-size: 10px;
    min-height: 46px;
    justify-content: center;
  }
  .bn-item:hover { text-decoration: none; }
  .bn-item.active { color: var(--accent); background: var(--accent-weak); }
  .bn-icon {
    width: 26px;
    height: 26px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    border: 1px solid currentColor;
    border-radius: 6px;
  }
}
</style>
