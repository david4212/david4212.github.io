import prisma from "@/lib/prisma";

export type TopicStat = { latest: number; best: number; attempts: number };

// Статистика тестів користувача по темах (остання спроба, найкраща, кількість спроб)
export async function getTopicStats(userId: string | undefined, topicIds: string[]) {
  const map = new Map<string, TopicStat>();
  if (!userId || topicIds.length === 0) return map;

  const results = await prisma.testResult.findMany({
    where: { userId, topicId: { in: topicIds }, subtopicId: null },
    orderBy: { createdAt: "desc" },
    select: { topicId: true, percent: true },
  });

  for (const r of results) {
    const s = map.get(r.topicId);
    if (!s) map.set(r.topicId, { latest: r.percent, best: r.percent, attempts: 1 });
    else {
      s.best = Math.max(s.best, r.percent);
      s.attempts += 1;
    }
  }
  return map;
}

// Статистика тестів по підрозділах
export async function getSubtopicStats(userId: string | undefined, subtopicIds: string[]) {
  const map = new Map<string, TopicStat>();
  if (!userId || subtopicIds.length === 0) return map;

  const results = await prisma.testResult.findMany({
    where: { userId, subtopicId: { in: subtopicIds } },
    orderBy: { createdAt: "desc" },
    select: { subtopicId: true, percent: true },
  });

  for (const r of results) {
    if (!r.subtopicId) continue;
    const s = map.get(r.subtopicId);
    if (!s) map.set(r.subtopicId, { latest: r.percent, best: r.percent, attempts: 1 });
    else {
      s.best = Math.max(s.best, r.percent);
      s.attempts += 1;
    }
  }
  return map;
}

export function percentBadge(p: number): string {
  if (p >= 80) return "bg-green-100 text-green-700";
  if (p >= 50) return "bg-yellow-100 text-yellow-700";
  return "bg-red-100 text-red-700";
}
