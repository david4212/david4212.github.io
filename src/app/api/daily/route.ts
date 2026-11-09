import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getUserId } from "@/lib/session-user";
import { kyivDate } from "@/lib/kyiv";
import { getDailyQuestionId } from "@/lib/daily";
import { recordAnswers } from "@/lib/answers";
import { effectiveStreak } from "@/lib/streak";

export const dynamic = "force-dynamic";

// GET — питання дня (без правильної відповіді) + стан користувача й streak
export async function GET() {
  const date = kyivDate();
  const qid = await getDailyQuestionId(date);
  if (!qid) return NextResponse.json({ error: "Немає питань" }, { status: 404 });

  const question = await prisma.question.findUnique({ where: { id: qid }, select: { id: true, text: true, options: true, imageUrl: true } });
  const userId = await getUserId();

  let answered: { chosen: number | null; isCorrect: boolean; correctIndex: number; explanation: string | null } | null = null;
  let streak = 0;
  if (userId) {
    const [prev, user] = await Promise.all([
      prisma.userAnswer.findFirst({ where: { userId, sessionId: `daily-${date}` } }),
      prisma.user.findUnique({ where: { id: userId }, select: { currentStreak: true, lastActiveDate: true } }),
    ]);
    if (user) streak = effectiveStreak(user);
    if (prev) {
      const q = await prisma.question.findUnique({ where: { id: qid }, select: { correctIndex: true, explanation: true } });
      answered = { chosen: prev.chosen, isCorrect: prev.isCorrect, correctIndex: q!.correctIndex, explanation: q!.explanation };
    }
  }
  return NextResponse.json({ date, question, answered, streak });
}

// POST { chosen } — одна спроба на добу
export async function POST(req: Request) {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const chosen = typeof body?.chosen === "number" ? body.chosen : null;

  const date = kyivDate();
  const qid = await getDailyQuestionId(date);
  if (!qid) return NextResponse.json({ error: "Немає питань" }, { status: 404 });

  const q = await prisma.question.findUnique({ where: { id: qid }, select: { correctIndex: true, explanation: true, options: true } });
  if (!q) return NextResponse.json({ error: "Питання не знайдено" }, { status: 404 });
  if (chosen === null || !Number.isInteger(chosen) || chosen < 0 || chosen >= q.options.length) {
    return NextResponse.json({ error: "Невірний варіант" }, { status: 400 });
  }

  const sessionId = `daily-${date}`;
  const already = await prisma.userAnswer.findFirst({ where: { userId, sessionId }, select: { id: true } });
  const isCorrect = chosen === q.correctIndex;
  if (!already) await recordAnswers(userId, [{ questionId: qid, chosen, isCorrect }], "DAILY", sessionId);

  const user = await prisma.user.findUnique({ where: { id: userId }, select: { currentStreak: true, lastActiveDate: true } });
  return NextResponse.json({
    correct: isCorrect,
    correctIndex: q.correctIndex,
    explanation: q.explanation,
    alreadyAnswered: !!already,
    streak: user ? effectiveStreak(user) : 0,
  });
}
