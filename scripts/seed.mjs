// Додає/оновлює офіційні теми НМТ. Безпечно запускати скільки завгодно разів:
// нічого з питань, карток і результатів не видаляє.
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";

// Старі тестові теми з першої версії сайту — видаляємо лише якщо вони порожні
const OLD_PLACEHOLDERS = [
  "Фонетика. Графіка. Орфоепія", "Лексикологія. Фразеологія", "Будова слова. Словотвір",
  "Морфологія (Іменник, Прикметник)", "Числа і вирази", "Рівняння, нерівності та їх системи",
  "Функції", "Вступ до історії України", "Київська держава (Русь-Україна)",
  "Grammar: Tenses", "Vocabulary & Word Formation",
];

let prisma;

try {
  // Динамічний імпорт з default: працює і в ESM, і з CJS-пакетом Prisma
  const prismaPkg = await import("@prisma/client");
  const { PrismaClient } = prismaPkg.default ?? prismaPkg;
  prisma = new PrismaClient();

  const curriculum = JSON.parse(readFileSync(new URL("../src/lib/curriculum.json", import.meta.url), "utf-8"));

  for (const [subject, titles] of Object.entries(curriculum)) {
    for (let i = 0; i < titles.length; i++) {
      const title = titles[i];
      const existing = await prisma.topic.findFirst({ where: { subject, title } });
      if (existing) {
        if (existing.order !== i + 1) await prisma.topic.update({ where: { id: existing.id }, data: { order: i + 1 } });
      } else {
        await prisma.topic.create({ data: { subject, title, order: i + 1 } });
      }
    }
  }

  const removed = await prisma.topic.deleteMany({
    where: {
      title: { in: OLD_PLACEHOLDERS },
      questions: { none: {} },
      flashcards: { none: {} },
      testResults: { none: {} },
    },
  });
  console.log(`[seed] теми НМТ оновлено, прибрано старих порожніх тем: ${removed.count}`);

  await importContent(prisma);
} catch (e) {
  console.log("[seed] не вдалось (збірку не зупиняю):", e.message);
} finally {
  await prisma?.$disconnect();
}


/* ---------- Імпорт контенту з content/ (json, ідемпотентно, нічого не видаляє) ---------- */
function listJson(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...listJson(full));
    else if (name.endsWith(".json")) out.push(full);
  }
  return out;
}

async function importContent(prisma) {
  const root = new URL("../content", import.meta.url).pathname;
  for (const file of listJson(root)) {
    try {
      const data = JSON.parse(readFileSync(file, "utf-8"));
      const topic = await prisma.topic.findFirst({ where: { subject: data.subject, title: data.topic } });
      if (!topic) { console.log(`[content] тему не знайдено: ${data.topic} (${file})`); continue; }

      let subtopicId = null;
      if (data.subtopic) {
        const sub = await prisma.subtopic.findFirst({ where: { topicId: topic.id, title: data.subtopic } });
        subtopicId = sub ? sub.id : (await prisma.subtopic.create({ data: { topicId: topic.id, title: data.subtopic, order: 99 } })).id;
      }

      const existingQ = await prisma.question.findMany({ where: { topicId: topic.id }, select: { text: true, explanation: true } });
      const known = new Map(existingQ.map((q) => [q.text, q.explanation]));
      const fresh = [];
      let filled = 0;
      for (const q of data.questions ?? []) {
        const ok = typeof q.text === "string" && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 5
          && Number.isInteger(q.correctIndex) && q.correctIndex >= 0 && q.correctIndex < q.options.length
          && typeof q.explanation === "string" && q.explanation.trim();
        if (!ok) { console.log(`[content] пропущено некоректне питання: ${String(q.text).slice(0, 40)}`); continue; }
        if (known.has(q.text)) {
          if (!known.get(q.text)) {
            await prisma.question.updateMany({ where: { topicId: topic.id, text: q.text, explanation: null }, data: { explanation: q.explanation } });
            filled++;
          }
          continue;
        }
        known.set(q.text, q.explanation);
        fresh.push({ text: q.text, options: q.options, correctIndex: q.correctIndex, explanation: q.explanation, testLevel: [1, 2, 3].includes(q.testLevel) ? q.testLevel : 1, topicId: topic.id, subtopicId });
      }
      if (fresh.length) await prisma.question.createMany({ data: fresh });

      const existingC = new Set((await prisma.flashcard.findMany({ where: { topicId: topic.id }, select: { question: true } })).map((c) => c.question));
      const cards = (data.cards ?? []).filter((c) => c.question && c.answer && !existingC.has(c.question)).map((c) => ({ question: c.question, answer: c.answer, topicId: topic.id, subtopicId }));
      if (cards.length) await prisma.flashcard.createMany({ data: cards });

      console.log(`[content] ${data.topic}: +${fresh.length} питань, +${cards.length} карток, доповнено обґрунтувань: ${filled}`);
    } catch (e) {
      console.log(`[content] помилка у ${file}:`, e.message);
    }
  }
}
