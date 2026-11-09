import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getUserId } from "@/lib/session-user";
import { calculateNmtScore, averageNmt } from "@/lib/score";
import { effectiveStreak } from "@/lib/streak";

export const dynamic = "force-dynamic";

const MIN_ANSWERS = 3; // менше — замало даних для висновку

// Аналітика за останні 7 днів: «Сильні сторони» (>80%) та «Пастки» (<60%) по темах
export async function GET() {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const since = new Date(Date.now() - 7 * 24 * 3600 * 1000);
  const [rows, user, openErrors] = await Promise.all([
    prisma.userAnswer.findMany({
      where: { userId, createdAt: { gte: since } },
      select: { isCorrect: true, question: { select: { topic: { select: { id: true, title: true, subject: true } } } } },
    }),
    prisma.user.findUnique({ where: { id: userId }, select: { currentStreak: true, longestStreak: true, lastActiveDate: true } }),
    prisma.userError.count({ where: { userId, isResolved: false } }),
  ]);

  // Останній завершений тест (діагностика/симуляція) з перерахунком у шкалу 100–200
  let lastTest: { kind: string; avgNmt: number | null; subjects: { subject: string; correct: number; total: number; nmtScore: number | null }[] } | null = null;
  const last = await prisma.testSession.findFirst({ where: { userId, status: "FINISHED" }, orderBy: { finishedAt: "desc" } });
  if (last) {
    const qs = await prisma.question.findMany({ where: { id: { in: last.questionIds } }, select: { id: true, correctIndex: true, topic: { select: { subject: true } } } });
    const saved = (last.answers && typeof last.answers === "object" ? last.answers : {}) as Record<string, number>;
    const bySub = new Map<string, { correct: number; total: number }>();
    for (const q of qs) {
      const e = bySub.get(q.topic.subject) ?? { correct: 0, total: 0 };
      e.total += 1;
      if (saved[q.id] === q.correctIndex) e.correct += 1;
      bySub.set(q.topic.subject, e);
    }
    const subjects = Array.from(bySub, ([subject, v]) => ({ subject, ...v, calc: calculateNmtScore(subject, v.correct, v.total) }));
    lastTest = { kind: last.kind, avgNmt: averageNmt(subjects.map((x) => x.calc)), subjects: subjects.map((x) => ({ subject: x.subject, correct: x.correct, total: x.total, nmtScore: x.calc.nmtScore })) };
  }

  const map = new Map<string, { topicId: string; title: string; subject: string; correct: number; total: number }>();
  for (const r of rows) {
    const t = r.question.topic;
    const e = map.get(t.id) ?? { topicId: t.id, title: t.title, subject: t.subject, correct: 0, total: 0 };
    e.total += 1;
    if (r.isCorrect) e.correct += 1;
    map.set(t.id, e);
  }

  const topics = Array.from(map.values())
    .filter((t) => t.total >= MIN_ANSWERS)
    .map((t) => ({ ...t, percent: Math.round((t.correct / t.total) * 100) }));

  return NextResponse.json({
    answers: rows.length,
    strengths: topics.filter((t) => t.percent > 80).sort((a, b) => b.percent - a.percent),
    traps: topics.filter((t) => t.percent < 60).sort((a, b) => a.percent - b.percent),
    openErrors,
    lastTest,
    streak: user ? { current: effectiveStreak(user), longest: user.longestStreak } : { current: 0, longest: 0 },
  });
}
