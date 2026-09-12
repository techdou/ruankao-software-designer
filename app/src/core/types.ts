// 题库与存档的核心数据模型

export type OptKey = 'A' | 'B' | 'C' | 'D'

export interface ChoiceQuestion {
  id: string
  kind: 'real' | 'drill'          // 真题 / 分章练习
  term: string                     // 真题卷期，如 "2021年上半年"；练习题为空
  no: number                       // 卷内题号（真题），练习题为 0
  chapter: string                  // 章节 id，如 "ch04"
  knowledge: string                // 知识点标签，如 "二叉树—遍历"
  difficulty: 1 | 2 | 3 | 4 | 5
  stem: string
  options: Partial<Record<OptKey, string>>
  answer: OptKey | ''              // 待补答案的题为空串
  analysis: string
  figure?: string[]                 // 配图（public/figures/ 下文件名），共干题共用
  figureMissing?: boolean          // 原卷含图但源 PDF 未印/未能提取
}

export interface CaseSubQuestion {
  no: number
  stem: string
  answer: string
  analysis: string
}

export interface CaseQuestion {
  id: string
  caseType: 'dfd' | 'db' | 'uml' | 'algo' | 'pattern'
  term: string
  title: string                    // "试题一"
  background: string
  figure?: string                  // figures.ts 注册表 key
  subQuestions: CaseSubQuestion[]
}

export interface ChapterMeta {
  id: string                       // "ch01"
  title: string
  subtitle: string
  weight: number                   // 上午卷分值权重（约数）
  keyPoints: string[]              // 高频考点短句
}

// ---------- 用户存档 ----------

export interface Attempt {
  choice: OptKey | ''              // '' = 案例/未作答
  correct: boolean
  at: string                       // ISO 时间
  caseScore?: number               // 案例小题得分 0/1
}

export interface SrsCard {
  stage: number                    // 0..5，连对升级；stage 5 = 毕业
  dueAt: string                    // 下次复习时间 ISO
  wrongCount: number
}

export interface ArchiveData {
  version: 1
  attempts: Record<string, Attempt>
  srs: Record<string, SrsCard>
  bookmarks: string[]
  noteProgress: Record<string, { ratio: number; lastAt: string; done: boolean }>
  history: { qid: string; correct: boolean; at: string }[]  // 作答流水（统计用）
  streak: { lastDate: string; days: number }
  settings: { dailyCount: number; examMinutes: number }
}
