import Link from "next/link";
import { ArrowLeft, Trophy } from "lucide-react";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { getLevelStats, passedCount } from "@/lib/progress";
import ProfileWidgets from "@/components/profile/ProfileWidgets";
import { SUBJECT_DETAILS, SUBJECT_ORDER } from "@/types";

export const dynamic = "force-dynamic";

export default async function ProfilePage() {
  const session = await getServerSession(authOptions);
  const userId = session?.user?.id;

  if (!userId) {
    return (
      <main className="container mx-auto px-4 py-10 max-w-2xl text-center">
        <p className="text-slate-600 mb-4">Увійди, щоб побачити свій профіль.</p>
        <Link href="/login" className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold">Увійти</Link>
      </main>
    );
  }

  const [topics, attempts] = await Promise.all([
    prisma.topic.findMany({ select: { id: true, subject: true } }),
    prisma.examAttempt.findMany({
      where: { userId },
      orderBy: { createdAt: "desc" },
      include: { exam: { select: { title: true } } },
    }),
  ]);
  const stats = await getLevelStats(userId, topics.map((t) => t.id));

  // Краща спроба по кожному пробному
  const bestByExam = new Map<string, { title: string; best: number; tries: number }>();
  for (const a of attempts) {
    const cur = bestByExam.get(a.examId);
    if (!cur) bestByExam.set(a.examId, { title: a.exam.title, best: a.score, tries: 1 });
    else {
      cur.best = Math.max(cur.best, a.score);
      cur.tries += 1;
    }
  }

  return (
    <main className="container mx-auto px-4 py-6 max-w-3xl">
      <Link href="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-5">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>
      <h1 className="text-3xl font-extrabold text-slate-900 mb-6">Профіль: {session.user.name}</h1>

      <ProfileWidgets />

      <h2 className="text-lg font-bold text-slate-800 mb-3">Прогрес по предметах</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        {SUBJECT_ORDER.map((id) => {
          const theme = SUBJECT_DETAILS[id];
          const own = topics.filter((t) => t.subject === id);
          const total = own.length * 3;
          const passed = own.reduce((acc, t) => acc + passedCount(stats.get(t.id)), 0);
          const pct = total ? Math.round((passed / total) * 100) : 0;
          return (
            <div key={id} className={`rounded-3xl p-5 text-white shadow-xl bg-gradient-to-br ${theme.gradient}`}>
              <p className="font-bold">{theme.title}</p>
              <p className="text-sm text-white/80 mb-3">Складено рівнів: {passed} з {total}</p>
              <div className="w-full bg-white/25 rounded-full h-2 overflow-hidden">
                <div className="h-2 rounded-full bg-white" style={{ width: `${pct}%` }} />
              </div>
            </div>
          );
        })}
      </div>

      <h2 className="text-lg font-bold text-slate-800 mb-3">Пробні НМТ</h2>
      {bestByExam.size === 0 ? (
        <p className="text-slate-500">Ти ще не складав пробне НМТ.</p>
      ) : (
        <div className="space-y-3">
          {Array.from(bestByExam.values()).map((e, i) => (
            <div key={i} className="flex items-center justify-between p-4 rounded-2xl bg-white border border-slate-100 shadow-md">
              <div>
                <p className="font-semibold text-slate-800">{e.title}</p>
                <p className="text-sm text-slate-500">Спроб: {e.tries}</p>
              </div>
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-100 text-amber-700 font-extrabold">
                <Trophy className="w-4 h-4" /> {e.best}
              </span>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
