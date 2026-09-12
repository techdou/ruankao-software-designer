<script setup lang="ts">
// 成就徽章墙：打卡 / 刷题量 / 正确率 / 毕业
import { computed } from 'vue'
import { useArchive } from '../stores/archive'
import { CHAPTERS } from '../data/chapters'

const archive = useArchive()

interface Badge {
  key: string
  name: string
  desc: string
  got: boolean
  progress: number   // 0-1，未达成时显示进度
}

const badges = computed<Badge[]>(() => {
  const d = archive.data
  const best = Math.max(d.streak.best ?? 0, d.streak.days)
  const done = archive.doneCount
  const acc = done ? archive.correctCount / done : 0
  const notesDone = CHAPTERS.filter((c) => d.noteProgress[c.id]?.done).length
  return [
    { key: 'badge-streak-3', name: '星火', desc: '连续学习 3 天', got: best >= 3, progress: Math.min(1, best / 3) },
    { key: 'badge-streak-7', name: '燎原', desc: '连续学习 7 天', got: best >= 7, progress: Math.min(1, best / 7) },
    { key: 'badge-streak-21', name: '习惯成钢', desc: '连续学习 21 天', got: best >= 21, progress: Math.min(1, best / 21) },
    { key: 'badge-q100', name: '百题斩', desc: '累计刷题 100 题', got: done >= 100, progress: Math.min(1, done / 100) },
    { key: 'badge-q300', name: '题海遨游', desc: '累计刷题 300 题', got: done >= 300, progress: Math.min(1, done / 300) },
    { key: 'badge-q500', name: '题库通吃', desc: '累计刷题 500 题', got: done >= 500, progress: Math.min(1, done / 500) },
    { key: 'badge-acc80', name: '神射手', desc: '刷满 100 题且正确率 ≥80%', got: done >= 100 && acc >= 0.8, progress: done >= 100 ? Math.min(1, acc / 0.8) : done / 100 },
    { key: 'badge-graduate', name: '满腹经纶', desc: '14 章讲义全部读完', got: notesDone >= CHAPTERS.length, progress: notesDone / CHAPTERS.length },
  ]
})

const gotCount = computed(() => badges.value.filter((b) => b.got).length)
</script>

<template>
  <div class="card ach">
    <div class="head">
      <b>成就徽章</b>
      <span class="muted small">{{ gotCount }} / {{ badges.length }}</span>
    </div>
    <div class="grid">
      <div
        v-for="b in badges"
        :key="b.key"
        class="badge"
        :class="{ got: b.got }"
        :title="b.desc"
      >
        <div class="pic">
          <img v-if="b.got" :src="`./art/${b.key}.png`" :alt="b.name" loading="lazy" />
          <div v-else class="lock">
            <div class="ring" :style="{ '--p': b.progress * 100 + '%' }" />
            <span class="pct">{{ Math.round(b.progress * 100) }}%</span>
          </div>
        </div>
        <div class="name">{{ b.got ? b.name : '？？？' }}</div>
        <div class="desc">{{ b.desc }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ach { margin-top: 18px; }
.head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
@media (max-width: 860px) { .grid { grid-template-columns: repeat(2, 1fr); } }
.badge { text-align: center; padding: 10px 6px; border-radius: var(--radius); }
.badge:not(.got) { opacity: 0.85; }
.pic { width: 84px; height: 84px; margin: 0 auto 8px; position: relative; }
.pic img { width: 100%; height: 100%; object-fit: contain; }
.lock {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  position: relative;
  background: var(--bg);
  border-radius: 50%;
}
.ring {
  position: absolute; inset: 0;
  border-radius: 50%;
  background: conic-gradient(var(--accent) var(--p), var(--line) 0);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 6px), #000 calc(100% - 5px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 6px), #000 calc(100% - 5px));
}
.pct { font-size: 13px; font-weight: 700; color: var(--ink-3); }
.name { font-weight: 700; font-size: 13px; }
.badge.got .name { color: var(--accent); }
.desc { font-size: 11px; color: var(--ink-3); margin-top: 2px; }
</style>
