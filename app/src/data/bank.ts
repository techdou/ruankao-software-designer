// 题库加载与筛选
import rawReal from './bank/real-choice-raw.json'
import rawDrillA from './bank/drill-a.json'
import rawDrillB from './bank/drill-b.json'
import type { ChoiceQuestion, OptKey } from '../core/types'

export const REAL_QUESTIONS: ChoiceQuestion[] = (rawReal as any[]).map((q) => ({
  id: q.id,
  kind: 'real' as const,
  term: q.term,
  no: q.no,
  chapter: q.chapter || '',
  knowledge: q.knowledge || '',
  difficulty: (q.difficulty || 3) as 1 | 2 | 3 | 4 | 5,
  stem: q.stem,
  options: q.options,
  answer: (q.answer || '') as OptKey | '',
  analysis: q.analysis || '',
  figureMissing: !!q.figureMissing,
}))

export const DRILL_QUESTIONS: ChoiceQuestion[] = [
  ...(rawDrillA as any[]),
  ...(rawDrillB as any[]),
].map((q) => ({
  id: q.id,
  kind: 'drill' as const,
  term: '',
  no: 0,
  chapter: q.chapter,
  knowledge: q.knowledge || '',
  difficulty: (q.difficulty || 3) as 1 | 2 | 3 | 4 | 5,
  stem: q.stem,
  options: q.options,
  answer: q.answer,
  analysis: q.analysis || '',
}))

export const ALL_QUESTIONS: ChoiceQuestion[] = [...REAL_QUESTIONS, ...DRILL_QUESTIONS]
// 有确定答案且选项齐全的题才可作答
export const PLAYABLE = ALL_QUESTIONS.filter((q) => q.answer && Object.keys(q.options).length === 4)

export const byId = new Map(ALL_QUESTIONS.map((q) => [q.id, q]))

export const TERMS = [...new Set(REAL_QUESTIONS.map((q) => q.term))].filter(Boolean)

export function paperQuestions(term: string): ChoiceQuestion[] {
  return REAL_QUESTIONS.filter((q) => q.term === term && q.answer).sort((a, b) => a.no - b.no)
}

export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}
