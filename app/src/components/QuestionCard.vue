<script setup lang="ts">
// 题目卡：题干 + 选项 + 判分 + 解析 + 收藏
import { ref, computed } from 'vue'
import type { ChoiceQuestion, OptKey } from '../core/types'
import { useArchive } from '../stores/archive'
import MdView from './MdView.vue'

const props = withDefaults(
  defineProps<{
    q: ChoiceQuestion
    index?: number
    total?: number
    /** exam = 考试模式：选择不立即判分，由父组件交卷 */
    mode?: 'practice' | 'exam' | 'review'
    locked?: boolean
  }>(),
  { index: undefined, total: undefined, mode: 'practice', locked: false },
)

const emit = defineEmits<{ answered: [choice: OptKey] }>()
const archive = useArchive()

const picked = ref<OptKey | ''>('')
const revealed = ref(false)

const attempt = computed(() => archive.attempts[props.q.id])
const bookmarked = computed(() => archive.bookmarks.has(props.q.id))

// review 模式直接显示上次的作答与判定
if (props.mode === 'review' && attempt.value) {
  picked.value = attempt.value.choice
  revealed.value = true
}

const showState = (key: OptKey) => {
  if (!revealed.value) return picked.value === key ? 'picked' : ''
  if (key === props.q.answer) return 'right'
  if (key === picked.value) return 'wrong'
  return ''
}

function pick(key: OptKey) {
  if (revealed.value || props.locked) return
  picked.value = key
  if (props.mode === 'practice') {
    revealed.value = true
    archive.record(props.q.id, key, key === props.q.answer)
    emit('answered', key)
  } else {
    emit('answered', key)
  }
}

async function toggleMark() {
  await archive.toggleBookmark(props.q.id)
}

const sourceLabel = computed(() =>
  props.q.kind === 'real' ? `${props.q.term} 真题 · 第${props.q.no}题` : '分章练习',
)
</script>

<template>
  <div class="qcard card">
    <div class="qhead">
      <span class="pill green" v-if="index !== undefined">第 {{ index }} / {{ total }} 题</span>
      <span class="pill">{{ sourceLabel }}</span>
      <span class="pill amber" v-if="q.knowledge">{{ q.knowledge }}</span>
      <span v-if="q.figureMissing" class="pill" title="原卷含图，本站未收录图示">⚠ 原卷含图</span>
      <button class="mark" :class="{ on: bookmarked }" @click="toggleMark" title="收藏本题">
        {{ bookmarked ? '★ 已收藏' : '☆ 收藏' }}
      </button>
    </div>

    <div class="stem"><MdView :source="q.stem" /></div>

    <div v-if="q.figure?.length" class="figures">
      <img
        v-for="f in q.figure"
        :key="f"
        :src="`./figures/${f}`"
        :alt="`题目配图 ${f}`"
        loading="lazy"
      />
    </div>
    <div v-else-if="q.figureMissing" class="pill" title="原卷含图但源 PDF 未印出，请按解析推理">⚠ 原卷含图（源 PDF 未印出）</div>

    <div class="opts">
      <button
        v-for="(text, key) in q.options"
        :key="key"
        class="opt"
        :class="showState(key as OptKey)"
        :disabled="revealed || locked"
        @click="pick(key as OptKey)"
      >
        <b class="optkey">{{ key }}</b>
        <span class="opttext">{{ text }}</span>
      </button>
    </div>

    <div v-if="revealed" class="judge" :class="picked === q.answer ? 'ok' : 'bad'">
      <template v-if="picked === q.answer">✔ 回答正确</template>
      <template v-else>✘ 回答错误，正确答案：{{ q.answer }}</template>
    </div>

    <div v-if="revealed && q.analysis" class="analysis">
      <div class="atitle">解析</div>
      <MdView :source="q.analysis" />
    </div>
  </div>
</template>

<style scoped>
.qcard { margin-bottom: 18px; }
.qhead { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.qhead .mark {
  margin-left: auto;
  border: none;
  background: transparent;
  color: var(--ink-3);
  padding: 2px 6px;
}
.qhead .mark.on { color: var(--accent-2); }
.stem { font-size: 15.5px; }
.figures { margin-top: 10px; display: grid; gap: 10px; }
.figures img {
  max-width: 100%;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: #fff;
  padding: 8px;
}
.opts { display: grid; gap: 8px; margin-top: 12px; }
.opt {
  display: flex;
  gap: 10px;
  text-align: left;
  padding: 10px 14px;
  align-items: baseline;
  min-height: 44px;
}
.opt:disabled { cursor: default; }
.opt.picked { border-color: var(--accent); background: var(--accent-weak); }
.opt.right { border-color: var(--ok); background: var(--ok-weak); }
.opt.wrong { border-color: var(--danger); background: var(--danger-weak); }
.optkey { flex: none; font-family: var(--font-mono); }
.judge { margin-top: 12px; font-weight: 600; }
.judge.ok { color: var(--ok); }
.judge.bad { color: var(--danger); }
.analysis {
  margin-top: 10px;
  border-top: 1px dashed var(--line);
  padding-top: 10px;
}
.atitle { font-weight: 700; color: var(--accent); margin-bottom: 4px; }
</style>
