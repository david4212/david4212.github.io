export type Subject = "UKRAINIAN" | "MATH" | "HISTORY" | "ENGLISH";

export const SUBJECT_DETAILS: Record<Subject, { title: string; bgClass: string }> = {
  UKRAINIAN: { title: "Українська мова", bgClass: "bg-ukrainian" },
  MATH: { title: "Математика", bgClass: "bg-math" },
  HISTORY: { title: "Історія України", bgClass: "bg-history" },
  ENGLISH: { title: "Англійська мова", bgClass: "bg-english" },
};
