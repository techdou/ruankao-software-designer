<script setup lang="ts">
// 真题套卷：选卷 → 逐题作答（答题卡）→ 交卷判分出报告
import { computed, ref } from 'vue'
import { paperQuestions, TERMS } from '../data/bank'
import { useArchive } from '../stores/archive'
import QuestionCard from '../components/QuestionCard.vue'

const archive = useArchive()
const term = ref('')
const submitted = ref(false)
const picks = ref<Record<string, string>>({})

const qs = computed(() => (term.value ? paperQuestions(term.value) : []))
const answeredCount = computed(() => qs.value.filter((q) => picks.value[q.id]).length)
const score = computed(() => {
  if (!submitted.value) return 0
  return qs.value.filter((q) => picks.value[q.id] === q.answer).length
})

function start(t: string) {
  term.value = t
  submitted.value = false
  picks.value = {}
  window.scrollTo({ top: 0 })
}

function pick(qid: string, choice: string) {
  picks.value[qid] = choice
}

function scrollToQ(i: number) {
  document.getElementById('q-' + i)?.scrollIntoView({ behavior: 'smooth' })
}

function submit() {
  submitted.value = true
  for (const q of qs.value) {
    const c = picks.value[q.id] as any
    if (c) archive.record(q.id, c, c === q.answer)
  }
  window.scrollTo({ top: 0 })
}
</script>

<template>
  <div>
    <template v-if="!term">
      <h1>真题套卷</h1>
      <p class="muted">整卷作答，交卷后统一判分。建议先整卷摸底，再按章精刷。</p>
      <div class="paperlist">
        <div v-for="t in TERMS" :key="t" class="card hoverable paper">
          <div>
            <h3 style="margin: 0 0 4px">{{ t }} · 综合知识</h3>
            <span class="small muted">{{ paperQuestions(t).length }} 题已收录（原卷 75 题）</span>
          </div>
          <button class="primary" @click="start(t)">开始作答</button>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="head">
        <button @click="term = ''">← 返回选卷</button>
        <h1 style="margin: 0">{{ term }} 综合知识</h1>
        <span class="pill">{{ answeredCount }}/{{ qs.length }} 已答</span>
      </div>

      <div v-if="submitted" class="card report">
        <span class="rscore">{{ score }}</span>
        <span class="rscore-sub">/ {{ qs.length }} 分（每题 1 分）</span>
        <div class="small muted" style="margin-top: 4px">
          45 分及格 · 已计入错题本与间隔复习
        </div>
      </div>

      <div class="sheet card">
        <button
          v-for="(q, i) in qs"
          :key="q.id"
          class="dot"
          :class="{ ok: submitted && picks[q.id] === q.answer, bad: submitted && picks[q.id] && picks[q.id] !== q.answer, filled: !submitted && picks[q.id] }"
          @click="scrollToQ(i)"
        >{{ q.no }}</button>
      </div>

      <template v-for="(q, i) in qs" :key="q.id">
        <div :id="'q-' + i">
          <QuestionCard
            :q="q"
            :index="i + 1"
            :total="qs.length"
            mode="exam"
            :locked="submitted"
            @answered="(c) => pick(q.id, c)"
          />
        </div>
      </template>

      <div class="stickybar" v-if="!submitted">
        <button class="primary big" :disabled="answeredCount === 0" @click="submit">
          交卷判分（{{ answeredCount }}/{{ qs.length }}）
        </button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.paperlist { display: grid; gap: 12px; margin-top: 16px; }
.paper { display: flex; justify-content: space-between; align-items: center; }
.head { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; flex-wrap: wrap; }
.report { display: flex; align-items: baseline; gap: 8px; margin-bottom: 14px; border-left: 4px solid var(--accent); }
.rscore { font-size: 42px; font-weight: 700; font-family: var(--font-serif); color: var(--accent); }
.rscore-sub { color: var(--ink-2); }
.sheet { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 14px; padding: 12px 16px; }
.dot {
  min-width: 32px; height: 32px; padding: 0 4px; font-size: 12px;
  border: 1px solid var(--line); border-radius: 6px; background: var(--surface); color: var(--ink-3);
}
.dot.filled { color: var(--accent); border-color: var(--accent-weak); background: var(--accent-weak); }
.dot.ok { background: var(--ok-weak); border-color: transparent; color: var(--ok); }
.dot.bad { background: var(--danger-weak); border-color: transparent; color: var(--danger); }
.stickybar {
  position: sticky; bottom: 14px; display: flex; justify-content: center;
  margin-top: 20px;
}
.big { font-size: 16px; padding: 12px 34px; box-shadow: var(--shadow); }
</style>
