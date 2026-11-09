import { NextResponse } from "next/server";
import type { BotSession, Subject } from "@prisma/client";
import prisma from "@/lib/prisma";
import { SUBJECT_DETAILS } from "@/types";
import { LEVELS, getLevel } from "@/lib/levels";
import { parseCards, parseQuestions } from "@/lib/parsers";
import { answerCallback, sendMessage, type InlineKeyboard } from "@/lib/telegram";

export const dynamic = "force-dynamic";

type TgPhoto = { file_id: string };
type TgMessage = {
  text?: string;
  caption?: string;
  chat: { id: number };
  from?: { id: number };
  photo?: TgPhoto[];
  document?: { file_id: string; mime_type?: string };
};
type TgUpdate = {
  message?: TgMessage;
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

/addtest — питання до тестів теми (3 рівні: Тест 1, 2, 3)
/addcards — флеш-картки
/addexam — нове тижневе пробне НМТ
/closeexam — закрити активне пробне
/t1 /t2 /t3 — перемкнути рівень тесту під час додавання
/noexpl — питання без обґрунтування, /explain <код> <текст>
/done — закінчити, /cancel — скасувати

Питання:
Питання: В якому році хрестили Русь?
А: 988
Б: 1054
В: 1187
Г: 1240
Відповідь: А

Картки:
Термін: Хрещення Русі
Пояснення: 988 рік

Фото (для історії, геометрії):
• надішли картинку з підписом-питанням (підпис до 1024 символів), або
• надішли картинку окремо, а наступним повідомленням питання, або
• додай у блок рядок: Фото: https://посилання.png
Одне фото — на одне питання (якщо в повідомленні кілька питань, фото піде до першого).`;

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
    } else if (update.message) {
      await handleMessage(chatId, update.message);
    }
  } catch (error) {
    console.error("Bot error:", error);
    await sendMessage(chatId, "Сталась помилка на сервері. Спробуй ще раз або напиши /cancel.");
  }
  return ok();
}

/* ---------------------------- допоміжне ---------------------------- */

function findSession(chatId: number) {
  return prisma.botSession.findUnique({ where: { chatId: String(chatId) } });
}

async function startFlow(chatId: number, mode: "TEST" | "CARDS") {
  await prisma.botSession.upsert({
    where: { chatId: String(chatId) },
    create: { chatId: String(chatId), mode, step: "SUBJECT" },
    update: { mode, step: "SUBJECT", subject: null, topicId: null, subtopicId: null, examId: null, pendingImage: null, testLevel: 1 },
  });
  const keyboard: InlineKeyboard = SUBJECTS.map((s) => [
    { text: SUBJECT_DETAILS[s].title, callback_data: `s:${s}` },
  ]);
  await sendMessage(chatId, mode === "TEST" ? "Додаємо питання. Обери предмет:" : "Додаємо картки. Обери предмет:", keyboard);
}

const FORMAT_HINT_TEST = `Питання: ...\nА: ...\nБ: ...\nВ: ...\nГ: ...\nВідповідь: А\nОбґрунтування: ... (необов'язково)`;
const PHOTO_HINT = `Фото: лише зовнішнє посилання — рядок «Фото: https://...» у питанні`;

async function contentPrompt(session: BotSession): Promise<string> {
  if (session.mode === "EXAM") {
    const exam = session.examId ? await prisma.weeklyExam.findUnique({ where: { id: session.examId } }) : null;
    return `Пробне НМТ «${exam?.title ?? ""}». Надсилай питання:\n\n${FORMAT_HINT_TEST}\n\n${PHOTO_HINT}\n\nКоли закінчиш — /done`;
  }
  const topic = session.topicId ? await prisma.topic.findUnique({ where: { id: session.topicId } }) : null;
  const sub = session.subtopicId ? await prisma.subtopic.findUnique({ where: { id: session.subtopicId } }) : null;
  const where = sub ? `Тема «${topic?.title}», підрозділ «${sub.title}».` : `Тема «${topic?.title}».`;

  if (session.mode === "TEST") {
    const lvl = getLevel(session.testLevel);
    return `${where}\nДодаю в Тест ${session.testLevel}${lvl ? ` (${lvl.name}, поріг ${lvl.pass}%)` : ""}. Перемкнути: /t1 /t2 /t3\n\n${FORMAT_HINT_TEST}\n\n${PHOTO_HINT}\n\nМожна кілька питань в одному повідомленні. Коли закінчиш — /done`;
  }
  return `${where} Надсилай картки:\n\nТермін: ...\nПояснення: ...\n\n${PHOTO_HINT}\n\nКоли закінчиш — /done`;
}

// Після вибору теми/підрозділу: для тестів питаємо рівень, для карток одразу контент
async function afterPlacement(chatId: number, sessionId: string) {
  const session = await prisma.botSession.findUnique({ where: { chatId: sessionId } });
  if (!session) return;
  if (session.mode === "TEST") {
    await prisma.botSession.update({ where: { chatId: sessionId }, data: { step: "LEVEL" } });
    const keyboard: InlineKeyboard = LEVELS.map((l) => [
      { text: `Тест ${l.level} · ${l.name} (поріг ${l.pass}%)`, callback_data: `l:${l.level}` },
    ]);
    await sendMessage(chatId, "У який тест додаємо питання?", keyboard);
  } else {
    await prisma.botSession.update({ where: { chatId: sessionId }, data: { step: "CONTENT" } });
    await sendMessage(chatId, await contentPrompt(session));
  }
}

async function askSubtopic(chatId: number, sessionId: string, topicId: string, topicTitle: string) {
  await prisma.botSession.update({ where: { chatId: sessionId }, data: { topicId, subtopicId: null, step: "SUBTOPIC" } });
  const subs = await prisma.subtopic.findMany({ where: { topicId }, orderBy: { order: "asc" } });
  const keyboard: InlineKeyboard = subs.map((u) => [{ text: `${u.order}. ${u.title}`.slice(0, 60), callback_data: `u:${u.id}` }]);
  keyboard.push([{ text: "➕ Додати підрозділ", callback_data: "newsub" }]);
  keyboard.push([{ text: "⏩ Без підрозділу", callback_data: "nosub" }]);
  await sendMessage(chatId, `Тема «${topicTitle}». Куди додаємо?`, keyboard);
}

/* ---------------------------- кнопки ---------------------------- */

async function handleCallback(chatId: number, data: string) {
  const session = await findSession(chatId);
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
    if (!session.topicId) return void (await sendMessage(chatId, "Спочатку обери тему: /addtest"));
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { subtopicId: null } });
    return afterPlacement(chatId, session.chatId);
  }

  if (data === "newsub") {
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { step: "NEW_SUBTOPIC" } });
    await sendMessage(chatId, "Напиши назву нового підрозділу одним повідомленням:");
    return;
  }

  if (data.startsWith("u:")) {
    const sub = await prisma.subtopic.findUnique({ where: { id: data.slice(2) } });
    if (!sub) return void (await sendMessage(chatId, "Підрозділ не знайдено, спробуй /addtest ще раз."));
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { topicId: sub.topicId, subtopicId: sub.id } });
    return afterPlacement(chatId, session.chatId);
  }

  if (data.startsWith("l:")) {
    const level = Number(data.slice(2));
    if (!getLevel(level)) return;
    const updated = await prisma.botSession.update({ where: { chatId: session.chatId }, data: { testLevel: level, step: "CONTENT" } });
    await sendMessage(chatId, await contentPrompt(updated));
  }
}

/* ---------------------------- повідомлення ---------------------------- */

async function handleMessage(chatId: number, msg: TgMessage) {
  const text = (msg.text ?? msg.caption ?? "").trim();
  const photoId = msg.photo?.length
    ? msg.photo[msg.photo.length - 1].file_id
    : msg.document?.mime_type?.startsWith("image/")
      ? msg.document.file_id
      : null;

  if (!photoId) {
    if (text) await handleText(chatId, text, null);
    return;
  }

  const session = await findSession(chatId);
  if (!session || session.step !== "CONTENT") {
    return void (await sendMessage(chatId, "Фото отримав, але нікуди його не додаю. Спочатку /addtest, /addcards або /addexam і дійди до кроку з контентом."));
  }
  // Нові медіа зберігаємо лише як зовнішні URL (без BLOB/Base64 у БД)
  return void (await sendMessage(chatId, "Фото в базу не зберігаю. Завантаж картинку на хостинг (напр. imgbb/Cloudinary) і додай у питання рядок «Фото: https://...»."));
}

async function handleText(chatId: number, text: string, newImage: string | null) {
  const cmd = text.startsWith("/") ? text.split(/[\s@]/)[0].toLowerCase() : "";

  if (cmd === "/start" || cmd === "/help") return void (await sendMessage(chatId, HELP));
  if (cmd === "/addtest") return startFlow(chatId, "TEST");
  if (cmd === "/addcards") return startFlow(chatId, "CARDS");

  if (cmd === "/addexam") {
    await prisma.botSession.upsert({
      where: { chatId: String(chatId) },
      create: { chatId: String(chatId), mode: "EXAM", step: "EXAM_TITLE" },
      update: { mode: "EXAM", step: "EXAM_TITLE", subject: null, topicId: null, subtopicId: null, examId: null, pendingImage: null },
    });
    return void (await sendMessage(chatId, "Нове тижневе пробне НМТ. Напиши його назву (наприклад: Пробне НМТ, тиждень 12):"));
  }

  // /noexpl — питання без обґрунтування; /explain <id> <текст> — додати/змінити
  if (cmd === "/noexpl") {
    const [list, count] = await Promise.all([
      prisma.question.findMany({ where: { explanation: null }, orderBy: { createdAt: "asc" }, take: 10, select: { id: true, text: true } }),
      prisma.question.count({ where: { explanation: null } }),
    ]);
    if (!list.length) return void (await sendMessage(chatId, "У всіх питань є обґрунтування 🎉"));
    const lines = list.map((q) => `${q.id.slice(-6)} — ${q.text.slice(0, 60)}`).join("\n");
    return void (await sendMessage(chatId, `Без обґрунтування: ${count}. Перші ${list.length}:\n\n${lines}\n\nДодати: /explain <код> <текст>`));
  }

  if (cmd === "/explain") {
    const m = text.match(/^\/explain(?:@\w+)?\s+(\S+)\s+([\s\S]+)$/i);
    if (!m) return void (await sendMessage(chatId, "Формат: /explain <код> <текст обґрунтування>\nКоди: /noexpl"));
    const key = m[1];
    const found = await prisma.question.findMany({
      where: key.length >= 20 ? { id: key } : key.length >= 4 ? { id: { endsWith: key } } : { id: "-" },
      take: 2,
      select: { id: true, text: true },
    });
    if (found.length === 0) return void (await sendMessage(chatId, "Питання з таким кодом не знайдено. Коди: /noexpl"));
    if (found.length > 1) return void (await sendMessage(chatId, "Код неоднозначний, вкажи довший."));
    await prisma.question.update({ where: { id: found[0].id }, data: { explanation: m[2].trim().slice(0, 2000) } });
    return void (await sendMessage(chatId, `Обґрунтування збережено для: ${found[0].text.slice(0, 60)}`));
  }

  if (cmd === "/closeexam") {
    const closed = await prisma.weeklyExam.updateMany({ where: { isActive: true }, data: { isActive: false } });
    return void (await sendMessage(chatId, closed.count ? "Активне пробне закрито, з головної воно зникло." : "Активного пробного немає."));
  }

  if (cmd === "/done" || cmd === "/cancel") {
    await prisma.botSession.deleteMany({ where: { chatId: String(chatId) } });
    return void (await sendMessage(chatId, cmd === "/done" ? "Готово! Контент уже на сайті." : "Скасовано."));
  }

  const session = await findSession(chatId);

  if ((cmd === "/t1" || cmd === "/t2" || cmd === "/t3") && session?.mode === "TEST" && session.step === "CONTENT") {
    const level = Number(cmd.slice(2));
    const lvl = getLevel(level)!;
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { testLevel: level } });
    return void (await sendMessage(chatId, `Тепер додаю в Тест ${level} (${lvl.name}, поріг ${lvl.pass}%).`));
  }

  if (!session) return void (await sendMessage(chatId, "Напиши /addtest, /addcards або /addexam. Довідка: /help"));

  if (session.step === "EXAM_TITLE") {
    await prisma.weeklyExam.updateMany({ where: { isActive: true }, data: { isActive: false } });
    const endTime = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    const exam = await prisma.weeklyExam.create({ data: { title: text.slice(0, 120), isActive: true, endTime } });
    const updated = await prisma.botSession.update({ where: { chatId: session.chatId }, data: { examId: exam.id, step: "CONTENT" } });
    const until = endTime.toLocaleString("uk-UA", { timeZone: "Europe/Kyiv", dateStyle: "short", timeStyle: "short" });
    return void (await sendMessage(chatId, `Створив «${exam.title}», діє 7 днів (до ${until}). Попереднє пробне закрито.\n\n${await contentPrompt(updated)}`));
  }

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
    await prisma.botSession.update({ where: { chatId: session.chatId }, data: { subtopicId: sub.id } });
    await sendMessage(chatId, `Створив підрозділ «${sub.title}».`);
    return afterPlacement(chatId, session.chatId);
  }

  if (session.step === "CONTENT") return saveContent(chatId, session, text, newImage);

  await sendMessage(chatId, "Спочатку обери варіант кнопками вище, або почни заново: /addtest");
}

/* ---------------------------- збереження контенту ---------------------------- */

async function saveContent(chatId: number, session: BotSession, text: string, newImage: string | null) {
  const hasBlocks = /^\s*(?:Питання|Термін)\s*(?:№?\s*\d+)?\s*[:.)]/im.test(text);

  // Фото без питання/картки — запам'ятовуємо для наступного повідомлення
  if (!hasBlocks) {
    if (newImage) {
      await prisma.botSession.update({ where: { chatId: session.chatId }, data: { pendingImage: newImage } });
      return void (await sendMessage(chatId, "Фото збережено. Надішли питання (або картку), прикріплю його до першого блоку."));
    }
    return void (await sendMessage(chatId, "Не бачу «Питання:» чи «Термін:». Формат дивись у /help"));
  }

  const image = newImage ?? session.pendingImage;
  let usedImage = false;
  const attach = <T extends { imageUrl?: string }>(items: T[]) => {
    if (image && items.length > 0 && !items[0].imageUrl) {
      items[0].imageUrl = image;
      usedImage = true;
    }
  };

  if (session.mode === "CARDS" && session.topicId) {
    const topicId = session.topicId;
    const { items, errors } = parseCards(text);
    attach(items);
    const existing = await prisma.flashcard.findMany({ where: { topicId }, select: { question: true } });
    const known = new Set(existing.map((c) => c.question));
    const fresh = items.filter((c) => !known.has(c.question));
    if (fresh.length) await prisma.flashcard.createMany({ data: fresh.map((c) => ({ ...c, topicId, subtopicId: session.subtopicId })) });
    const total = await prisma.flashcard.count({ where: { topicId } });
    await finish(chatId, session, usedImage, report("карток", fresh.length, items.length - fresh.length, total, errors, fresh.filter((c) => c.imageUrl).length));
    return;
  }

  const { items, errors } = parseQuestions(text);
  attach(items);

  if (session.mode === "EXAM" && session.examId) {
    const examId = session.examId;
    const existing = await prisma.examQuestion.findMany({ where: { examId }, select: { text: true } });
    const known = new Set(existing.map((q) => q.text));
    const fresh = items.filter((q) => !known.has(q.text));
    if (fresh.length) await prisma.examQuestion.createMany({ data: fresh.map(({ explanation: _e, ...q }) => ({ ...q, examId })) });
    const total = await prisma.examQuestion.count({ where: { examId } });
    await finish(chatId, session, usedImage, report("питань", fresh.length, items.length - fresh.length, total, errors, fresh.filter((q) => q.imageUrl).length));
    return;
  }

  if (session.mode === "TEST" && session.topicId) {
    const topicId = session.topicId;
    const existing = await prisma.question.findMany({ where: { topicId }, select: { text: true } });
    const known = new Set(existing.map((q) => q.text));
    const fresh = items.filter((q) => !known.has(q.text));
    if (fresh.length) {
      await prisma.question.createMany({
        data: fresh.map((q) => ({ ...q, topicId, subtopicId: session.subtopicId, testLevel: session.testLevel })),
      });
    }
    const total = await prisma.question.count({ where: { topicId, testLevel: session.testLevel } });
    await finish(chatId, session, usedImage, report(`питань у Тесті ${session.testLevel}`, fresh.length, items.length - fresh.length, total, errors, fresh.filter((q) => q.imageUrl).length));
    return;
  }

  await sendMessage(chatId, "Щось пішло не так зі станом діалогу. Почни заново: /addtest");
}

async function finish(chatId: number, session: BotSession, usedImage: boolean, message: string) {
  if (usedImage) await prisma.botSession.update({ where: { chatId: session.chatId }, data: { pendingImage: null } });
  await sendMessage(chatId, message);
}

function report(noun: string, added: number, dupes: number, total: number, errors: string[], withPhoto: number) {
  let msg = `Додано ${noun}: ${added}.`;
  if (withPhoto) msg += ` З фото: ${withPhoto}.`;
  if (dupes) msg += ` Пропущено дублів: ${dupes}.`;
  msg += ` Усього: ${total}.`;
  if (errors.length) msg += `\n\nНе вдалось прочитати:\n${errors.slice(0, 10).join("\n")}`;
  return msg;
}
