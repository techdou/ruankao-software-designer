<script setup lang="ts">
// 收藏夹
import { computed, ref } from 'vue'
import { PLAYABLE } from '../data/bank'
import { useArchive } from '../stores/archive'
import QuestionCard from '../components/QuestionCard.vue'

const archive = useArchive()
const session = ref<string[]>([])
const cur = ref(0)

const favs = computed(() => PLAYABLE.filter((q) => archive.bookmarks.has(q.id)))

function start() {
  session.value = favs.value.map((q) => q.id)
  cur.value = 0
}

const q = computed(() => {
  const id = session.value[cur.value]
  return PLAYABLE.find((x) => x.id === id)
})
</script>

<template>
  <div>
    <h1>收藏夹</h1>
    <p class="muted">典型题、易错题点个收藏，考前集中重刷。</p>

    <div v-if="!favs.length" class="empty">
      <img :src="'/art/scene-fav-empty.png'" alt="收藏夹还是空的" />
      <p>收藏夹还是空的。做题时点「☆ 收藏」，典型题和易错题就会住进这里。</p>
    </div>

    <div v-else-if="!session.length" class="card">
      共 {{ favs.length }} 道收藏题。
      <button class="primary" style="margin-left: 12px" @click="start">开始重刷</button>
    </div>

    <template v-else>
      <div class="meta card">第 {{ cur + 1 }} / {{ session.length }} 题</div>
      <QuestionCard v-if="q" :key="q.id + 'f'" :q="q" mode="practice" />
      <div class="pager">
        <button :disabled="cur === 0" @click="cur--">← 上一题</button>
        <button class="primary" :disabled="cur === session.length - 1" @click="cur++">下一题 →</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.meta { padding: 10px 16px; margin-bottom: 12px; }
.pager { display: flex; justify-content: space-between; margin-top: 4px; }
.empty { text-align: center; padding: 20px 0; }
.empty img { max-width: 420px; width: 100%; border-radius: var(--radius-lg); }
.empty p { color: var(--ink-2); }
</style>
