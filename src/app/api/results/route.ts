import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";

export const dynamic = "force-dynamic";

// Приймає відповіді, рахує відсоток НА СЕРВЕРІ (правильні відповіді браузер не отримує наперед)
export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  const topicId = typeof body?.topicId === "string" ? body.topicId : "";
  const subtopicId = typeof body?.subtopicId === "string" && body.subtopicId ? body.subtopicId : null;
  const answers: Record<string, number> = body?.answers && typeof body.answers === "object" ? body.answers : {};

  if (!topicId) return NextResponse.json({ error: "Немає topicId" }, { status: 400 });

  const questions = await prisma.question.findMany({
    where: { topicId, ...(subtopicId ? { subtopicId } : {}) },
    select: { id: true, correctIndex: true },
  });
  if (questions.length === 0) return NextResponse.json({ error: "У темі немає питань" }, { status: 404 });

  const details = questions.map((q) => {
    const chosen = typeof answers[q.id] === "number" ? answers[q.id] : null;
    return { id: q.id, correctIndex: q.correctIndex, chosen };
  });
  const correct = details.filter((d) => d.chosen === d.correctIndex).length;
  const total = questions.length;
  const percent = Math.round((correct / total) * 100);

  let saved = false;
  const session = await getServerSession(authOptions);
  if (session?.user?.id) {
    try {
      await prisma.testResult.create({
        data: { userId: session.user.id, topicId, subtopicId, correct, total, percent },
      });
      saved = true;
    } catch (e) {
      console.error("Не вдалось зберегти результат:", e);
    }
  }

  return NextResponse.json({ correct, total, percent, saved, details });
}
