// Додає/оновлює офіційні теми НМТ. Безпечно запускати скільки завгодно разів:
// нічого з питань, карток і результатів не видаляє (крім технічних дублів питань нових типів).
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";
import { normalizeQuestion, questionKey, sameMeta } from "./normalize-question.mjs";

// Старі тестові теми з першої версії сайту — видаляємо лише якщо вони порожні
const OLD_PLACEHOLDERS = [
  "Фонетика. Графіка. Орфоепія", "Лексикологія. Фразеологія", "Будова слова. Словотвір",
  "Морфологія (Іменник, Прикметник)", "Числа і вирази", "Рівняння, нерівності та їх системи",
  "Функції", "Вступ до історії України", "Київська держава (Русь-Україна)",
  "Grammar: Tenses", "Vocabulary & Word Formation",
];

// Питання, вилучені з контенту через неоднозначність (замінено новими формулюваннями)
const RETIRED_QUESTIONS = [
  "У якому столітті було засновано Київ (згідно з літописною традицією)?",
  "Скільки мільйонів людей (мінімальна оцінка) загинуло під час Голодомору?",
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
  const retired = await prisma.question.deleteMany({ where: { text: { in: RETIRED_QUESTIONS } } });
  if (retired.count) console.log(`[content] вилучено застарілих питань: ${retired.count}`);
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

      const existingQ = await prisma.question.findMany({ where: { topicId: topic.id }, select: { id: true, text: true, options: true, explanation: true, imageUrl: true, questionType: true, metadata: true }, orderBy: { createdAt: "asc" } });
      // Прибираємо дублі нових типів, що з'явилися через старий ключ дубліката (баг до листопада 2026); лишаємо найстарішу копію
      const known = new Map();
      const dupIds = [];
      for (const q of existingQ) {
        const k = questionKey(q);
        if (known.has(k)) { if (q.questionType !== "single_choice") dupIds.push(q.id); continue; }
        known.set(k, q);
      }
      if (dupIds.length) {
        await prisma.question.deleteMany({ where: { id: { in: dupIds } } });
        console.log(`[content] ${data.topic}: видалено дублів нових типів: ${dupIds.length}`);
      }
      const VALID_TYPES = ["single_choice", "matching", "sequencing", "choose_multi", "fill_blanks", "short_answer"];
      const fresh = [];
      let filled = 0;
      for (const rawQ of data.questions ?? []) {
        const norm = normalizeQuestion(rawQ);
        if (norm.error) { console.log(`[content] пропущено (${norm.error}): ${String(rawQ.text ?? rawQ.question).slice(0, 40)}`); continue; }
        const q = norm.q;
        // Legacy 78 hand-drawn history illustrations are under factual review.
        // Do not reimport their 292 unverified questions until individually approved.
        if (data.subject === "HISTORY" && typeof q.image === "string" && q.image.startsWith("/img/history/")) continue;
        const qType = VALID_TYPES.includes(q.questionType) ? q.questionType : "single_choice";

        // Валідація залежно від типу питання
        let ok;
        if (qType === "single_choice") {
          ok = typeof q.text === "string" && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 5
            && Number.isInteger(q.correctIndex) && q.correctIndex >= 0 && q.correctIndex < q.options.length
            && typeof q.explanation === "string" && q.explanation.trim();
        } else if (qType === "short_answer") {
          ok = typeof q.text === "string" && q.metadata && (typeof q.metadata.answer === "number" || typeof q.metadata.answer === "string")
            && typeof q.explanation === "string" && q.explanation.trim();
        } else {
          // matching, sequencing, choose_multi, fill_blanks — потребують metadata + text + explanation
          ok = typeof q.text === "string" && q.metadata && typeof q.metadata === "object"
            && typeof q.explanation === "string" && q.explanation.trim();
        }

        if (!ok) { console.log(`[content] пропущено некоректне питання (${qType}): ${String(q.text).slice(0, 40)}`); continue; }
        const key = questionKey(q);
        if (known.has(key)) {
          const ex = known.get(key);
          if (!ex.id) continue; // дубль усередині контенту — уже додано
          const img = q.image ?? null;
          const metaChanged = qType !== "single_choice" && (!sameMeta(ex.metadata, q.metadata) || [...(ex.options ?? [])].join("|") !== [...(q.options ?? [])].join("|"));
          if (ex.explanation !== q.explanation || (ex.imageUrl ?? null) !== img || metaChanged) {
            await prisma.question.update({ where: { id: ex.id }, data: { options: q.options ?? [], correctIndex: q.correctIndex ?? 0, explanation: q.explanation, imageUrl: img, testLevel: [1, 2, 3].includes(q.testLevel) ? q.testLevel : 1, questionType: qType, metadata: q.metadata ?? null } });
            filled++;
          }
          continue;
        }
        known.set(key, { id: null, explanation: q.explanation, imageUrl: q.image ?? null, metadata: q.metadata, options: q.options });
        fresh.push({ text: q.text, options: q.options ?? [], correctIndex: q.correctIndex ?? 0, explanation: q.explanation, imageUrl: q.image ?? null, testLevel: [1, 2, 3].includes(q.testLevel) ? q.testLevel : 1, questionType: qType, metadata: q.metadata ?? null, topicId: topic.id, subtopicId });
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
