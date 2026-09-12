<script setup lang="ts">
// 案例题（下午题）：背景 + 逐小问先想后看 + 自评
import { computed, ref } from 'vue'
import rawCases from '../data/bank/cases.json'
import MdView from '../components/MdView.vue'
import { useArchive } from '../stores/archive'

const cases = rawCases as any[]
const archive = useArchive()

const cur = ref<string>('')
const revealed = ref<Record<string, boolean>>({})
const selfOk = ref<Record<string, boolean>>({})

const c = computed(() => cases.find((x) => x.id === cur.value))

const typeLabel: Record<string, string> = {
  dfd: '数据流图',
  db: '数据库设计',
  uml: 'UML 建模',
  algo: '算法设计',
  pattern: '设计模式',
}

function open(id: string) {
  cur.value = id
  revealed.value = {}
  selfOk.value = {}
  window.scrollTo({ top: 0 })
}

function reveal(key: string) {
  revealed.value[key] = true
}

async function self(no: number, ok: boolean) {
  const key = `${c.value!.id}-q${no}`
  selfOk.value[no] = ok
  // 案例题自评：choice 记空，正确性记入历史与 SRS（错题本里以案例题形式出现）
  await archive.record(key, '', ok)
}

const progress = computed(() => {
  const done = Object.keys(selfOk.value).length
  const ok = Object.values(selfOk.value).filter(Boolean).length
  return { done, ok, total: c.value?.subQuestions.length ?? 0 }
})
</script>

<template>
  <div>
    <template v-if="!c">
      <h1>案例题专项</h1>
      <p class="muted">
        下午卷五大固定题型，每套 4 小问。先自己作答（写下来），再对照答案与解析自评。
      </p>
      <div class="hero"><img :src="'/art/hero-cases.png'" alt="案例题插画" /></div>
      <div class="paperlist">
        <div v-for="x in cases" :key="x.id" class="card hoverable paper">
          <div>
            <h3 style="margin: 0 0 4px">{{ x.title }}</h3>
            <span class="pill green">{{ typeLabel[x.caseType] }}</span>
            <span class="pill">{{ x.subQuestions.length }} 小问</span>
          </div>
          <button class="primary" @click="open(x.id)">进入作答</button>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="head">
        <button @click="cur = ''">← 返回列表</button>
        <h1 style="margin: 0; font-size: 20px">{{ c.title }}</h1>
      </div>

      <div class="card bg">
        <div class="atitle">题干背景</div>
        <MdView :source="c.background" />
      </div>

      <div v-for="(sq, i) in c.subQuestions" :key="sq.no" class="card q">
        <div class="qno">第 {{ Number(i) + 1 }} 问（{{ sq.no }} 小题）</div>
        <div class="qstem">{{ sq.stem }}</div>

        <template v-if="!revealed[sq.no]">
          <div class="think muted small">⌛ 请先在纸上/编辑器写下你的答案，再对照解析自评。</div>
          <button class="primary" @click="reveal(sq.no)">查看答案与解析</button>
        </template>

        <template v-else>
          <div class="answer"><b>参考答案：</b>{{ sq.answer }}</div>
          <div class="ana"><b>解析：</b>{{ sq.analysis }}</div>
          <div class="selfbar" v-if="selfOk[sq.no] === undefined">
            <span class="small muted">对照后自评：</span>
            <button class="okbtn" @click="self(sq.no, true)">✔ 我答对了</button>
            <button class="badbtn" @click="self(sq.no, false)">✘ 没答对</button>
          </div>
          <div v-else class="selfdone" :class="selfOk[sq.no] ? 'oktext' : 'badtext'">
            {{ selfOk[sq.no] ? '已记录：答对' : '已记录：未答对（建议重做本题）' }}
          </div>
        </template>
      </div>

      <div class="card" v-if="progress.done > 0">
        本套进度：{{ progress.done }}/{{ progress.total }} 问已自评 · 答对 {{ progress.ok }} 问
      </div>
    </template>
  </div>
</template>

<style scoped>
.paperlist { display: grid; gap: 12px; margin-top: 16px; }
.hero { margin: 12px 0; border: 1px solid var(--line); border-radius: var(--radius-lg); overflow: hidden; }
.hero img { display: block; width: 100%; height: auto; }
.paper { display: flex; justify-content: space-between; align-items: center; }
.head { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.bg { border-left: 4px solid var(--accent); margin-bottom: 14px; }
.atitle { font-weight: 700; color: var(--accent); margin-bottom: 6px; }
.q { margin-bottom: 12px; }
.qno { font-weight: 700; margin-bottom: 6px; color: var(--ink-2); font-size: 13px; }
.qstem { white-space: pre-wrap; font-size: 15px; }
.think { margin: 8px 0; }
.answer { background: var(--accent-weak); border-radius: var(--radius); padding: 8px 12px; margin-top: 10px; }
.ana { margin-top: 8px; color: var(--ink-2); font-size: 14px; }
.selfbar { display: flex; gap: 10px; align-items: center; margin-top: 10px; }
.okbtn { color: var(--ok); border-color: var(--ok); }
.badbtn { color: var(--danger); border-color: var(--danger); }
.selfdone { margin-top: 10px; font-weight: 600; }
.oktext { color: var(--ok); }
.badtext { color: var(--danger); }
.md :deep(pre) { white-space: pre-wrap; }
</style>
