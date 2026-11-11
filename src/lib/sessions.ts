import { calculateNmtScore, averageNmt } from "@/lib/score";
import prisma from "@/lib/prisma";
import { recordAnswers, shuffle, type AnswerSource } from "@/lib/answers";
import { SUBJECT_DETAILS, type Subject } from "@/types";
import { verifiedQuestionWhere } from "@/lib/history-review";

export const SUBJECTS: Subject[] = ["UKRAINIAN", "MATH", "HISTORY", "ENGLISH"];

// Діагностика: 4 × 5 = 20 питань без таймера. Симуляція: 4 × 10 = 40 питань, 90 хв.
export const KINDS = {
  DIAGNOSTIC: { perSubject: 5, minutes: null as number | null },
  SIMULATION: { perSubject: 10, minutes: 90 },
} as const;
export type Kind = keyof typeof KINDS;

// Збирає питання на льоту: рівномірно по предметах, випадкові, порядок перемішано
export async function buildQuestionIds(kind: Kind): Promise<string[]> {
  const { perSubject } = KINDS[kind];
  const ids: string[] = [];
  for (const subject of SUBJECTS) {
    const rows = await prisma.question.findMany({ where: { topic: { subject }, ...verifiedQuestionWhere }, select: { id: true } });
    ids.push(...shuffle(rows.map((r) => r.id)).slice(0, perSubject));
  }
  return shuffle(ids);
}

export async function loadQuestions(ids: string[]) {
  const rows = await prisma.question.findMany({
    where: { id: { in: ids }, ...verifiedQuestionWhere },
    select: { id: true, text: true, options: true, imageUrl: true, topic: { select: { subject: true } } },
  });
  const map = new Map(rows.map((r) => [r.id, r]));
  return ids
    .map((id) => map.get(id))
    .filter((q): q is NonNullable<typeof q> => !!q)
    .map(({ topic, ...q }) => ({ ...q, subject: topic.subject as Subject }));
}

// Оцінює сесію й один раз записує відповіді (банк помилок, streak). Повторний виклик лише перераховує результат.
export async function finishSession(sessionId: string, userId: string) {
  const s = await prisma.testSession.findFirst({ where: { id: sessionId, userId } });
  if (!s) return null;

  const saved = (s.answers && typeof s.answers === "object" ? s.answers : {}) as Record<string, number>;
  const qs = await prisma.question.findMany({
    where: { id: { in: s.questionIds }, ...verifiedQuestionWhere },
    select: { id: true, correctIndex: true, explanation: true, topic: { select: { subject: true } } },
  });
  const map = new Map(qs.map((q) => [q.id, q]));

  const details = s.questionIds
    .map((id) => map.get(id))
    .filter((q): q is NonNullable<typeof q> => !!q)
    .map((q) => {
      const chosen = typeof saved[q.id] === "number" ? saved[q.id] : null;
      return { id: q.id, subject: q.topic.subject as Subject, chosen, correctIndex: q.correctIndex, explanation: q.explanation, isCorrect: chosen === q.correctIndex };
    });

  const correct = details.filter((d) => d.isCorrect).length;
  const total = details.length;
  const percent = total ? Math.round((correct / total) * 100) : 0;

  if (s.status !== "FINISHED") {
    // Атомарно "захоплюємо" завершення, щоб паралельні запити не записали відповіді двічі
    const claimed = await prisma.testSession.updateMany({
      where: { id: s.id, status: "IN_PROGRESS" },
      data: { status: "FINISHED", finishedAt: new Date(), correct, total, percent },
    });
    if (claimed.count === 1) {
      await recordAnswers(
        userId,
        details.map((d) => ({ questionId: d.id, chosen: d.chosen, isCorrect: d.isCorrect })),
        s.kind as AnswerSource,
        s.id
      );
    }
  }

  const perSubject = SUBJECTS.map((subject) => {
    const part = details.filter((d) => d.subject === subject);
    const c = part.filter((d) => d.isCorrect).length;
    return { subject, title: SUBJECT_DETAILS[subject].title, correct: c, total: part.length, percent: part.length ? Math.round((c / part.length) * 100) : 0, nmt: calculateNmtScore(subject, c, part.length) };
  });
  const avgNmt = averageNmt(perSubject.filter((p) => p.total).map((p) => p.nmt));

  return { id: s.id, kind: s.kind, correct, total, percent, perSubject, avgNmt, details };
}
