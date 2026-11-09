import prisma from "@/lib/prisma";
import { touchStreak } from "@/lib/streak";

export type AnswerSource = "TEST" | "ERRORS" | "DIAGNOSTIC" | "SIMULATION" | "DAILY";
export type AnswerItem = { questionId: string; chosen: number | null; isCorrect: boolean };

export const RESOLVE_AFTER = 3; // поспіль правильних відповідей у різних сесіях

// Єдина точка запису відповідей: лог + банк помилок + streak.
// Помилка (в т.ч. пропуск) створює/оновлює UserError і скидає лічильник.
// Правильна відповідь на відкриту помилку рахується, лише якщо сесія відрізняється від попередньої.
export async function recordAnswers(userId: string, items: AnswerItem[], source: AnswerSource, sessionId: string) {
  if (items.length === 0) return;

  await prisma.userAnswer.createMany({
    data: items.map((i) => ({ userId, questionId: i.questionId, chosen: i.chosen, isCorrect: i.isCorrect, source, sessionId })),
  });

  const now = new Date();
  const wrong = items.filter((i) => !i.isCorrect);
  const right = items.filter((i) => i.isCorrect);

  const ops = wrong.map((w) =>
    prisma.userError.upsert({
      where: { userId_questionId: { userId, questionId: w.questionId } },
      create: { userId, questionId: w.questionId, failCount: 1, consecutiveCorrect: 0, isResolved: false, lastSessionId: sessionId, lastAnswerAt: now },
      update: { failCount: { increment: 1 }, consecutiveCorrect: 0, isResolved: false, lastSessionId: sessionId, lastAnswerAt: now },
    })
  );

  if (right.length > 0) {
    const open = await prisma.userError.findMany({
      where: { userId, isResolved: false, questionId: { in: right.map((r) => r.questionId) } },
    });
    for (const e of open) {
      if (e.lastSessionId === sessionId) continue; // та сама сесія — не рахуємо
      const n = e.consecutiveCorrect + 1;
      ops.push(
        prisma.userError.update({
          where: { id: e.id },
          data: { consecutiveCorrect: n, isResolved: n >= RESOLVE_AFTER, lastSessionId: sessionId, lastAnswerAt: now },
        })
      );
    }
  }

  if (ops.length > 0) await prisma.$transaction(ops);
  await touchStreak(userId);
}

export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
