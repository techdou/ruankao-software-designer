<script setup lang="ts">
// 仪表盘：总进度 + 连续打卡 + 待复习 + 薄弱章节 + 快捷入口
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useArchive } from '../stores/archive'
import { CHAPTERS } from '../data/chapters'
import { PLAYABLE, ALL_QUESTIONS } from '../data/bank'
import { isDue } from '../core/srs'
import ProgressRing from '../components/ProgressRing.vue'
import Achievements from '../components/Achievements.vue'

const archive = useArchive()

const totalPlayable = computed(() => PLAYABLE.length)
const done = computed(() => archive.doneCount)
const acc = computed(() => (done.value ? archive.correctCount / done.value : 0))
const dueCount = computed(
  () => Object.values(archive.data.srs).filter((c) => isDue(c as any)).length,
)

const chapterStats = computed(() =>
  CHAPTERS.map((ch) => {
    const qs = PLAYABLE.filter((q) => q.chapter === ch.id)
    const doneQs = qs.filter((q) => archive.attempts[q.id])
    const ok = doneQs.filter((q) => archive.attempts[q.id].correct)
    return {
      ...ch,
      total: qs.length,
      done: doneQs.length,
      acc: doneQs.length ? ok.length / doneQs.length : null,
    }
  }),
)

// 薄弱章节：做过 ≥5 题且正确率 < 70%
const weak = computed(() =>
  chapterStats.value
    .filter((c) => c.done >= 5 && c.acc !== null && c.acc < 0.7)
    .sort((a, b) => (a.acc ?? 1) - (b.acc ?? 1))
    .slice(0, 3),
)

const notesDone = computed(
  () => Object.values(archive.data.noteProgress).filter((n) => n.done).length,
)
</script>

<template>
  <div>
    <h1>仪表盘</h1>
    <p class="muted">软件设计师 · 每天进步一点，考场就稳一点。</p>

    <div class="hero">
      <img src="/hero.png" alt="学习插画：书本翻页化作软件流程图" />
    </div>

    <div class="grid">
      <div class="card row">
        <ProgressRing :value="totalPlayable ? done / totalPlayable : 0" label="刷题进度" />
        <div class="facts">
          <div><b>{{ done }}</b> / {{ totalPlayable }} 题已刷</div>
          <div>正确率 <b>{{ Math.round(acc * 100) }}%</b></div>
          <div>连续学习 <b>{{ archive.data.streak.days }}</b> 天</div>
        </div>
      </div>

      <div class="card">
        <div class="kbig" :class="{ amber: dueCount > 0 }">{{ dueCount }}</div>
        <div class="muted">到期待复习（间隔复习队列）</div>
        <RouterLink to="/wrong" class="primary linkbtn" v-if="dueCount > 0">去复习 →</RouterLink>
      </div>

      <div class="card">
        <div class="kbig">{{ notesDone }}<span class="muted"> / {{ CHAPTERS.length }}</span></div>
        <div class="muted">讲义已读完章节数</div>
        <RouterLink to="/notes" class="linkbtn">继续阅读 →</RouterLink>
      </div>
    </div>

    <div v-if="weak.length" class="card warn">
      <b>薄弱章节提醒</b>
      <p class="small muted">以下章节做题 ≥5 且正确率不足 70%，建议先重读讲义再刷题：</p>
      <RouterLink v-for="w in weak" :key="w.id" :to="`/drill?chapter=${w.id}`" class="weak-item">
        {{ w.title }}（正确率 {{ Math.round((w.acc ?? 0) * 100) }}%）
      </RouterLink>
    </div>

    <Achievements />

    <h2>章节进度</h2>
    <div class="chlist card">
      <div v-for="c in chapterStats" :key="c.id" class="chrow">
        <span class="chtitle">{{ c.title }}</span>
        <div class="bar">
          <div class="bar-fill" :style="{ width: (c.total ? c.done / c.total : 0) * 100 + '%' }" />
        </div>
        <span class="small muted num">{{ c.done }}/{{ c.total }}</span>
        <span class="small num" :class="c.acc === null ? 'muted' : c.acc >= 0.7 ? 'oktext' : 'badtext'">
          {{ c.acc === null ? '—' : Math.round(c.acc * 100) + '%' }}
        </span>
      </div>
    </div>

    <p class="small muted" style="margin-top: 14px">
      题库总量 {{ ALL_QUESTIONS.length }} 题（可作答 {{ totalPlayable }} 题）。
    </p>
  </div>
</template>

<style scoped>
.grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 14px; margin-top: 16px; }
@media (max-width: 860px) { .grid { grid-template-columns: 1fr; } }
.row { display: flex; gap: 18px; align-items: center; }
.facts { display: grid; gap: 6px; }
.kbig { font-size: 34px; font-weight: 700; font-family: var(--font-serif); }
.kbig.amber { color: var(--accent-2); }
.linkbtn { display: inline-block; margin-top: 8px; font-weight: 600; }
.warn { margin-top: 14px; border-left: 3px solid var(--accent-2); }
.hero { margin: 12px 0 4px; border: 1px solid var(--line); border-radius: var(--radius-lg); overflow: hidden; background: var(--surface); }
.hero img { display: block; width: 100%; height: auto; }
.weak-item { display: inline-block; margin: 4px 14px 0 0; }
.chlist { margin-top: 8px; }
.chrow { display: flex; align-items: center; gap: 12px; padding: 7px 0; }
.chrow + .chrow { border-top: 1px dashed var(--line); }
.chtitle { width: 150px; flex: none; }
.bar { flex: 1; height: 8px; background: var(--bg); border-radius: 999px; overflow: hidden; }
.bar-fill { height: 100%; background: var(--accent); border-radius: 999px; }
.num { width: 74px; text-align: right; flex: none; }
.oktext { color: var(--ok); }
.badtext { color: var(--danger); }
</style>
