import Link from "next/link";
import { ArrowLeft, BookOpen, ListChecks } from "lucide-react";
import { getServerSession } from "next-auth";
import { SUBJECT_DETAILS, Subject } from "@/types";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { getTopicStats, percentBadge } from "@/lib/progress";

export const dynamic = "force-dynamic";

export default async function SubjectPage({ params }: { params: { subject: string } }) {
  const subjectKey = params.subject.toUpperCase() as Subject;
  const subjectInfo = SUBJECT_DETAILS[subjectKey];

  if (!subjectInfo) {
    return <div className="p-10 text-center text-2xl font-bold">Предмет не знайдено</div>;
  }

  const session = await getServerSession(authOptions);
  const topics = await prisma.topic.findMany({
    where: { subject: subjectKey },
    orderBy: { order: "asc" },
    include: { _count: { select: { flashcards: true, questions: true } } },
  });
  const stats = await getTopicStats(session?.user?.id, topics.map((t) => t.id));

  return (
    <main className="container mx-auto px-4 py-8 max-w-4xl">
      <Link href="/" className="inline-flex items-center text-gray-500 hover:text-gray-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>

      <div className="flex items-center gap-4 mb-4">
        <div className={`w-4 h-12 rounded-full ${subjectInfo.bgClass}`}></div>
        <h1 className="text-4xl font-extrabold text-gray-900">{subjectInfo.title}</h1>
      </div>
      {!session?.user && (
        <p className="text-sm text-gray-500 mb-6">
          <Link href="/login" className="text-blue-600 underline">Увійди</Link>, щоб бачити свій відсоток по темах.
        </p>
      )}

      {topics.length === 0 ? (
        <div className="text-center p-10 mt-6 bg-white rounded-2xl border border-gray-100 shadow-sm">
          <p className="text-gray-500">Тем поки немає. Додай їх через Telegram-бота (/addtest).</p>
        </div>
      ) : (
        <div className="space-y-4 mt-6">
          {topics.map((topic, index) => {
            const stat = stats.get(topic.id);
            return (
              <div key={topic.id} className="p-5 rounded-2xl bg-white border border-gray-100 shadow-soft hover:shadow-md transition-shadow flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="flex items-start gap-4">
                  <span className="text-2xl font-bold text-gray-300">{(index + 1).toString().padStart(2, "0")}</span>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">{topic.title}</h3>
                    <div className="flex flex-wrap items-center text-sm text-gray-500 mt-1 gap-x-4 gap-y-1">
                      <span className="inline-flex items-center gap-1"><ListChecks className="w-4 h-4" />{topic._count.questions} питань</span>
                      <span className="inline-flex items-center gap-1"><BookOpen className="w-4 h-4" />{topic._count.flashcards} карток</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                  {stat ? (
                    <span title={`Найкращий: ${stat.best}%, спроб: ${stat.attempts}`} className={`px-3 py-1 rounded-full text-xs font-bold ${percentBadge(stat.latest)}`}>
                      {stat.latest}%
                    </span>
                  ) : (
                    <span className="px-3 py-1 bg-gray-200 text-gray-600 rounded-full text-xs font-bold uppercase">Не пройдено</span>
                  )}

                  <div className="flex gap-2">
                    {topic._count.flashcards > 0 && (
                      <Link href={`/subjects/${params.subject}/topic/${topic.id}`} className="px-4 py-2 bg-white border border-gray-200 text-gray-800 rounded-lg text-sm font-semibold hover:bg-gray-50 transition">
                        Картки
                      </Link>
                    )}
                    {topic._count.questions > 0 && (
                      <Link href={`/subjects/${params.subject}/topic/${topic.id}/test`} className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-800 transition">
                        Тест
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </main>
  );
}
