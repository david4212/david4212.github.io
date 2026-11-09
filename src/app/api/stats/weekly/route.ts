import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getUserId } from "@/lib/session-user";
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
    streak: user ? { current: effectiveStreak(user), longest: user.longestStreak } : { current: 0, longest: 0 },
  });
}
