import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { getLevel } from "@/lib/levels";
import { recordAnswers } from "@/lib/answers";
import { randomUUID } from "crypto";

export const dynamic = "force-dynamic";

// Приймає відповіді, рахує відсоток НА СЕРВЕРІ (правильні відповіді браузер не отримує наперед)
// Тест теми: { topicId, level: 1|2|3 }; практика по підрозділу: { topicId, subtopicId }
export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  const topicId = typeof body?.topicId === "string" ? body.topicId : "";
  const subtopicId = typeof body?.subtopicId === "string" && body.subtopicId ? body.subtopicId : null;
  const level = subtopicId ? 0 : Number(body?.level);
  const answers: Record<string, number> = body?.answers && typeof body.answers === "object" ? body.answers : {};

  if (!topicId) return NextResponse.json({ error: "Немає topicId" }, { status: 400 });
  if (!subtopicId && !getLevel(level)) return NextResponse.json({ error: "Невірний рівень тесту" }, { status: 400 });

  const questions = await prisma.question.findMany({
    where: subtopicId ? { topicId, subtopicId } : { topicId, testLevel: level },
    select: { id: true, correctIndex: true, explanation: true },
  });
  if (questions.length === 0) return NextResponse.json({ error: "Немає питань" }, { status: 404 });

  const details = questions.map((q) => {
    const chosen = typeof answers[q.id] === "number" ? answers[q.id] : null;
    return { id: q.id, correctIndex: q.correctIndex, chosen, explanation: q.explanation };
  });
  const correct = details.filter((d) => d.chosen === d.correctIndex).length;
  const total = questions.length;
  const percent = Math.round((correct / total) * 100);

  const threshold = getLevel(level)?.pass;
  const passed = threshold !== undefined ? percent >= threshold : undefined;

  let saved = false;
  const session = await getServerSession(authOptions);
  if (session?.user?.id) {
    try {
      await prisma.testResult.create({
        data: { userId: session.user.id, topicId, subtopicId, testLevel: level, correct, total, percent },
      });
      saved = true;
      await recordAnswers(
        session.user.id,
        details.map((d) => ({ questionId: d.id, chosen: d.chosen, isCorrect: d.chosen === d.correctIndex })),
        "TEST",
        randomUUID()
      );
    } catch (e) {
      console.error("Не вдалось зберегти результат:", e);
    }
  }

  return NextResponse.json({ correct, total, percent, saved, details, threshold, passed });
}
