import { calculateNmtScore, averageNmt } from "@/lib/score";
import prisma from "@/lib/prisma";
import { recordAnswers, shuffle, type AnswerSource } from "@/lib/answers";
import { SUBJECT_DETAILS, SUBJECT_ORDER, NMT_CONFIG, type Subject, type ProbnikDifficulty } from "@/types";
import { verifiedQuestionWhere } from "@/lib/history-review";

export const SUBJECTS: Subject[] = ["UKRAINIAN", "MATH", "HISTORY", "ENGLISH"];

// Діагностика: 4 × 5 = 20 питань без таймера.
// Пробник НМТ: UA 30, Math 22, History 30, English 32 = 114 питань, 60 хв/предмет (загалом 240 хв)
export const KINDS = {
  DIAGNOSTIC: { perSubject: 5, minutes: null as number | null },
  SIMULATION: { perSubject: null as number | null, minutes: 240 }, // пробник НМТ (було: 10 за предмет, 90 хв)
} as const;
export type Kind = keyof typeof KINDS;

/**
 * Збирає питання для пробника НМТ з урахуванням складності.
 * difficulty: 1 = Easy (30% hard), 2 = Medium (50% hard), 3 = Hard (80% hard)
 * hardPercent — відсоток питань testLevel=3 у тесті.
 * Решта — рівномірно з testLevel 1 і 2.
 */
export async function buildQuestionIds(kind: Kind, difficulty: ProbnikDifficulty = 2): Promise<string[]> {
  // Для історії додаємо фільтр верифікованих питань
  const historyFilter = (subject: string) => subject === "HISTORY" ? verifiedQuestionWhere : {};

  if (kind === "DIAGNOSTIC") {
    const ids: string[] = [];
    for (const subject of SUBJECTS) {
      const rows = await prisma.question.findMany({
        where: { topic: { subject }, questionType: "single_choice", ...historyFilter(subject) },
        select: { id: true },
      });
      ids.push(...shuffle(rows.map((r) => r.id)).slice(0, 5));
    }
    return shuffle(ids);
  }

  // Пробник НМТ — реальна кількість питань по предметах
  const hardPercent = { 1: 30, 2: 50, 3: 80 }[difficulty] ?? 50;
  const ids: string[] = [];

  for (const subject of SUBJECTS) {
    const needed = NMT_CONFIG[subject].questions;
    const hardCount = Math.round((needed * hardPercent) / 100);
    const easyMedCount = needed - hardCount;

    // Отримуємо hard (testLevel=3) і easy/medium (testLevel 1-2) окремо
    const hFilter = historyFilter(subject);
    const [hardRows, easyMedRows] = await Promise.all([
      prisma.question.findMany({
        where: { topic: { subject }, testLevel: 3, questionType: "single_choice", ...hFilter },
        select: { id: true },
      }),
      prisma.question.findMany({
        where: { topic: { subject }, testLevel: { in: [1, 2] }, questionType: "single_choice", ...hFilter },
        select: { id: true },
      }),
    ]);

    const hard = shuffle(hardRows.map((r) => r.id)).slice(0, hardCount);
    const easyMed = shuffle(easyMedRows.map((r) => r.id)).slice(0, easyMedCount);

    // Якщо одного рівня не вистачає — добираємо з іншого
    let pool = [...hard, ...easyMed];
    if (pool.length < needed) {
      const usedSet = new Set(pool);
      const allRows = await prisma.question.findMany({
        where: { topic: { subject }, questionType: "single_choice", ...hFilter },
        select: { id: true },
      });
      const extra = shuffle(allRows.map((r) => r.id).filter((id) => !usedSet.has(id)));
      pool.push(...extra.slice(0, needed - pool.length));
    }

    ids.push(...pool.slice(0, needed));
  }

  return shuffle(ids);
}

export async function loadQuestions(ids: string[]) {
  const rows = await prisma.question.findMany({
    where: { id: { in: ids }, ...verifiedQuestionWhere },
    select: { id: true, text: true, options: true, imageUrl: true, questionType: true, metadata: true, topic: { select: { subject: true } } },
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

  const saved = (s.answers && typeof s.answers === "object" ? s.answers : {}) as Record<string, any>;
  const qs = await prisma.question.findMany({
    where: { id: { in: s.questionIds }, ...verifiedQuestionWhere },
    select: { id: true, correctIndex: true, explanation: true, questionType: true, metadata: true, topic: { select: { subject: true } } },
  });
  const map = new Map(qs.map((q) => [q.id, q]));

  const details = s.questionIds
    .map((id) => map.get(id))
    .filter((q): q is NonNullable<typeof q> => !!q)
    .map((q) => {
      const ans = saved[q.id];
      const qType = q.questionType ?? "single_choice";
      const meta = q.metadata as any;
      let isCorrect = false;
      let chosen: number | null = null;

      if (qType === "single_choice") {
        chosen = typeof ans === "number" ? ans : null;
        isCorrect = chosen === q.correctIndex;
      } else if (qType === "matching" && Array.isArray(ans) && meta?.pairs) {
        // correct when user's order matches 0,1,2,... (pairs are in correct order in DB)
        isCorrect = ans.length === meta.pairs.length && ans.every((v: number, i: number) => v === i);
      } else if (qType === "sequencing" && Array.isArray(ans) && meta?.correctOrder) {
        isCorrect = JSON.stringify(ans) === JSON.stringify(meta.correctOrder);
      } else if (qType === "choose_multi" && Array.isArray(ans) && meta?.correctIndices) {
        isCorrect = JSON.stringify([...ans].sort()) === JSON.stringify([...meta.correctIndices].sort());
      } else if (qType === "fill_blanks" && Array.isArray(ans) && meta?.blanks) {
        isCorrect = meta.blanks.every((b: { answer: string; alternatives?: string[] }, i: number) => {
          const userVal = (ans[i] ?? "").trim().toLowerCase();
          if (userVal === b.answer.trim().toLowerCase()) return true;
          return b.alternatives?.some((a: string) => a.trim().toLowerCase() === userVal) ?? false;
        });
      } else if (qType === "short_answer" && typeof ans === "string" && meta?.answer !== undefined) {
        const userVal = ans.trim();
        if (typeof meta.answer === "number") {
          const num = parseFloat(userVal);
          const tolerance = meta.tolerance ?? 0;
          isCorrect = !isNaN(num) && Math.abs(num - meta.answer) <= tolerance;
        } else {
          isCorrect = userVal.toLowerCase() === String(meta.answer).trim().toLowerCase();
        }
      }

      return { id: q.id, subject: q.topic.subject as Subject, chosen, correctIndex: q.correctIndex, explanation: q.explanation, isCorrect };
    });

  const correct = details.filter((d) => d.isCorrect).length;
  const total = details.length;
  const percent = total ? Math.round((correct / total) * 100) : 0;

  const perSubject = SUBJECTS.map((subject) => {
    const part = details.filter((d) => d.subject === subject);
    const c = part.filter((d) => d.isCorrect).length;
    return { subject, title: SUBJECT_DETAILS[subject].title, correct: c, total: part.length, percent: part.length ? Math.round((c / part.length) * 100) : 0, nmt: calculateNmtScore(subject, c, part.length) };
  });
  const avgNmt = averageNmt(perSubject.filter((p) => p.total).map((p) => p.nmt));

  if (s.status !== "FINISHED") {
    // Атомарно "захоплюємо" завершення, щоб паралельні запити не записали відповіді двічі
    const claimed = await prisma.testSession.updateMany({
      where: { id: s.id, status: "IN_PROGRESS" },
      data: {
        status: "FINISHED",
        finishedAt: new Date(),
        correct,
        total,
        percent,
        nmtScore: avgNmt,
        subjectScores: perSubject.map((p) => ({ subject: p.subject, correct: p.correct, total: p.total, nmtScore: p.nmt.nmtScore, isPassed: p.nmt.isPassed })),
      },
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

  return { id: s.id, kind: s.kind, correct, total, percent, perSubject, avgNmt, details };
}
