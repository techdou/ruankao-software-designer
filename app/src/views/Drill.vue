<script setup lang="ts">
// 刷题练习：按章节/状态筛选，顺序或随机，即时判分
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { PLAYABLE, shuffle } from '../data/bank'
import { CHAPTERS, chapterMap } from '../data/chapters'
import { useArchive } from '../stores/archive'
import QuestionCard from '../components/QuestionCard.vue'

const route = useRoute()
const archive = useArchive()

const chapter = ref(String(route.query.chapter || 'all'))
const status = ref<'all' | 'wrong' | 'todo'>('all')
const random = ref(false)
const session = ref<string[]>([])
const cur = ref(0)
const started = ref(false)

watch(
  () => route.query.chapter,
  (v) => {
    if (v) {
      chapter.value = String(v)
      start()
    }
  },
)

const pool = computed(() => {
  let list = PLAYABLE.filter((q) => (chapter.value === 'all' ? true : q.chapter === chapter.value))
  if (status.value === 'wrong') list = list.filter((q) => archive.attempts[q.id]?.correct === false)
  if (status.value === 'todo') list = list.filter((q) => !archive.attempts[q.id])
  return list
})

function start() {
  const list = pool.value
  session.value = random.value ? shuffle(list.map((q) => q.id)) : list.map((q) => q.id)
  cur.value = 0
  started.value = session.value.length > 0
}

const questions = computed(() => session.value.map((id) => PLAYABLE.find((q) => q.id === id)!))
const q = computed(() => questions.value[cur.value])

const sessionStat = computed(() => {
  const answered = questions.value.filter((x) => archive.attempts[x.id]).length
  const ok = questions.value.filter((x) => archive.attempts[x.id]?.correct).length
  return { answered, ok }
})

function jump(i: number) {
  cur.value = i
}
function nextQ() {
  if (cur.value < questions.value.length - 1) cur.value++
}
function prevQ() {
  if (cur.value > 0) cur.value--
}
</script>

<template>
  <div>
    <h1>刷题练习</h1>

    <div class="card filter">
      <label>章节
        <select v-model="chapter">
          <option value="all">全部章节</option>
          <option v-for="c in CHAPTERS" :key="c.id" :value="c.id">{{ c.title }}</option>
        </select>
      </label>
      <label>范围
        <select v-model="status">
          <option value="all">全部</option>
          <option value="todo">未做过</option>
          <option value="wrong">只刷错题</option>
        </select>
      </label>
      <label class="chk"><input type="checkbox" v-model="random" /> 随机顺序</label>
      <button class="primary" @click="start">开始练习（{{ pool.length }} 题）</button>
      <span class="muted small" v-if="!started && !pool.length">当前筛选没有题。</span>
    </div>

    <template v-if="started">
      <div class="sessionbar card">
        <div class="progress-line">
          <span>本组：{{ sessionStat.answered }}/{{ questions.length }} 已做 · 对 {{ sessionStat.ok }}</span>
          <span class="muted small">{{ chapterMap.get(chapter)?.title }}</span>
        </div>
        <div class="sheet">
          <button
            v-for="(qq, i) in questions"
            :key="qq.id"
            class="dot"
            :class="{
              cur: i === cur,
              ok: archive.attempts[qq.id]?.correct,
              bad: archive.attempts[qq.id] && !archive.attempts[qq.id].correct,
            }"
            @click="jump(i)"
          >{{ i + 1 }}</button>
        </div>
      </div>

      <QuestionCard v-if="q" :key="q.id" :q="q" :index="cur + 1" :total="questions.length" />

      <div class="pager">
        <button @click="prevQ" :disabled="cur === 0">← 上一题</button>
        <button class="primary" @click="nextQ" :disabled="cur === questions.length - 1">下一题 →</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.filter { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin-bottom: 16px; }
.filter label { display: flex; align-items: center; gap: 6px; font-size: 14px; color: var(--ink-2); }
.filter select { font: inherit; padding: 6px 10px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); }
.chk input { accent-color: var(--accent); }
.filter button { margin-left: auto; }
.sessionbar { margin-bottom: 14px; padding: 14px 18px; }
.progress-line { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }
.sheet { display: flex; flex-wrap: wrap; gap: 5px; }
.dot {
  min-width: 30px; height: 30px; padding: 0 4px;
  font-size: 12px; text-align: center;
  border: 1px solid var(--line); background: var(--surface); border-radius: 6px;
  color: var(--ink-3);
}
.dot.ok { background: var(--ok-weak); border-color: transparent; color: var(--ok); }
.dot.bad { background: var(--danger-weak); border-color: transparent; color: var(--danger); }
.dot.cur { outline: 2px solid var(--accent); color: var(--ink); font-weight: 700; }
.pager { display: flex; justify-content: space-between; margin-top: 4px; }
</style>
