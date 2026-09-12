<script setup lang="ts">
// 圆环进度
const props = withDefaults(defineProps<{ value: number; size?: number; label?: string }>(), {
  size: 96,
  label: '',
})
const r = 40
const c = 2 * Math.PI * r
const dash = Math.min(Math.max(props.value, 0), 1) * c
</script>

<template>
  <div class="ring" :style="{ width: size + 'px', height: size + 'px' }">
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" :r="r" fill="none" stroke="var(--line)" stroke-width="9" />
      <circle
        cx="50" cy="50" :r="r" fill="none" stroke="var(--accent)" stroke-width="9"
        stroke-linecap="round"
        :stroke-dasharray="`${dash} ${c}`"
        transform="rotate(-90 50 50)"
      />
    </svg>
    <div class="ring-label">
      <b>{{ Math.round(value * 100) }}%</b>
      <span v-if="label">{{ label }}</span>
    </div>
  </div>
</template>

<style scoped>
.ring { position: relative; flex: none; }
.ring svg { width: 100%; height: 100%; }
.ring-label {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.3;
}
.ring-label b { font-size: 18px; }
.ring-label span { font-size: 11px; color: var(--ink-3); }
</style>
