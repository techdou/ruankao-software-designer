// 存档层：IndexedDB 持久化 + Pinia 状态 + JSON 导入导出
import { defineStore } from 'pinia'
import type { ArchiveData, Attempt, SrsCard, OptKey } from '../core/types'
import { onAnswer, nextStreak } from '../core/srs'

const DB_NAME = 'ruankao-sd'
const STORE = 'archive'
const KEY = 'main'

export function emptyArchive(): ArchiveData {
  return {
    version: 1,
    attempts: {},
    srs: {},
    bookmarks: [],
    noteProgress: {},
    history: [],
    streak: { lastDate: '', days: 0, best: 0 },
    settings: { dailyCount: 20, examMinutes: 150 },
  }
}

let dbp: Promise<IDBDatabase> | null = null

function openDB(): Promise<IDBDatabase> {
  if (dbp) return dbp
  dbp = new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1)
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(STORE)) req.result.createObjectStore(STORE)
    }
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
  })
  return dbp
}

async function loadRaw(): Promise<ArchiveData> {
  try {
    const db = await openDB()
    return await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readonly')
      const req = tx.objectStore(STORE).get(KEY)
      req.onsuccess = () => resolve(req.result ? { ...emptyArchive(), ...req.result } : emptyArchive())
      req.onerror = () => reject(req.error)
    })
  } catch {
    return emptyArchive()
  }
}

async function saveRaw(data: ArchiveData): Promise<void> {
  const db = await openDB()
  // Pinia 的 reactive Proxy 不能 structuredClone，先落成 plain 对象
  const plain = JSON.parse(JSON.stringify(data)) as ArchiveData
  await new Promise<void>((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite')
    tx.objectStore(STORE).put(plain, KEY)
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

export const useArchive = defineStore('archive', {
  state: () => ({ data: emptyArchive(), ready: false }),
  getters: {
    attempts: (s) => s.data.attempts,
    bookmarks: (s) => new Set(s.data.bookmarks),
    doneCount: (s) => Object.keys(s.data.attempts).length,
    correctCount: (s) => Object.values(s.data.attempts).filter((a) => a.correct).length,
  },
  actions: {
    async init() {
      this.data = await loadRaw()
      this.ready = true
    },
    async record(qid: string, choice: OptKey | '', correct: boolean) {
      const d = this.data
      d.attempts[qid] = { choice, correct, at: new Date().toISOString() } as Attempt
      d.srs[qid] = onAnswer(d.srs[qid] as SrsCard | undefined, correct)
      d.history.push({ qid, correct, at: d.attempts[qid].at })
      if (d.history.length > 5000) d.history.splice(0, d.history.length - 5000)
      d.streak = nextStreak(d.streak)
      await saveRaw(d)
    },
    async toggleBookmark(qid: string) {
      const arr = this.data.bookmarks
      const i = arr.indexOf(qid)
      if (i >= 0) arr.splice(i, 1)
      else arr.push(qid)
      await saveRaw(this.data)
    },
    async setNoteProgress(chId: string, ratio: number) {
      const prev = this.data.noteProgress[chId]
      this.data.noteProgress[chId] = {
        ratio: Math.max(ratio, prev?.ratio ?? 0),
        lastAt: new Date().toISOString(),
        done: (prev?.done || ratio >= 0.95) ?? false,
      }
      await saveRaw(this.data)
    },
    async markNoteDone(chId: string, done: boolean) {
      const prev = this.data.noteProgress[chId] ?? { ratio: 0, lastAt: '', done: false }
      this.data.noteProgress[chId] = { ...prev, done }
      await saveRaw(this.data)
    },
    async updateSettings(patch: Partial<ArchiveData['settings']>) {
      Object.assign(this.data.settings, patch)
      await saveRaw(this.data)
    },
    exportJSON(): string {
      return JSON.stringify({ ...this.data, exportedAt: new Date().toISOString() }, null, 1)
    },
    importSummary(jsonText: string) {
      const obj = JSON.parse(jsonText)
      if (obj.version !== 1) throw new Error('不支持的存档版本')
      return {
        exportedAt: obj.exportedAt ?? '未知',
        attempts: Object.keys(obj.attempts ?? {}).length,
        bookmarks: (obj.bookmarks ?? []).length,
        streakDays: obj.streak?.days ?? 0,
      }
    },
    async importJSON(jsonText: string) {
      const obj = JSON.parse(jsonText)
      if (obj.version !== 1) throw new Error('不支持的存档版本')
      const base = emptyArchive()
      this.data = { ...base, ...obj }
      await saveRaw(this.data)
    },
    async resetAll() {
      this.data = emptyArchive()
      await saveRaw(this.data)
    },
  },
})
