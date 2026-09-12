<script setup lang="ts">
// 统计：章节正确率 + 近 30 天刷题量 + 待复习分布
import { computed } from 'vue'
import { useArchive } from '../stores/archive'
import { CHAPTERS } from '../data/chapters'
import { PLAYABLE } from '../data/bank'

const archive = useArchive()

const chapters = computed(() =>
  CHAPTERS.map((ch) => {
    const qs = PLAYABLE.filter((q) => q.chapter === ch.id)
    const done = qs.filter((q) => archive.attempts[q.id])
    const ok = done.filter((q) => archive.attempts[q.id].correct)
    return { ...ch, total: qs.length, done: done.length, acc: done.length ? ok.length / done.length : null }
  }).sort((a, b) => (b.acc ?? -1) - (a.acc ?? -1)),
)

const daily = computed(() => {
  const days: { date: string; n: number; ok: number }[] = []
  for (let i = 29; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    const key = d.toISOString().slice(0, 10)
    days.push({ date: key, n: 0, ok: 0 })
  }
  const map = new Map(days.map((d) => [d.date, d]))
  for (const h of archive.data.history) {
    const day = map.get(h.at.slice(0, 10))
    if (day) {
      day.n++
      if (h.correct) day.ok++
    }
  }
  return days
})
const maxDay = computed(() => Math.max(1, ...daily.value.map((d) => d.n)))

const srsStages = computed(() => {
  const buckets = [0, 0, 0, 0, 0, 0, 0] // stage0..5 + 毕业
  for (const c of Object.values(archive.data.srs) as any[]) {
    buckets[Math.min(c.stage, 5)]++
  }
  return buckets
})
const stageNames = ['第1轮(1天)', '第2轮(2天)', '第3轮(4天)', '第4轮(7天)', '第5轮(15天)', '第6轮(30天)', '已毕业']
</script>

<template>
  <div>
    <h1>统计</h1>

    <h2>章节正确率（从高到低）</h2>
    <div class="card">
      <div v-for="c in chapters" :key="c.id" class="row">
        <span class="name">{{ c.title }}</span>
        <div class="barwrap">
          <div class="bar" :class="{ low: c.acc !== null && c.acc < 0.7 }" :style="{ width: (c.acc ?? 0) * 100 + '%' }" />
        </div>
        <span class="val small" :class="c.acc === null ? 'muted' : c.acc !== null && c.acc < 0.7 ? 'badtext' : ''">
          {{ c.acc === null ? '未做' : Math.round(c.acc * 100) + '%' }} ({{ c.done }}/{{ c.total }})
        </span>
      </div>
    </div>

    <h2>近 30 天刷题量</h2>
    <div class="card chart">
      <div v-for="d in daily" :key="d.date" class="col" :title="`${d.date}: ${d.n} 题`">
        <div class="stack">
          <div class="okpart" :style="{ height: maxDay ? (d.ok / maxDay) * 120 + 'px' : 0 }" />
          <div class="badpart" :style="{ height: maxDay ? ((d.n - d.ok) / maxDay) * 120 + 'px' : 0 }" />
        </div>
        <span v-if="d.n" class="bub">{{ d.n }}</span>
      </div>
    </div>
    <p class="small muted">绿=答对，红=答错；悬停柱子看日期与题数。</p>

    <h2>间隔复习分布</h2>
    <div class="card srs">
      <div v-for="(n, i) in srsStages" :key="i" class="srsrow">
        <span class="sname small">{{ stageNames[i] }}</span>
        <span class="sval" :class="{ big: i === 6 }">{{ n }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card { margin-bottom: 6px; }
.row { display: flex; align-items: center; gap: 12px; padding: 6px 0; }
.name { width: 150px; flex: none; }
.barwrap { flex: 1; height: 12px; background: var(--bg); border-radius: 999px; overflow: hidden; }
.bar { height: 100%; background: var(--accent); border-radius: 999px; min-width: 2px; }
.bar.low { background: var(--accent-2); }
.val { width: 110px; text-align: right; flex: none; }
.badtext { color: var(--accent-2); }
.chart { display: flex; align-items: flex-end; gap: 4px; height: 150px; padding: 14px 16px; }
.col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; height: 100%; justify-content: flex-end; position: relative; }
.stack { display: flex; flex-direction: column; justify-content: flex-end; width: 100%; max-width: 18px; }
.okpart { background: var(--accent); border-radius: 2px 2px 0 0; width: 100%; }
.badpart { background: var(--danger); opacity: 0.75; width: 100%; border-radius: 2px 2px 0 0; }
.bub { font-size: 9px; color: var(--ink-3); position: absolute; top: -2px; }
.srsrow { display: flex; justify-content: space-between; padding: 5px 0; }
.sname { color: var(--ink-2); }
.sval { font-weight: 700; }
.sval.big { color: var(--accent); }
</style>
