<script setup lang="ts">
// 讲义中心：章节列表 + 阅读进度
import { RouterLink } from 'vue-router'
import { CHAPTERS } from '../data/chapters'
import { useArchive } from '../stores/archive'
import { PLAYABLE } from '../data/bank'

const archive = useArchive()
const countOf = (id: string) => PLAYABLE.filter((q) => q.chapter === id).length
</script>

<template>
  <div>
    <h1>讲义中心</h1>
    <p class="muted">14 章考点精讲。读一章、标一章、练一章。</p>
    <div class="chgrid">
      <RouterLink
        v-for="c in CHAPTERS"
        :key="c.id"
        :to="`/notes/${c.id}`"
        class="card hoverable chcard"
      >
        <div class="cover">
          <img :src="`./art/${c.id}.png`" :alt="`${c.title} 封面`" loading="lazy" />
          <span v-if="archive.data.noteProgress[c.id]?.done" class="done-tag">✓ 已读完</span>
        </div>
        <div class="chbody">
          <div class="chhead">
            <span class="chno">{{ c.id.replace('ch', '') }}</span>
            <span class="pill">{{ c.weight }} 分值</span>
          </div>
          <h3>{{ c.title }}</h3>
          <div class="small muted">{{ c.subtitle }}</div>
          <div class="kps">
            <span v-for="k in c.keyPoints.slice(0, 3)" :key="k" class="kp">{{ k }}</span>
          </div>
          <div class="small muted">配套练习 {{ countOf(c.id) }} 题</div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.chgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 16px; }
@media (max-width: 960px) { .chgrid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .chgrid { grid-template-columns: 1fr; } }
.chcard { display: block; color: inherit; padding: 0; overflow: hidden; }
.chcard:hover { text-decoration: none; }
.cover { position: relative; aspect-ratio: 16 / 9; background: var(--bg); }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.done-tag {
  position: absolute; top: 8px; right: 8px;
  background: var(--accent); color: #fff;
  font-size: 11px; padding: 2px 8px; border-radius: 999px;
}
.chbody { padding: 12px 16px 14px; }
.chhead { display: flex; gap: 6px; align-items: center; margin-bottom: 4px; }
.chno {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
  width: 26px;
}
.chcard h3 { margin: 2px 0 4px; }
.kps { margin: 8px 0; display: flex; flex-wrap: wrap; gap: 5px; }
.kp {
  font-size: 11px;
  background: var(--bg);
  border: 1px solid var(--line);
  padding: 1px 7px;
  border-radius: 999px;
  color: var(--ink-2);
}
</style>
