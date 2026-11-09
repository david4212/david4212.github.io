import { NextResponse } from "next/server";
import { randomUUID } from "crypto";
import prisma from "@/lib/prisma";
import { getUserId } from "@/lib/session-user";
import { recordAnswers, RESOLVE_AFTER, shuffle } from "@/lib/answers";

export const dynamic = "force-dynamic";

// GET /api/errors?limit=20&topicId=... — набір для режиму «Повторення помилок» (без правильних відповідей)
export async function GET(req: Request) {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const url = new URL(req.url);
  const limit = Math.min(Math.max(Number(url.searchParams.get("limit")) || 20, 1), 50);
  const topicId = url.searchParams.get("topicId");

  const where = { userId, isResolved: false, ...(topicId ? { question: { topicId } } : {}) };
  const [open, resolved, rows] = await Promise.all([
    prisma.userError.count({ where }),
    prisma.userError.count({ where: { userId, isResolved: true } }),
    prisma.userError.findMany({
      where,
      take: 200,
      orderBy: { lastAnswerAt: "asc" },
      select: {
        failCount: true,
        consecutiveCorrect: true,
        question: { select: { id: true, text: true, options: true, imageUrl: true, topicId: true } },
      },
    }),
  ]);

  const picked = shuffle(rows).slice(0, limit);
  return NextResponse.json({
    sessionId: randomUUID(),
    open,
    resolved,
    need: RESOLVE_AFTER,
    questions: picked.map((r) => ({ ...r.question, failCount: r.failCount, consecutiveCorrect: r.consecutiveCorrect })),
  });
}

// POST { sessionId, questionId, chosen } — відповідь у режимі повторення; одразу повертає explanation
export async function POST(req: Request) {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const sessionId = typeof body?.sessionId === "string" ? body.sessionId : "";
  const questionId = typeof body?.questionId === "string" ? body.questionId : "";
  const chosen = typeof body?.chosen === "number" ? body.chosen : null;
  if (!sessionId || !questionId) return NextResponse.json({ error: "Невірний запит" }, { status: 400 });

  const q = await prisma.question.findUnique({
    where: { id: questionId },
    select: { correctIndex: true, explanation: true, options: true },
  });
  if (!q) return NextResponse.json({ error: "Питання не знайдено" }, { status: 404 });
  if (chosen !== null && (!Number.isInteger(chosen) || chosen < 0 || chosen >= q.options.length)) {
    return NextResponse.json({ error: "Невірний варіант" }, { status: 400 });
  }

  // Захист від повторного зарахування однієї відповіді в тій самій сесії
  const dup = await prisma.userAnswer.findFirst({ where: { userId, questionId, sessionId }, select: { id: true } });
  const isCorrect = chosen === q.correctIndex;
  if (!dup) await recordAnswers(userId, [{ questionId, chosen, isCorrect }], "ERRORS", sessionId);

  const err = await prisma.userError.findUnique({
    where: { userId_questionId: { userId, questionId } },
    select: { consecutiveCorrect: true, isResolved: true, failCount: true },
  });

  return NextResponse.json({
    correct: isCorrect,
    correctIndex: q.correctIndex,
    explanation: q.explanation,
    consecutiveCorrect: err?.consecutiveCorrect ?? 0,
    need: RESOLVE_AFTER,
    isResolved: err?.isResolved ?? false,
  });
}
