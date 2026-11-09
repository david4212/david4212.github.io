import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getUserId } from "@/lib/session-user";
import { buildQuestionIds, finishSession, KINDS, loadQuestions, type Kind } from "@/lib/sessions";

export const dynamic = "force-dynamic";

async function payload(s: { id: string; kind: string; questionIds: string[]; answers: unknown; currentIdx: number; startedAt: Date; deadlineAt: Date | null }) {
  return {
    id: s.id,
    kind: s.kind,
    startedAt: s.startedAt,
    deadlineAt: s.deadlineAt,
    currentIdx: s.currentIdx,
    answers: s.answers ?? {},
    questions: await loadQuestions(s.questionIds), // correctIndex клієнту не віддаємо
  };
}

// POST { kind: "DIAGNOSTIC" | "SIMULATION" } — стартує нову сесію або відновлює незавершену
export async function POST(req: Request) {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const kind = body?.kind as Kind;
  if (!(kind in KINDS)) return NextResponse.json({ error: "Невірний тип" }, { status: 400 });
  const fresh = body?.restart === true;

  const open = await prisma.testSession.findFirst({
    where: { userId, kind, status: "IN_PROGRESS" },
    orderBy: { startedAt: "desc" },
  });

  if (open) {
    const expired = open.deadlineAt && open.deadlineAt < new Date();
    if (expired || fresh) {
      await finishSession(open.id, userId); // зараховуємо те, що встиг, і закриваємо
    } else {
      return NextResponse.json({ resumed: true, ...(await payload(open)) });
    }
  }

  const questionIds = await buildQuestionIds(kind);
  if (questionIds.length === 0) return NextResponse.json({ error: "У базі немає питань" }, { status: 404 });

  const minutes = KINDS[kind].minutes;
  const s = await prisma.testSession.create({
    data: { userId, kind, questionIds, deadlineAt: minutes ? new Date(Date.now() + minutes * 60_000) : null },
  });
  return NextResponse.json({ resumed: false, ...(await payload(s)) });
}

// PATCH { id, answers: {questionId: index}, currentIdx } — збереження проміжного стану
export async function PATCH(req: Request) {
  const userId = await getUserId();
  if (!userId) return NextResponse.json({ error: "Потрібен вхід" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const id = typeof body?.id === "string" ? body.id : "";
  const s = await prisma.testSession.findFirst({ where: { id, userId } });
  if (!s) return NextResponse.json({ error: "Сесію не знайдено" }, { status: 404 });
  if (s.status !== "IN_PROGRESS") return NextResponse.json({ error: "Сесію завершено" }, { status: 409 });
  if (s.deadlineAt && s.deadlineAt < new Date()) return NextResponse.json({ error: "Час вийшов", expired: true }, { status: 409 });

  const allowed = new Set(s.questionIds);
  const clean: Record<string, number> = {};
  if (body?.answers && typeof body.answers === "object") {
    for (const [k, v] of Object.entries(body.answers as Record<string, unknown>)) {
      if (allowed.has(k) && typeof v === "number" && Number.isInteger(v) && v >= 0 && v < 10) clean[k] = v;
    }
  }
  const currentIdx = Math.min(Math.max(Number(body?.currentIdx) || 0, 0), s.questionIds.length - 1);

  await prisma.testSession.update({ where: { id: s.id }, data: { answers: clean, currentIdx } });
  return NextResponse.json({ ok: true });
}
