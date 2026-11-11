export type Subject = "UKRAINIAN" | "MATH" | "HISTORY" | "ENGLISH";

// Усі класи записані повними рядками, щоб Tailwind їх підхопив
export type SubjectTheme = {
  title: string;
  bgClass: string; // суцільний колір (смужки, точки)
  gradient: string; // градієнт блоку
  soft: string; // напівпрозорий акцент
  pill: string; // бейдж
  text: string; // колір тексту-акценту
  bar: string; // заповнення прогрес-бару
};

export const SUBJECT_DETAILS: Record<Subject, SubjectTheme> = {
  UKRAINIAN: {
    title: "Українська мова",
    bgClass: "bg-emerald-500",
    gradient: "from-emerald-500 to-teal-700",
    soft: "bg-emerald-100/20",
    pill: "bg-emerald-100 text-emerald-800",
    text: "text-emerald-600",
    bar: "bg-emerald-300",
  },
  HISTORY: {
    title: "Історія України",
    bgClass: "bg-amber-500",
    gradient: "from-amber-500 to-orange-700",
    soft: "bg-amber-100/20",
    pill: "bg-amber-100 text-amber-800",
    text: "text-amber-600",
    bar: "bg-amber-300",
  },
  MATH: {
    title: "Математика",
    bgClass: "bg-blue-600",
    gradient: "from-blue-600 to-indigo-800",
    soft: "bg-blue-100/20",
    pill: "bg-blue-100 text-blue-800",
    text: "text-blue-600",
    bar: "bg-blue-300",
  },
  ENGLISH: {
    title: "Англійська мова",
    bgClass: "bg-violet-600",
    gradient: "from-violet-600 to-purple-800",
    soft: "bg-violet-100/20",
    pill: "bg-violet-100 text-violet-800",
    text: "text-violet-600",
    bar: "bg-violet-300",
  },
};

export const SUBJECT_ORDER: Subject[] = ["UKRAINIAN", "MATH", "HISTORY", "ENGLISH"];

// ───────── Типи питань НМТ ─────────
export type QuestionType = "single_choice" | "matching" | "sequencing" | "choose_multi" | "fill_blanks" | "short_answer";

// Metadata для кожного типу питання:
// matching: { pairs: [[left, right], ...], leftLabels?: string[], rightLabels?: string[] }
//   — завдання на відповідність. Відповідь = масив індексів правильних пар
// sequencing: { items: string[], correctOrder: number[] }
//   — завдання на послідовність. Відповідь = порядок індексів
// choose_multi: { correctIndices: number[], requiredCount: number }
//   — вибір кількох відповідей (3 із 7). Відповідь = масив обраних індексів
// fill_blanks: { blanks: { answer: string, alternatives?: string[] }[] }
//   — заповнення пропусків. Відповідь = масив текстових значень
// short_answer: { answer: number | string, tolerance?: number }
//   — коротка відповідь (зазвичай число). Відповідь = рядок або число

export type MatchingMeta = { pairs: [string, string][]; leftLabels?: string[]; rightLabels?: string[] };
export type SequencingMeta = { items: string[]; correctOrder: number[] };
export type ChooseMultiMeta = { correctIndices: number[]; requiredCount: number };
export type FillBlanksMeta = { blanks: { answer: string; alternatives?: string[] }[] };
export type ShortAnswerMeta = { answer: number | string; tolerance?: number };

export type QuestionMeta = MatchingMeta | SequencingMeta | ChooseMultiMeta | FillBlanksMeta | ShortAnswerMeta;

// ───────── Конфігурація пробника НМТ ─────────
export const NMT_CONFIG = {
  UKRAINIAN: { questions: 30, minutes: 60, maxRaw: 45 },
  MATH:      { questions: 22, minutes: 60, maxRaw: 32 },
  HISTORY:   { questions: 30, minutes: 60, maxRaw: 54 },
  ENGLISH:   { questions: 32, minutes: 60, maxRaw: 32 },
} as const;

export const NMT_TOTAL_QUESTIONS = Object.values(NMT_CONFIG).reduce((s, c) => s + c.questions, 0); // 114

// Рівні складності пробника
export type ProbnikDifficulty = 1 | 2 | 3;
export const DIFFICULTY_LABELS: Record<ProbnikDifficulty, { label: string; description: string; hardPercent: number }> = {
  1: { label: "Легкий", description: "30% складних питань", hardPercent: 30 },
  2: { label: "Середній", description: "50% складних питань", hardPercent: 50 },
  3: { label: "Важкий", description: "80% складних питань", hardPercent: 80 },
};
