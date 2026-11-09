import Link from "next/link";
import { ArrowLeft, BookOpen, ListChecks, Star } from "lucide-react";
import { getServerSession } from "next-auth";
import { SUBJECT_DETAILS, Subject } from "@/types";
import SubjectIcon from "@/components/shared/SubjectIcon";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { LEVELS } from "@/lib/levels";
import { getLevelStats, isPassed } from "@/lib/progress";

export const dynamic = "force-dynamic";

export default async function SubjectPage({ params }: { params: { subject: string } }) {
  const subjectKey = params.subject.toUpperCase() as Subject;
  const theme = SUBJECT_DETAILS[subjectKey];

  if (!theme) {
    return <div className="p-10 text-center text-2xl font-bold">Предмет не знайдено</div>;
  }

  const session = await getServerSession(authOptions);
  const topics = await prisma.topic.findMany({
    where: { subject: subjectKey },
    orderBy: { order: "asc" },
    include: { _count: { select: { flashcards: true, questions: true, subtopics: true } } },
  });
  const stats = await getLevelStats(session?.user?.id, topics.map((t) => t.id));

  return (
    <main className="container mx-auto px-4 py-6 max-w-4xl">
      <Link href="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-5">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>

      <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${theme.gradient} p-6 md:p-8 text-white shadow-xl mb-4`}>
        <div className={`absolute -top-8 -right-8 w-40 h-40 rounded-full ${theme.soft}`} />
        <div className="relative flex items-center gap-4">
          <div className="p-3 rounded-2xl bg-white/20 backdrop-blur-md">
            <SubjectIcon subject={subjectKey} className="w-9 h-9 text-white" />
          </div>
          <div>
            <h1 className="text-3xl md:text-4xl font-extrabold drop-shadow">{theme.title}</h1>
            <p className="text-white/80 text-sm">Тем: {topics.length}</p>
          </div>
        </div>
      </div>

      {!session?.user && (
        <p className="text-sm text-slate-500 mb-4">
          <Link href="/login" className="text-indigo-600 underline">Увійди</Link>, щоб зберігався твій прогрес по рівнях.
        </p>
      )}

      {topics.length === 0 ? (
        <div className="text-center p-10 mt-6 bg-white rounded-2xl border border-slate-100 shadow-sm">
          <p className="text-slate-500">Тем поки немає. Додай їх через Telegram-бота (/addtest).</p>
        </div>
      ) : (
        <div className="space-y-4 mt-6">
          {topics.map((topic, index) => {
            const st = stats.get(topic.id);
            return (
              <Link
                key={topic.id}
                href={`/subjects/${params.subject}/topic/${topic.id}`}
                className="block p-5 rounded-3xl bg-white border border-slate-100 shadow-md hover:shadow-xl hover:scale-[1.01] transition-all duration-300"
              >
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div className="flex items-start gap-4">
                    <span className={`text-2xl font-extrabold ${theme.text}`}>{(index + 1).toString().padStart(2, "0")}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800">{topic.title}</h3>
                      <div className="flex flex-wrap items-center text-sm text-slate-500 mt-1 gap-x-4 gap-y-1">
                        <span className="inline-flex items-center gap-1"><ListChecks className="w-4 h-4" />{topic._count.questions} питань</span>
                        <span className="inline-flex items-center gap-1"><BookOpen className="w-4 h-4" />{topic._count.flashcards} карток</span>
                        {topic._count.subtopics > 0 && <span>{topic._count.subtopics} підрозділів</span>}
                      </div>
                    </div>
                  </div>

                  {/* 3 зірочки = 3 рівні тестів */}
                  <div className="flex items-center gap-2">
                    {LEVELS.map((l) => {
                      const s = st?.[l.level];
                      const passed = isPassed(st, l.level);
                      const cls = passed
                        ? "bg-green-100 text-green-700"
                        : s
                          ? "bg-red-100 text-red-700"
                          : "bg-slate-100 text-slate-400";
                      return (
                        <span key={l.level} title={`Тест ${l.level} · ${l.name}${s ? `: ${s.best}%` : ""}`} className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-bold ${cls}`}>
                          <Star className={`w-3.5 h-3.5 ${passed ? "fill-current" : ""}`} />
                          {s ? `${s.best}%` : l.level}
                        </span>
                      );
                    })}
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </main>
  );
}
