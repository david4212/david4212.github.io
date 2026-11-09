import prisma from "@/lib/prisma";
import { kyivDate, prevDate } from "@/lib/kyiv";

// Викликається при будь-якій активності (відповідь на питання). Повертає актуальну серію.
export async function touchStreak(userId: string) {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { currentStreak: true, longestStreak: true, lastActiveDate: true },
  });
  if (!user) return null;

  const today = kyivDate();
  if (user.lastActiveDate === today) return user;

  const current = user.lastActiveDate === prevDate(today) ? user.currentStreak + 1 : 1;
  const longest = Math.max(user.longestStreak, current);
  await prisma.user.update({
    where: { id: userId },
    data: { currentStreak: current, longestStreak: longest, lastActiveDate: today },
  });
  return { currentStreak: current, longestStreak: longest, lastActiveDate: today };
}

// Для показу: якщо пропущено більше ніж вчора — серія вже обнулена
export function effectiveStreak(u: { currentStreak: number; lastActiveDate: string | null }) {
  const today = kyivDate();
  return u.lastActiveDate === today || u.lastActiveDate === prevDate(today) ? u.currentStreak : 0;
}
