// SRS 间隔复习：答错回 stage0，答对升级；间隔天数逐级拉长
import type { SrsCard } from './types'

export const STAGE_DAYS = [1, 2, 4, 7, 15, 30] as const
export const GRADUATED = STAGE_DAYS.length // stage 达到 5 视为掌握毕业

export function newCard(now = new Date()): SrsCard {
  return { stage: 0, dueAt: addDays(now, STAGE_DAYS[0]).toISOString(), wrongCount: 1 }
}

export function onAnswer(card: SrsCard | undefined, correct: boolean, now = new Date()): SrsCard {
  if (!card) {
    if (correct) {
      // 首答即对：不进复习队列（记录一次尝试即可）
      return { stage: GRADUATED, dueAt: '', wrongCount: 0 }
    }
    return newCard(now)
  }
  if (correct) {
    const stage = Math.min(card.stage + 1, GRADUATED)
    const done = stage >= GRADUATED
    return { ...card, stage, dueAt: done ? '' : addDays(now, STAGE_DAYS[stage]).toISOString() }
  }
  return { stage: 0, dueAt: addDays(now, STAGE_DAYS[0]).toISOString(), wrongCount: card.wrongCount + 1 }
}

export function isDue(card: SrsCard | undefined, now = new Date()): boolean {
  if (!card || !card.dueAt) return false
  if (card.stage >= GRADUATED) return false
  return new Date(card.dueAt).getTime() <= now.getTime()
}

function addDays(d: Date, n: number): Date {
  const x = new Date(d)
  x.setDate(x.getDate() + n)
  return x
}

// 连续打卡：与上次学习日相邻则 +1，否则重置为 1
export function nextStreak(streak: { lastDate: string; days: number }, now = new Date()) {
  const today = now.toISOString().slice(0, 10)
  if (streak.lastDate === today) return streak
  const yest = new Date(now)
  yest.setDate(yest.getDate() - 1)
  const yestStr = yest.toISOString().slice(0, 10)
  return {
    lastDate: today,
    days: streak.lastDate === yestStr ? streak.days + 1 : 1,
  }
}
