import { NextResponse } from "next/server";
import { getUserId } from "@/lib/session-user";
import { finishSession } from "@/lib/sessions";
import prisma from "@/lib/prisma";

export const dynamic = "force-dynamic";

// POST { id, answers? } — завершення; фінальні відповіді можна передати разом із запитом
export async function POST(req: Request) {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const id = typeof body?.id === "string" ? body.id : "";

  const s = await prisma.testSession.findFirst({ where: { id, userId } });
  if (!s) return NextResponse.json({ error: "Сесію не знайдено" }, { status: 404 });

  const late = !!s.deadlineAt && s.deadlineAt.getTime() + 30_000 < Date.now(); // 30 с запасу на мережу
  if (s.status === "IN_PROGRESS" && !late && body?.answers && typeof body.answers === "object") {
    const allowed = new Set(s.questionIds);
    const clean: Record<string, number> = {};
    for (const [k, v] of Object.entries(body.answers as Record<string, unknown>)) {
      if (allowed.has(k) && typeof v === "number" && Number.isInteger(v) && v >= 0 && v < 10) clean[k] = v;
    }
    await prisma.testSession.update({ where: { id: s.id }, data: { answers: clean } });
  }

  const result = await finishSession(id, userId);
  return NextResponse.json(result);
}
