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
