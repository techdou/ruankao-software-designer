<script setup lang="ts">
// 错题本：SRS 到期复习优先，或按章重刷错题（review 模式看上次作答）
import { computed, ref } from 'vue'
import { PLAYABLE, shuffle } from '../data/bank'
import { CHAPTERS } from '../data/chapters'
import { useArchive } from '../stores/archive'
import { isDue } from '../core/srs'
import QuestionCard from '../components/QuestionCard.vue'

const archive = useArchive()
const mode = ref<'due' | 'all'>('due')
const chapter = ref('all')
const session = ref<string[]>([])
const cur = ref(0)

const wrongs = computed(() => PLAYABLE.filter((q) => archive.attempts[q.id]?.correct === false))

const dueList = computed(() =>
  shuffle(wrongs.value.filter((q) => isDue(archive.data.srs[q.id] as any))),
)

function start() {
  let list = mode.value === 'due' ? dueList.value : wrongs.value
  if (chapter.value !== 'all') list = list.filter((q) => q.chapter === chapter.value)
  session.value = list.map((q) => q.id)
  cur.value = 0
}

const qs = computed(() => session.value.map((id) => PLAYABLE.find((q) => q.id === id)!))
const q = computed(() => qs.value[cur.value])

const stageLabel = (id: string) => {
  const c = archive.data.srs[id] as any
  if (!c) return ''
  return c.stage >= 5 ? '已掌握' : `复习第 ${c.stage + 1} 轮`
}
</script>

<template>
  <div>
    <h1>错题本</h1>
    <p class="muted">
      答错自动收录。答对一次进入间隔复习（1/2/4/7/15/30 天），连续答对 6 轮即毕业移出。
    </p>

    <div class="card filter">
      <label>模式
        <select v-model="mode">
          <option value="due">只看到期待复习（{{ dueList.length }}）</option>
          <option value="all">全部错题（{{ wrongs.length }}）</option>
        </select>
      </label>
      <label>章节
        <select v-model="chapter">
          <option value="all">全部章节</option>
          <option v-for="c in CHAPTERS" :key="c.id" :value="c.id">{{ c.title }}</option>
        </select>
      </label>
      <button class="primary" @click="start">开始复习</button>
      <span v-if="!wrongs.length" class="small muted">还没有错题，保持！</span>
    </div>

    <template v-if="session.length && q">
      <div class="meta card">
        第 {{ cur + 1 }} / {{ qs.length }} 题 ·
        <span class="pill amber">{{ stageLabel(q.id) }}</span>
        <span v-if="q.knowledge" class="pill">{{ q.knowledge }}</span>
      </div>
      <QuestionCard :key="q.id + 'w'" :q="q" :mode="'practice'" />
      <div class="pager">
        <button :disabled="cur === 0" @click="cur--">← 上一题</button>
        <button class="primary" :disabled="cur === qs.length - 1" @click="cur++">下一题 →</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.filter { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin-bottom: 16px; }
.filter label { display: flex; align-items: center; gap: 6px; font-size: 14px; color: var(--ink-2); }
select { font: inherit; padding: 6px 10px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); }
.filter button { margin-left: auto; }
.meta { padding: 10px 16px; margin-bottom: 12px; display: flex; gap: 8px; align-items: center; }
.pager { display: flex; justify-content: space-between; margin-top: 4px; }
</style>
