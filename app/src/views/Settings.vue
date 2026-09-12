<script setup lang="ts">
// 存档：导入/导出/重置 + 每日题量设置
import { ref } from 'vue'
import { useArchive } from '../stores/archive'

const archive = useArchive()
const summary = ref<string>('')
const pendingImport = ref('')
const msg = ref('')

function download() {
  const blob = new Blob([archive.exportJSON()], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ruankao-sd-archive-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
  msg.value = '已导出到浏览器下载目录。'
}

async function onFile(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (!f) return
  pendingImport.value = await f.text()
  try {
    const s = archive.importSummary(pendingImport.value)
    summary.value = `导出时间：${s.exportedAt} · 作答记录 ${s.attempts} 条 · 收藏 ${s.bookmarks} 个 · 连续学习 ${s.streakDays} 天`
  } catch (err: any) {
    msg.value = '文件解析失败：' + err.message
    pendingImport.value = ''
  }
}

async function doImport() {
  await archive.importJSON(pendingImport.value)
  msg.value = '导入成功，当前进度已替换。'
  pendingImport.value = ''
  summary.value = ''
}

async function resetAll() {
  if (confirm('确定清空全部学习记录？此操作不可恢复（建议先导出备份）。')) {
    await archive.resetAll()
    msg.value = '已清空。'
  }
}

function setDaily(v: number) {
  archive.updateSettings({ dailyCount: v })
}
function setExamMinutes(v: number) {
  archive.updateSettings({ examMinutes: v })
}
</script>

<template>
  <div>
    <h1>学习存档</h1>
    <p class="muted">进度自动保存在本机浏览器（IndexedDB）。换设备用导出/导入迁移。</p>

    <div class="card">
      <h3>导出备份</h3>
      <p class="small muted">导出作答记录、错题复习队列、收藏、讲义阅读进度、连续打卡。</p>
      <button class="primary" @click="download">导出 JSON 存档</button>
    </div>

    <div class="card" style="margin-top: 14px">
      <h3>导入存档</h3>
      <input type="file" accept=".json" @change="onFile" />
      <div v-if="summary" class="importsum">
        <p>{{ summary }}</p>
        <button class="primary" @click="doImport">确认导入（覆盖当前进度）</button>
      </div>
    </div>

    <div class="card" style="margin-top: 14px">
      <h3>偏好设置</h3>
      <div class="setrow">
        <span>每次复习题量</span>
        <select :value="archive.data.settings.dailyCount" @change="setDaily(+($event.target as any).value)">
          <option :value="10">10 题</option>
          <option :value="20">20 题</option>
          <option :value="30">30 题</option>
          <option :value="50">50 题</option>
        </select>
      </div>
      <div class="setrow">
        <span>模拟考试时长（分钟）</span>
        <select :value="archive.data.settings.examMinutes" @change="setExamMinutes(+($event.target as any).value)">
          <option :value="90">90</option>
          <option :value="120">120</option>
          <option :value="150">150（与实考一致）</option>
        </select>
      </div>
    </div>

    <div class="card danger" style="margin-top: 14px">
      <h3>危险操作</h3>
      <button class="reset" @click="resetAll">清空全部学习记录</button>
    </div>

    <p v-if="msg" class="msg">{{ msg }}</p>
  </div>
</template>

<style scoped>
.card { padding: 18px 22px; }
.importsum { margin-top: 10px; padding: 10px 14px; background: var(--accent-weak); border-radius: var(--radius); }
.setrow { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; max-width: 380px; }
select { font: inherit; padding: 6px 10px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); }
.danger { border-color: var(--danger-weak); }
.reset { color: var(--danger); border-color: var(--danger); }
.reset:hover { background: var(--danger-weak); border-color: var(--danger); }
.msg { margin-top: 12px; color: var(--accent); font-weight: 600; }
input[type='file'] { font: inherit; }
</style>
