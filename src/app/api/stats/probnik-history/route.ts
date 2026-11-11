import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getUserId } from "@/lib/session-user";

export const dynamic = "force-dynamic";

// GET — повертає список завершених пробників для профілю
export async function GET() {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const sessions = await prisma.testSession.findMany({
    where: { userId, kind: "SIMULATION", status: "FINISHED" },
    orderBy: { finishedAt: "desc" },
    take: 50,
    select: {
      id: true,
      difficulty: true,
      correct: true,
      total: true,
      percent: true,
      nmtScore: true,
      subjectScores: true,
      startedAt: true,
      finishedAt: true,
    },
  });

  return NextResponse.json({
    sessions: sessions.map((s) => ({
      id: s.id,
      difficulty: s.difficulty,
      correct: s.correct,
      total: s.total,
      percent: s.percent,
      nmtScore: s.nmtScore,
      subjectScores: s.subjectScores,
      startedAt: s.startedAt,
      finishedAt: s.finishedAt,
      durationMin: s.startedAt && s.finishedAt ? Math.round((s.finishedAt.getTime() - s.startedAt.getTime()) / 60_000) : null,
    })),
  });
}
