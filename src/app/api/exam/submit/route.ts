import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { mockScore } from "@/lib/score";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  const examId = typeof body?.examId === "string" ? body.examId : "";
  const answers: Record<string, number> = body?.answers && typeof body.answers === "object" ? body.answers : {};
  if (!examId) return NextResponse.json({ error: "Немає examId" }, { status: 400 });

  const exam = await prisma.weeklyExam.findUnique({
    where: { id: examId },
    include: { questions: { select: { id: true, correctIndex: true } } },
  });
  const now = new Date();
  if (!exam || !exam.isActive || exam.startTime > now || exam.endTime < now) {
    return NextResponse.json({ error: "Пробне НМТ зараз недоступне" }, { status: 403 });
  }
  if (exam.questions.length === 0) return NextResponse.json({ error: "У пробному немає питань" }, { status: 404 });

  const details = exam.questions.map((q) => {
    const chosen = typeof answers[q.id] === "number" ? answers[q.id] : null;
    return { id: q.id, correctIndex: q.correctIndex, chosen };
  });
  const correct = details.filter((d) => d.chosen === d.correctIndex).length;
  const total = exam.questions.length;
  const percent = Math.round((correct / total) * 100);
  const score = mockScore(percent);

  let saved = false;
  let bestScore = score;
  const session = await getServerSession(authOptions);
  if (session?.user?.id) {
    try {
      await prisma.examAttempt.create({ data: { examId, userId: session.user.id, correct, total, percent, score } });
      saved = true;
      const best = await prisma.examAttempt.aggregate({ where: { examId, userId: session.user.id }, _max: { score: true } });
      bestScore = best._max.score ?? score;
    } catch (e) {
      console.error("Не вдалось зберегти спробу:", e);
    }
  }

  return NextResponse.json({ correct, total, percent, saved, details, score, bestScore });
}
