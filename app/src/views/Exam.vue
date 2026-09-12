<script setup lang="ts">
// 模拟考试：全库抽 75 题限时 150 分钟，倒计时，交卷报告
import { computed, onUnmounted, ref } from 'vue'
import { PLAYABLE, shuffle } from '../data/bank'
import { useArchive } from '../stores/archive'
import QuestionCard from '../components/QuestionCard.vue'

const archive = useArchive()

const PRESET_TERMS = ['2026年上半年 · 模拟卷A', '2026年上半年 · 模拟卷B']
const preset = ref('')
const started = ref(false)
const submitted = ref(false)
const picks = ref<Record<string, string>>({})
const remain = ref(0)
let timer: number | undefined

const qs = ref<any[]>([])
const answeredCount = computed(() => qs.value.filter((q) => picks.value[q.id]).length)
const score = computed(() => qs.value.filter((q) => picks.value[q.id] === q.answer).length)

function start(name: string) {
  preset.value = name
  qs.value = shuffle(PLAYABLE).slice(0, 75)
  picks.value = {}
  submitted.value = false
  started.value = true
  remain.value = archive.data.settings.examMinutes * 60
  timer = window.setInterval(() => {
    remain.value--
    if (remain.value <= 0) submit()
  }, 1000)
}

function pick(qid: string, choice: string) {
  if (!submitted.value) picks.value[qid] = choice
}

function scrollToQ(i: number) {
  document.getElementById('e-' + i)?.scrollIntoView({ behavior: 'smooth' })
}

function submit() {
  if (timer) clearInterval(timer)
  submitted.value = true
  for (const q of qs.value) {
    const c = picks.value[q.id] as any
    if (c) archive.record(q.id, c, c === q.answer)
  }
  window.scrollTo({ top: 0 })
}

onUnmounted(() => timer && clearInterval(timer))

const mmss = computed(() => {
  const m = Math.floor(remain.value / 60)
  const s = remain.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})
</script>

<template>
  <div>
    <template v-if="!started">
      <h1>模拟考试</h1>
      <p class="muted">从全部题库随机抽取 75 题，限时 150 分钟，模拟机考节奏。</p>
      <div class="paperlist">
        <div v-for="t in PRESET_TERMS" :key="t" class="card hoverable paper">
          <div>
            <h3 style="margin: 0 0 4px">{{ t }}</h3>
            <span class="small muted">75 题 · 150 分钟 · 自动抽题</span>
          </div>
          <button class="primary" @click="start(t)">开考</button>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="head">
        <h1 style="margin: 0">{{ preset }}</h1>
        <span class="timer" :class="{ urgent: remain < 300 }">{{ mmss }}</span>
        <span class="pill">{{ answeredCount }}/75 已答</span>
      </div>

      <div v-if="submitted" class="card report">
        <span class="rscore">{{ score }}</span>
        <span class="rscore-sub">/ 75 分（45 分及格）</span>
        <div class="small muted" style="margin-top: 4px">
          {{ score >= 45 ? '过线！保持手感。' : '未过线，回错题本复盘薄弱知识点。' }}
          已计入错题本与间隔复习。
        </div>
      </div>

      <div class="sheet card" v-if="!submitted">
        <button
          v-for="(q, i) in qs"
          :key="q.id"
          class="dot"
          :class="{ filled: picks[q.id] }"
          @click="scrollToQ(i)"
        >{{ i + 1 }}</button>
      </div>

      <template v-for="(q, i) in qs" :key="q.id">
        <div :id="'e-' + i">
          <QuestionCard
            :q="q"
            :index="i + 1"
            :total="75"
            mode="exam"
            :locked="submitted"
            @answered="(c) => pick(q.id, c)"
          />
        </div>
      </template>

      <div class="stickybar" v-if="!submitted">
        <button class="primary big" @click="submit">交卷（{{ answeredCount }}/75）</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.paperlist { display: grid; gap: 12px; margin-top: 16px; }
.paper { display: flex; justify-content: space-between; align-items: center; }
.head { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; flex-wrap: wrap; }
.timer {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
  color: var(--accent);
  background: var(--accent-weak);
  padding: 4px 14px;
  border-radius: 8px;
}
.timer.urgent { color: var(--danger); background: var(--danger-weak); }
.report { display: flex; align-items: baseline; gap: 8px; margin-bottom: 14px; border-left: 4px solid var(--accent); }
.rscore { font-size: 42px; font-weight: 700; font-family: var(--font-serif); color: var(--accent); }
.rscore-sub { color: var(--ink-2); }
.sheet { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 14px; padding: 12px 16px; }
.dot {
  min-width: 32px; height: 32px; font-size: 12px;
  border: 1px solid var(--line); border-radius: 6px; background: var(--surface); color: var(--ink-3);
}
.dot.filled { color: var(--accent); background: var(--accent-weak); border-color: transparent; }
.stickybar { position: sticky; bottom: 14px; display: flex; justify-content: center; margin-top: 20px; }
.big { font-size: 16px; padding: 12px 34px; box-shadow: var(--shadow); }
</style>
