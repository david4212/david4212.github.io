import prisma from "@/lib/prisma";
import { LEVELS } from "@/lib/levels";

export type TopicStat = { latest: number; best: number; attempts: number };
export type LevelStats = Record<number, TopicStat | undefined>;

// Статистика тестів ТЕМИ по рівнях 1-3 (практика по підрозділах сюди не входить)
export async function getLevelStats(userId: string | undefined, topicIds: string[]) {
  const map = new Map<string, LevelStats>();
  if (!userId || topicIds.length === 0) return map;

  const results = await prisma.testResult.findMany({
    where: { userId, topicId: { in: topicIds }, subtopicId: null, testLevel: { in: [1, 2, 3] } },
    orderBy: { createdAt: "desc" },
    select: { topicId: true, testLevel: true, percent: true },
  });

  for (const r of results) {
    const levels = map.get(r.topicId) ?? {};
    const s = levels[r.testLevel];
    if (!s) levels[r.testLevel] = { latest: r.percent, best: r.percent, attempts: 1 };
    else {
      s.best = Math.max(s.best, r.percent);
      s.attempts += 1;
    }
    map.set(r.topicId, levels);
  }
  return map;
}

export function isPassed(stats: LevelStats | undefined, level: number): boolean {
  const s = stats?.[level];
  const lvl = LEVELS.find((l) => l.level === level);
  return !!s && !!lvl && s.best >= lvl.pass;
}

export function passedCount(stats: LevelStats | undefined): number {
  return LEVELS.filter((l) => isPassed(stats, l.level)).length;
}

// Рівень відкритий, якщо попередній складено (для рівня 1 — завжди)
export function isUnlocked(stats: LevelStats | undefined, level: number): boolean {
  return level <= 1 || isPassed(stats, level - 1);
}

// Статистика практики по підрозділах
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
