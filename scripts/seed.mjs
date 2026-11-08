// Додає/оновлює офіційні теми НМТ. Безпечно запускати скільки завгодно разів:
// нічого з питань, карток і результатів не видаляє.
import { readFileSync } from "node:fs";

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
} catch (e) {
  console.log("[seed] не вдалось (збірку не зупиняю):", e.message);
} finally {
  await prisma?.$disconnect();
}
