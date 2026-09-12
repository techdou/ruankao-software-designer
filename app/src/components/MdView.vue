<script setup lang="ts">
// Markdown 渲染：marked + DOMPurify + KaTeX（$行内 / $$块级）
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import katex from 'katex'

const props = defineProps<{ source: string }>()

function renderMath(src: string): string {
  // 块级 $$...$$
  src = src.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => {
    try {
      return katex.renderToString(tex.trim(), { displayMode: true, throwOnError: false })
    } catch {
      return _
    }
  })
  // 行内 $...$（排除 $ 后紧跟空白的开头，避免误伤货币符号）
  src = src.replace(/\$([^\n$]+?)\$/g, (_, tex) => {
    try {
      return katex.renderToString(tex.trim(), { displayMode: false, throwOnError: false })
    } catch {
      return _
    }
  })
  return src
}

const html = computed(() => {
  const withMath = renderMath(props.source ?? '')
  const raw = marked.parse(withMath, { async: false, breaks: true }) as string
  return DOMPurify.sanitize(raw, { ADD_ATTR: ['target'] })
})
</script>

<template>
  <div class="md" v-html="html" />
</template>
