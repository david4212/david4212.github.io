import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { calculateNmtScore, averageNmt, mockScore } from "@/lib/score";
import { isUnverifiedHistoryQuestion } from "@/lib/history-review";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  const examId = typeof body?.examId === "string" ? body.examId : "";
  const answers: Record<string, number> = body?.answers && typeof body.answers === "object" ? body.answers : {};
  if (!examId) return NextResponse.json({ error: "Немає examId" }, { status: 400 });

  const exam = await prisma.weeklyExam.findUnique({
    where: { id: examId },
    include: { questions: { select: { id: true, correctIndex: true, subject: true, imageUrl: true } } },
  });
  const now = new Date();
  if (!exam || !exam.isActive || exam.startTime > now || exam.endTime < now) {
    return NextResponse.json({ error: "Пробне НМТ зараз недоступне" }, { status: 403 });
  }
  const safeQuestions = exam.questions.filter((q) => !isUnverifiedHistoryQuestion(q.imageUrl));
  if (safeQuestions.length === 0) return NextResponse.json({ error: "У пробному немає питань" }, { status: 404 });

  const details = safeQuestions.map((q) => {
    const chosen = typeof answers[q.id] === "number" ? answers[q.id] : null;
    return { id: q.id, correctIndex: q.correctIndex, chosen, subject: (q.subject as string | null) ?? null };
  });
  const correct = details.filter((d) => d.chosen === d.correctIndex).length;
  const total = safeQuestions.length;
  const percent = Math.round((correct / total) * 100);

  // Окремий розрахунок по кожному предмету за офіційною шкалою 100–200
  const bySubject = new Map<string, { correct: number; total: number }>();
  for (const d of details) {
    if (!d.subject) continue; // питання без предмета у розрахунок за шкалою не входять
    const e = bySubject.get(d.subject) ?? { correct: 0, total: 0 };
    e.total += 1;
    if (d.chosen === d.correctIndex) e.correct += 1;
    bySubject.set(d.subject, e);
  }
  const subjects = Array.from(bySubject, ([subject, v]) => ({ subject, correct: v.correct, total: v.total, ...calculateNmtScore(subject, v.correct, v.total) }));
  const tagged = subjects.length > 0; // чи є в пробному питання з указаним предметом
  const avg = tagged ? averageNmt(subjects) : null;
  const passed = tagged ? avg !== null : null;
  const score = tagged ? (avg ?? 0) : mockScore(percent); // 0 у БД = «Не склав»

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

  return NextResponse.json({
    correct, total, percent, saved,
    details: details.map(({ subject: _s, ...d }) => d),
    ...(tagged ? { score: avg, passed } : {}), subjects: subjects.map((x) => ({ subject: x.subject, correct: x.correct, total: x.total, nmtScore: x.nmtScore, isPassed: x.isPassed })),
    bestScore: bestScore > 0 ? bestScore : null,
  });
}
