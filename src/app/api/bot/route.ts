import { NextResponse } from "next/server";
import type { Subject } from "@prisma/client";
import prisma from "@/lib/prisma";
import { SUBJECT_DETAILS } from "@/types";
import { parseCards, parseQuestions } from "@/lib/parsers";
import { answerCallback, sendMessage, type InlineKeyboard } from "@/lib/telegram";

export const dynamic = "force-dynamic";

type TgUpdate = {
  message?: { text?: string; chat: { id: number }; from?: { id: number } };
  callback_query?: {
    id: string;
    data?: string;
    from: { id: number };
    message?: { chat: { id: number } };
  };
};

const SUBJECTS = Object.keys(SUBJECT_DETAILS) as Subject[];
const ok = () => NextResponse.json({ ok: true });

const HELP = `Адмінка НМТ на 200

/addtest — додати питання до тесту
(після вибору теми бот спитає: додати підрозділ чи без підрозділу)
/addcards — додати флеш-картки
/done — закінчити додавання
/cancel — скасувати

Формат питань (можна кілька підряд, 50 питань краще слати кількома повідомленнями):

Питання: В якому році хрестили Русь?
А: 988
Б: 1054
В: 1187
Г: 1240
Відповідь: А

Формат карток:

Термін: Хрещення Русі
Пояснення: 988 рік, князь Володимир Великий`;

export async function GET() {
  return NextResponse.json({ status: "bot webhook is alive" });
}

export async function POST(req: Request) {
  // 1. Секрет вебхука (якщо заданий) — відсікає запити не від Telegram
  const secret = process.env.TELEGRAM_WEBHOOK_SECRET;
  if (secret && req.headers.get("x-telegram-bot-api-secret-token") !== secret) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }

  let update: TgUpdate;
  try {
    update = await req.json();
  } catch {
    return ok();
  }

  // 2. Тільки адмін: будь-хто інший ігнорується мовчки
  const adminId = String(process.env.TELEGRAM_ADMIN_ID ?? "").trim();
  const fromId = String(update.message?.from?.id ?? update.callback_query?.from?.id ?? "");
  if (!adminId || fromId !== adminId) return ok();

  const chatId = update.message?.chat.id ?? update.callback_query?.message?.chat.id;
  if (!chatId) return ok();

  try {
    if (update.callback_query) {
      await answerCallback(update.callback_query.id);
      await handleCallback(chatId, update.callback_query.data ?? "");
    } else if (update.message?.text) {
      await handleText(chatId, update.message.text.trim());
    }
  } catch (error) {
    console.error("Bot error:", error);
    await sendMessage(chatId, "Сталась помилка на сервері. Спробуй ще раз або напиши /cancel.");
  }
  return ok();
}

async function startFlow(chatId: number, mode: "TEST" | "CARDS") {
  await prisma.botSession.upsert({
    where: { chatId: String(chatId) },
    create: { chatId: String(chatId), mode, step: "SUBJECT" },
    update: { mode, step: "SUBJECT", subject: null, topicId: null, subtopicId: null },
  });
  const keyboard: InlineKeyboard = SUBJECTS.map((s) => [
    { text: SUBJECT_DETAILS[s].title, callback_data: `s:${s}` },
  ]);
  await sendMessage(chatId, mode === "TEST" ? "Додаємо питання. Обери предмет:" : "Додаємо картки. Обери предмет:", keyboard);
}

async function handleCallback(chatId: number, data: string) {
  const session = await prisma.botSession.findUnique({ where: { chatId: String(chatId) } });
  if (!session) return void (await sendMessage(chatId, "Почни з /addtest або /addcards."));

  if (data.startsWith("s:")) {
    const subject = data.slice(2) as Subject;
    if (!SUBJECTS.includes(subject)) return;
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { subject, step: "TOPIC", topicId: null, subtopicId: null } });
    const topics = await prisma.topic.findMany({ where: { subject }, orderBy: { order: "asc" } });
    const keyboard: InlineKeyboard = topics.map((t) => [
      { text: `${t.order}. ${t.title}`.slice(0, 60), callback_data: `t:${t.id}` },
    ]);
    keyboard.push([{ text: "➕ Нова тема", callback_data: "new" }]);
    await sendMessage(chatId, `${SUBJECT_DETAILS[subject].title}. Обери тему або створи нову:`, keyboard);
    return;
  }

  if (data === "new") {
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { step: "NEW_TOPIC" } });
    await sendMessage(chatId, "Напиши назву нової теми одним повідомленням:");
    return;
  }

  if (data.startsWith("t:")) {
    const topic = await prisma.topic.findUnique({ where: { id: data.slice(2) } });
    if (!topic) return void (await sendMessage(chatId, "Тему не знайдено, спробуй /addtest ще раз."));
    await askSubtopic(chatId, session.chatId, topic.id, topic.title);
    return;
  }

  if (data === "nosub") {
    const topic = session.topicId ? await prisma.topic.findUnique({ where: { id: session.topicId } }) : null;
    if (!topic) return void (await sendMessage(chatId, "Спочатку обери тему: /addtest"));
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { subtopicId: null, step: "CONTENT" } });
    await sendMessage(chatId, contentPrompt(session.mode, topic.title));
    return;
  }

  if (data === "newsub") {
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { step: "NEW_SUBTOPIC" } });
    await sendMessage(chatId, "Напиши назву нового підрозділу одним повідомленням:");
    return;
  }

  if (data.startsWith("u:")) {
    const sub = await prisma.subtopic.findUnique({ where: { id: data.slice(2) }, include: { topic: true } });
    if (!sub) return void (await sendMessage(chatId, "Підрозділ не знайдено, спробуй /addtest ще раз."));
    await prisma.botSession.update({
      where: { chatId: session.chatId },
      data: { topicId: sub.topicId, subtopicId: sub.id, step: "CONTENT" },
    });
    await sendMessage(chatId, contentPrompt(session.mode, sub.topic.title, sub.title));
  }
}

// Після вибору теми: додати підрозділ, обрати наявний чи працювати без підрозділу
async function askSubtopic(chatId: number, sessionId: string, topicId: string, topicTitle: string) {
  await prisma.botSession.update({ where: { chatId: sessionId }, data: { topicId, subtopicId: null, step: "SUBTOPIC" } });
  const subs = await prisma.subtopic.findMany({ where: { topicId }, orderBy: { order: "asc" } });
  const keyboard: InlineKeyboard = subs.map((u) => [{ text: `${u.order}. ${u.title}`.slice(0, 60), callback_data: `u:${u.id}` }]);
  keyboard.push([{ text: "➕ Додати підрозділ", callback_data: "newsub" }]);
  keyboard.push([{ text: "⏩ Без підрозділу", callback_data: "nosub" }]);
  await sendMessage(chatId, `Тема «${topicTitle}». Куди додаємо?`, keyboard);
}

function contentPrompt(mode: string, title: string, subTitle?: string) {
  const where = subTitle ? `Тема «${title}», підрозділ «${subTitle}».` : `Тема «${title}».`;
  return mode === "TEST"
    ? `${where} Надсилай питання у форматі:\n\nПитання: ...\nА: ...\nБ: ...\nВ: ...\nГ: ...\nВідповідь: А\n\nМожна кілька питань в одному повідомленні (до 4096 символів). Коли закінчиш — /done`
    : `${where} Надсилай картки у форматі:\n\nТермін: ...\nПояснення: ...\n\nМожна кілька карток в одному повідомленні. Коли закінчиш — /done`;
}

async function handleText(chatId: number, text: string) {
  const cmd = text.startsWith("/") ? text.split(/[\s@]/)[0].toLowerCase() : "";

  if (cmd === "/start" || cmd === "/help") return void (await sendMessage(chatId, HELP));
  if (cmd === "/addtest") return startFlow(chatId, "TEST");
  if (cmd === "/addcards") return startFlow(chatId, "CARDS");
  if (cmd === "/done" || cmd === "/cancel") {
    await prisma.botSession.deleteMany({ where: { chatId: String(chatId) } });
    return void (await sendMessage(chatId, cmd === "/done" ? "Готово! Контент вже на сайті." : "Скасовано."));
  }

  const session = await prisma.botSession.findUnique({ where: { chatId: String(chatId) } });
  if (!session) return void (await sendMessage(chatId, "Напиши /addtest або /addcards. Довідка: /help"));

  if (session.step === "NEW_TOPIC" && session.subject) {
    const last = await prisma.topic.findFirst({ where: { subject: session.subject }, orderBy: { order: "desc" } });
    const topic = await prisma.topic.create({
      data: { subject: session.subject, title: text.slice(0, 120), order: (last?.order ?? 0) + 1 },
    });
    await sendMessage(chatId, `Створив тему «${topic.title}».`);
    return askSubtopic(chatId, session.chatId, topic.id, topic.title);
  }

  if (session.step === "NEW_SUBTOPIC" && session.topicId) {
    const topic = await prisma.topic.findUnique({ where: { id: session.topicId } });
    if (!topic) return void (await sendMessage(chatId, "Тему не знайдено, спробуй /addtest ще раз."));
    const last = await prisma.subtopic.findFirst({ where: { topicId: topic.id }, orderBy: { order: "desc" } });
    const sub = await prisma.subtopic.create({
      data: { topicId: topic.id, title: text.slice(0, 120), order: (last?.order ?? 0) + 1 },
    });
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { subtopicId: sub.id, step: "CONTENT" } });
    return void (await sendMessage(chatId, `Створив підрозділ «${sub.title}».\n\n${contentPrompt(session.mode, topic.title, sub.title)}`));
  }

  if (session.step === "CONTENT" && session.topicId) {
    const topicId = session.topicId;
    const subtopicId = session.subtopicId;
    if (session.mode === "TEST") {
      const { items, errors } = parseQuestions(text);
      const existing = await prisma.question.findMany({ where: { topicId }, select: { text: true } });
      const known = new Set(existing.map((q) => q.text));
      const fresh = items.filter((q) => !known.has(q.text));
      if (fresh.length) {
        await prisma.question.createMany({ data: fresh.map((q) => ({ ...q, topicId, subtopicId })) });
      }
      const total = await prisma.question.count({ where: { topicId } });
      await sendMessage(chatId, report("питань", fresh.length, items.length - fresh.length, total, errors));
    } else {
      const { items, errors } = parseCards(text);
      const existing = await prisma.flashcard.findMany({ where: { topicId }, select: { question: true } });
      const known = new Set(existing.map((c) => c.question));
      const fresh = items.filter((c) => !known.has(c.question));
      if (fresh.length) {
        await prisma.flashcard.createMany({ data: fresh.map((c) => ({ ...c, topicId, subtopicId })) });
      }
      const total = await prisma.flashcard.count({ where: { topicId } });
      await sendMessage(chatId, report("карток", fresh.length, items.length - fresh.length, total, errors));
    }
    return;
  }

  await sendMessage(chatId, "Спочатку обери предмет і тему кнопками вище, або почни заново: /addtest");
}

function report(noun: string, added: number, dupes: number, total: number, errors: string[]) {
  let msg = `Додано ${noun}: ${added}.`;
  if (dupes) msg += ` Пропущено дублів: ${dupes}.`;
  msg += ` Усього в темі: ${total}.`;
  if (errors.length) msg += `\n\nНе вдалось прочитати:\n${errors.slice(0, 10).join("\n")}`;
  return msg;
}
