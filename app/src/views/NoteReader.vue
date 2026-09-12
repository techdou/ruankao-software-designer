<script setup lang="ts">
// 讲义阅读器：Markdown 渲染 + 目录 + 进度标记
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CHAPTERS, chapterMap } from '../data/chapters'
import { useArchive } from '../stores/archive'
import MdView from '../components/MdView.vue'

const files = import.meta.glob('../content/*.md', { query: '?raw', import: 'default', eager: true }) as Record<string, string>

const route = useRoute()
const router = useRouter()
const archive = useArchive()

const id = computed(() => String(route.params.id || 'ch01'))
const ch = computed(() => chapterMap.get(id.value))

// 拆 frontmatter 与正文
const parsed = computed(() => {
  const raw = files[`../content/${id.value}.md`] ?? ''
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/)
  const meta: Record<string, any> = {}
  if (m) {
    for (const line of m[1].split('\n')) {
      const kv = line.match(/^(\w+):\s*(.*)$/)
      if (kv) meta[kv[1]] = kv[2].trim()
    }
  }
  return { body: m ? m[2] : raw, meta }
})

// 从标题生成目录
const toc = computed(() => {
  const out: { level: number; text: string; anchor: string }[] = []
  for (const line of parsed.value.body.split('\n')) {
    const m = line.match(/^(#{2,3})\s+(.*)$/)
    if (m) {
      const text = m[2].replace(/[#*`]/g, '').trim()
      out.push({ level: m[1].length, text, anchor: text })
    }
  }
  return out
})

const idx = CHAPTERS.findIndex((c) => c.id === id.value)
const prev = idx > 0 ? CHAPTERS[idx - 1] : null
const next = idx >= 0 && idx < CHAPTERS.length - 1 ? CHAPTERS[idx + 1] : null

const readerEl = ref<HTMLElement | null>(null)
let saveTimer: number | undefined

async function onScroll() {
  const el = readerEl.value
  if (!el) return
  const ratio = Math.min(1, el.scrollTop / Math.max(1, el.scrollHeight - el.clientHeight))
  clearTimeout(saveTimer)
  saveTimer = window.setTimeout(() => archive.setNoteProgress(id.value, ratio), 600)
}

watch(id, () => {
  readerEl.value?.scrollTo({ top: 0 })
})

async function markDone() {
  await archive.markNoteDone(id.value, !archive.data.noteProgress[id.value]?.done)
}

function tocGo(anchor: string) {
  const headings = readerEl.value?.querySelectorAll('h2, h3')
  headings?.forEach((h) => {
    if (h.textContent?.trim() === anchor) h.scrollIntoView({ behavior: 'smooth' })
  })
}

function goDrill() {
  router.push(`/drill?chapter=${id.value}`)
}
</script>

<template>
  <div v-if="ch" class="reader">
    <aside class="toc card">
      <div class="small muted toc-head">本篇目录</div>
      <a
        v-for="t in toc"
        :key="t.anchor + t.level"
        :href="`#/notes/${id}`"
        class="toc-item"
        :class="{ l3: t.level === 3 }"
        @click.prevent="tocGo(t.anchor)"
      >{{ t.text }}</a>
    </aside>

    <article class="content" @scroll.passive="onScroll" ref="readerEl">
      <div class="thead">
        <h1>{{ parsed.meta.title || ch.title }}</h1>
        <div class="muted small">{{ ch.subtitle }} · 预计 {{ parsed.meta.minutes || 45 }} 分钟</div>
        <div class="actions">
          <button :class="{ primary: !archive.data.noteProgress[id]?.done }" @click="markDone">
            {{ archive.data.noteProgress[id]?.done ? '✓ 已读完（点击取消）' : '标记为已读完' }}
          </button>
          <button @click="goDrill">做本章练习 →</button>
        </div>
      </div>
      <MdView :source="parsed.body" />
      <div class="pager">
        <button v-if="prev" @click="router.push(`/notes/${prev.id}`)">← {{ prev.title }}</button>
        <span v-else />
        <button v-if="next" @click="router.push(`/notes/${next.id}`)">{{ next.title }} →</button>
      </div>
    </article>
  </div>
  <div v-else class="card">未找到该章节。</div>
</template>

<style scoped>
.reader { display: flex; gap: 18px; align-items: flex-start; }
.toc {
  width: 230px;
  flex: none;
  position: sticky;
  top: 18px;
  max-height: calc(100vh - 60px);
  overflow-y: auto;
  padding: 14px;
}
.toc-head { margin-bottom: 6px; }
.toc-item { display: block; padding: 3px 0; color: var(--ink-2); font-size: 13px; }
.toc-item.l3 { padding-left: 14px; font-size: 12px; color: var(--ink-3); }
.toc-item:hover { color: var(--accent); text-decoration: none; }
.content { flex: 1; min-width: 0; max-height: calc(100vh - 70px); overflow-y: auto; padding-right: 6px; }
.thead { margin-bottom: 14px; }
.actions { display: flex; gap: 10px; margin-top: 12px; }
.pager { display: flex; justify-content: space-between; margin-top: 30px; }
@media (max-width: 900px) { .toc { display: none; } }
</style>
