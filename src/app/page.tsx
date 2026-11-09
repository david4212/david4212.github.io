import Link from "next/link";
import { Flame, Trophy } from "lucide-react";
import { getServerSession } from "next-auth";
import CountdownTimer from "@/components/shared/CountdownTimer";
import ExamCountdown from "@/components/shared/ExamCountdown";
import SubjectIcon from "@/components/shared/SubjectIcon";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { getLevelStats, passedCount } from "@/lib/progress";
import { SUBJECT_DETAILS, SUBJECT_ORDER } from "@/types";

export const dynamic = "force-dynamic";

type ExamInfo = { id: string; title: string; endTime: string; questionCount: number };

export default async function Home() {
  // Прогрес предмета = скільки рівнів тестів (з 3 у кожній темі) складено
  const progress: Record<string, { passed: number; total: number }> = {};
  let exam: ExamInfo | null = null;
  let bestScore: number | null = null;

  try {
    const session = await getServerSession(authOptions);
    const userId = session?.user?.id;

    const topics = await prisma.topic.findMany({ select: { id: true, subject: true } });
    const stats = await getLevelStats(userId, topics.map((t) => t.id));
    for (const sub of SUBJECT_ORDER) {
      const own = topics.filter((t) => t.subject === sub);
      progress[sub] = {
        total: own.length * 3,
        passed: own.reduce((acc, t) => acc + passedCount(stats.get(t.id)), 0),
      };
    }

    const now = new Date();
    const active = await prisma.weeklyExam.findFirst({
      where: { isActive: true, startTime: { lte: now }, endTime: { gt: now } },
      orderBy: { startTime: "desc" },
      include: { _count: { select: { questions: true } } },
    });
    if (active) {
      exam = { id: active.id, title: active.title, endTime: active.endTime.toISOString(), questionCount: active._count.questions };
      if (userId) {
        const best = await prisma.examAttempt.aggregate({ where: { examId: active.id, userId }, _max: { score: true } });
        bestScore = best._max.score ?? null;
      }
    }
  } catch (e) {
    console.error("Не вдалось завантажити дані головної:", e);
  }

  return (
    <main className="container mx-auto px-4 py-6 max-w-5xl">
      <header className="text-center mb-8">
        <h1 className="text-4xl md:text-6xl font-extrabold text-slate-900 mb-3 tracking-tight">
          НМТ на <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-pink-500">200</span>
        </h1>
        <p className="text-lg text-slate-600">Відслідковуй прогрес, вчи флеш-картки та досягай мети</p>
      </header>

      <section className="mb-8">
        <CountdownTimer />
      </section>

      {exam && (
        <section className="mb-10">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-amber-500 to-rose-500 p-6 md:p-8 text-white shadow-xl">
            <div className="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-white/15" />
            <div className="relative flex flex-col md:flex-row md:items-center md:justify-between gap-5">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-sm font-bold mb-3">
                  <Flame className="w-4 h-4" /> Пробне НМТ цього тижня
                </div>
                <h2 className="text-2xl md:text-3xl font-extrabold mb-3 drop-shadow">{exam.title}</h2>
                <div className="flex flex-wrap gap-3 text-sm">
                  <span className="px-3 py-1 rounded-xl bg-white/20 backdrop-blur-md">Питань: {exam.questionCount}</span>
                  <span className="px-3 py-1 rounded-xl bg-white/20 backdrop-blur-md">
                    До кінця: <ExamCountdown endTime={exam.endTime} />
                  </span>
                  {bestScore !== null && (
                    <span className="px-3 py-1 rounded-xl bg-white/30 backdrop-blur-md inline-flex items-center gap-1 font-bold">
                      <Trophy className="w-4 h-4" /> Твій найкращий бал: {bestScore}
                    </span>
                  )}
                </div>
              </div>
              {exam.questionCount > 0 && (
                <Link href={`/exam/${exam.id}`} className="shrink-0 text-center px-7 py-3 rounded-2xl bg-white text-rose-600 font-extrabold shadow-lg hover:scale-105 transition-transform">
                  Скласти іспит
                </Link>
              )}
            </div>
          </div>
        </section>
      )}

      <section>
        <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">Твої предмети</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {SUBJECT_ORDER.map((id) => {
            const theme = SUBJECT_DETAILS[id];
            const pr = progress[id] ?? { passed: 0, total: 0 };
            const pct = pr.total ? Math.round((pr.passed / pr.total) * 100) : 0;
            return (
              <Link href={`/subjects/${id.toLowerCase()}`} key={id}>
                <div className={`relative overflow-hidden p-6 rounded-3xl bg-gradient-to-br ${theme.gradient} text-white shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 cursor-pointer`}>
                  <div className={`absolute -top-6 -right-6 w-32 h-32 rounded-full ${theme.soft}`} />
                  <div className="absolute top-5 right-5 p-3 rounded-2xl bg-white/20 backdrop-blur-md">
                    <SubjectIcon subject={id} className="w-8 h-8 text-white" />
                  </div>

                  <h3 className="relative text-2xl font-extrabold mb-1 pr-20">{theme.title}</h3>
                  <p className="relative text-white/80 text-sm">Тести, картки, підрозділи</p>

                  <div className="relative mt-8">
                    <div className="flex justify-between text-sm mb-2 text-white/90">
                      <span>Складено рівнів: {pr.passed} з {pr.total}</span>
                      <span className="font-bold">{pct}%</span>
                    </div>
                    <div className="w-full bg-white/25 rounded-full h-3 overflow-hidden">
                      <div className="h-3 rounded-full bg-white transition-all duration-1000" style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </main>
  );
}
