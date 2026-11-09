import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getDailyQuestionId } from "@/lib/daily";
import { sendMessage } from "@/lib/telegram";

export const dynamic = "force-dynamic";

const LETTERS = ["А", "Б", "В", "Г", "Д"];

// Vercel Cron (vercel.json): формує питання дня й шле його адміну в Telegram.
// Потрібен ENV CRON_SECRET — Vercel додає його як Authorization: Bearer.
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const qid = await getDailyQuestionId();
  if (!qid) return NextResponse.json({ ok: false, reason: "no questions" });

  const q = await prisma.question.findUnique({ where: { id: qid }, select: { text: true, options: true } });
  const adminId = process.env.TELEGRAM_ADMIN_ID;
  if (q && adminId) {
    const site = process.env.NEXTAUTH_URL ?? "https://david4212-github-io.vercel.app";
    const body = q.options.map((o, i) => `${LETTERS[i] ?? i + 1}) ${o}`).join("\n");
    await sendMessage(adminId, `🎯 Питання дня\n\n${q.text}\n\n${body}\n\nВідповідати: ${site}/`);
  }
  return NextResponse.json({ ok: true, questionId: qid });
}
