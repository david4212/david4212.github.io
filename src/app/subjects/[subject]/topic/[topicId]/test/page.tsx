import Link from "next/link";
import { redirect } from "next/navigation";
import { ArrowLeft, Lock } from "lucide-react";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { getLevel } from "@/lib/levels";
import { getLevelStats, isUnlocked } from "@/lib/progress";
import TestRunner from "@/components/cards/TestRunner";
import { verifiedQuestionWhere } from "@/lib/history-review";

export const dynamic = "force-dynamic";

export default async function TestPage({
  params,
  searchParams,
}: {
  params: { subject: string; topicId: string };
  searchParams: { level?: string; sub?: string };
}) {
  const base = `/subjects/${params.subject}/topic/${params.topicId}`;
  const level = Number(searchParams.level);
  const lvl = getLevel(level);
  const subId = searchParams.sub;

  if (!lvl && !subId) redirect(base);

  const session = await getServerSession(authOptions);
  const userId = session?.user?.id;

  // correctIndex навмисно НЕ вибираємо — браузер не має знати правильні відповіді
  const topic = await prisma.topic.findUnique({
    where: { id: params.topicId },
    include: {
      subtopics: { select: { id: true, title: true } },
      questions: {
        where: { ...(subId ? { subtopicId: subId } : { testLevel: level }), ...verifiedQuestionWhere },
        select: { id: true, text: true, options: true, imageUrl: true },
        orderBy: { createdAt: "asc" },
      },
    },
  });

  if (!topic) {
    return <div className="p-10 text-center text-2xl font-bold">Тему не знайдено</div>;
  }

  const sub = topic.subtopics.find((u) => u.id === subId);

  // Рівень 2 і 3 відкриваються, коли складено попередній (для тих, хто увійшов)
  let locked = false;
  if (lvl && userId) {
    const stats = (await getLevelStats(userId, [topic.id])).get(topic.id);
    locked = !isUnlocked(stats, lvl.level);
  }

  const subtitle = sub ? `Практика: ${sub.title}` : `Тест ${lvl?.level} · ${lvl?.name} (поріг ${lvl?.pass}%)`;

  return (
    <main className="container mx-auto px-4 py-6 max-w-2xl min-h-screen">
      <Link href={base} className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> Назад до теми
      </Link>
      <h1 className="text-2xl font-extrabold text-slate-900">{topic.title}</h1>
      <p className="text-slate-500 text-sm mt-1">{subtitle}</p>

      {locked ? (
        <div className="text-center p-10 mt-8 bg-white rounded-3xl border border-slate-100 shadow-md">
          <Lock className="w-8 h-8 mx-auto text-slate-400 mb-3" />
          <p className="text-slate-600">Цей тест ще заблокований. Спочатку склади попередній рівень.</p>
        </div>
      ) : topic.questions.length === 0 ? (
        <div className="text-center p-10 mt-8 bg-white rounded-3xl border border-slate-100 shadow-md">
          <p className="text-slate-500">У цій темі немає перевірених питань. Частина старих картосхем тимчасово знята з тестування для фактчекінгу.</p>
        </div>
      ) : (
        <TestRunner
          key={`${level}-${subId ?? "all"}`}
          questions={topic.questions}
          submitUrl="/api/results"
          payload={sub ? { topicId: topic.id, subtopicId: sub.id } : { topicId: topic.id, level }}
          backHref={base}
          backLabel="До теми"
          loggedIn={!!userId}
        />
      )}
    </main>
  );
}
