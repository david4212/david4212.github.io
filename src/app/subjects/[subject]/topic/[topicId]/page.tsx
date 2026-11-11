import Link from "next/link";
import { ArrowLeft, CheckCircle2, Lock, Star, XCircle } from "lucide-react";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { LEVELS } from "@/lib/levels";
import { getLevelStats, getSubtopicStats, isPassed, isUnlocked, percentBadge } from "@/lib/progress";
import FlashcardViewer from "@/components/cards/FlashcardViewer";
import { verifiedQuestionWhere } from "@/lib/history-review";

export const dynamic = "force-dynamic";

export default async function TopicPage({
  params,
  searchParams,
}: {
  params: { subject: string; topicId: string };
  searchParams: { sub?: string };
}) {
  const session = await getServerSession(authOptions);
  const userId = session?.user?.id;

  const topic = await prisma.topic.findUnique({
    where: { id: params.topicId },
    include: {
      subtopics: {
        orderBy: { order: "asc" },
        include: { _count: { select: { questions: true, flashcards: true } } },
      },
      flashcards: { orderBy: { createdAt: "asc" } },
    },
  });

  if (!topic) {
    return <div className="p-10 text-center text-2xl font-bold">Тему не знайдено</div>;
  }

  const perLevel = await prisma.question.groupBy({
    by: ["testLevel"],
    where: { topicId: topic.id, ...verifiedQuestionWhere },
    _count: { _all: true },
  });
  const countByLevel = new Map<number, number>(perLevel.map((r) => [r.testLevel, r._count._all] as [number, number]));

  const levelStats = (await getLevelStats(userId, [topic.id])).get(topic.id);
  const subStats = await getSubtopicStats(userId, topic.subtopics.map((u) => u.id));

  const selected = topic.subtopics.find((u) => u.id === searchParams.sub);
  const cards = selected ? topic.flashcards.filter((c) => c.subtopicId === selected.id) : topic.flashcards;
  const base = `/subjects/${params.subject}/topic/${topic.id}`;

  return (
    <main className="container mx-auto px-4 py-6 max-w-3xl min-h-screen flex flex-col">
      <Link href={`/subjects/${params.subject}`} className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-5">
        <ArrowLeft className="w-4 h-4 mr-2" /> До списку тем
      </Link>

      <h1 className="text-3xl font-extrabold text-slate-900 mb-6">{topic.title}</h1>

      {topic.subject === "HISTORY" && <p className="mb-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">Триває перевірка історичних карт. Непідтверджені візуальні завдання тимчасово не включені до тестів, щоб уникнути помилкових відповідей.</p>}

      {/* 3 тести теми */}
      <h2 className="text-lg font-bold text-slate-800 mb-3">Тести теми</h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-3">
        {LEVELS.map((l) => {
          const count = countByLevel.get(l.level) ?? 0;
          const stat = levelStats?.[l.level];
          const passed = isPassed(levelStats, l.level);
          const locked = !!userId && !isUnlocked(levelStats, l.level);
          const empty = count === 0;
          const disabled = locked || empty;

          return (
            <div
              key={l.level}
              className={`relative overflow-hidden rounded-3xl p-5 text-white shadow-xl bg-gradient-to-br ${disabled ? "from-slate-400 to-slate-500" : l.gradient}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="text-xs uppercase tracking-wider text-white/80">Тест {l.level}</p>
                  <p className="text-xl font-extrabold">{l.name}</p>
                </div>
                {locked ? <Lock className="w-5 h-5" /> : <Star className={`w-5 h-5 ${passed ? "fill-white" : ""}`} />}
              </div>

              <p className="text-sm text-white/90 mb-3">Поріг {l.pass}% · питань: {count}</p>

              <div className="w-full bg-white/25 rounded-full h-2 mb-3 overflow-hidden">
                <div className="h-2 rounded-full bg-white" style={{ width: `${stat?.best ?? 0}%` }} />
              </div>

              <p className="text-sm font-semibold mb-4 min-h-[1.25rem] inline-flex items-center gap-1">
                {empty ? (
                  "Питань ще немає"
                ) : locked ? (
                  `Заблоковано: склади Тест ${l.level - 1}`
                ) : stat ? (
                  passed ? (
                    <><CheckCircle2 className="w-4 h-4" /> Пройдено {stat.best}%</>
                  ) : (
                    <><XCircle className="w-4 h-4" /> Не складено ({stat.best}%)</>
                  )
                ) : (
                  "Не пройдено"
                )}
              </p>

              {disabled ? (
                <span className="block text-center px-4 py-2 rounded-xl bg-white/20 text-white/80 text-sm font-semibold cursor-not-allowed">
                  Недоступно
                </span>
              ) : (
                <Link href={`${base}/test?level=${l.level}`} className="block text-center px-4 py-2 rounded-xl bg-white text-slate-900 text-sm font-bold hover:scale-105 transition-transform">
                  {stat ? "Пройти ще раз" : "Почати"}
                </Link>
              )}
            </div>
          );
        })}
      </div>
      {!userId && (
        <p className="text-sm text-slate-500 mb-4">
          <Link href="/login" className="text-indigo-600 underline">Увійди</Link>, щоб результати зберігались, а рівні відкривались по черзі.
        </p>
      )}

      {/* Підрозділи */}
      {topic.subtopics.length > 0 && (
        <>
          <h2 className="text-lg font-bold text-slate-800 mt-6 mb-3">Підрозділи</h2>
          <div className="flex flex-wrap gap-2 mb-4">
            <Link
              href={base}
              className={`px-4 py-2 rounded-full text-sm font-semibold border transition ${
                !selected ? "bg-slate-900 text-white border-slate-900" : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
              }`}
            >
              Усі картки
            </Link>
            {topic.subtopics.map((u) => {
              const st = subStats.get(u.id);
              return (
                <Link
                  key={u.id}
                  href={`${base}?sub=${u.id}`}
                  className={`px-4 py-2 rounded-full text-sm font-semibold border transition inline-flex items-center gap-2 ${
                    selected?.id === u.id ? "bg-slate-900 text-white border-slate-900" : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  {u.title}
                  {st && <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${percentBadge(st.latest)}`}>{st.latest}%</span>}
                </Link>
              );
            })}
          </div>
          {selected && selected._count.questions > 0 && (
            <div className="mb-2">
              <Link href={`${base}/test?sub=${selected.id}`} className="inline-block px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 transition">
                Практика по підрозділу ({selected._count.questions} питань)
              </Link>
            </div>
          )}
        </>
      )}

      <h2 className="text-lg font-bold text-slate-800 mt-6">Флеш-картки</h2>
      <FlashcardViewer key={selected?.id ?? "all"} cards={cards} />
    </main>
  );
}
