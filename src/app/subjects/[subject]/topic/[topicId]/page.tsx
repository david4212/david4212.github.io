import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import { getSubtopicStats, percentBadge } from "@/lib/progress";
import FlashcardViewer from "@/components/cards/FlashcardViewer";

export const dynamic = "force-dynamic";

export default async function TopicPage({
  params,
  searchParams,
}: {
  params: { subject: string; topicId: string };
  searchParams: { sub?: string };
}) {
  const session = await getServerSession(authOptions);

  const topic = await prisma.topic.findUnique({
    where: { id: params.topicId },
    include: {
      subtopics: {
        orderBy: { order: "asc" },
        include: { _count: { select: { questions: true, flashcards: true } } },
      },
      flashcards: { orderBy: { createdAt: "asc" } },
      _count: { select: { questions: true } },
    },
  });

  if (!topic) {
    return <div className="p-10 text-center text-2xl font-bold">Тему не знайдено</div>;
  }

  const selected = topic.subtopics.find((u) => u.id === searchParams.sub);
  const cards = selected ? topic.flashcards.filter((c) => c.subtopicId === selected.id) : topic.flashcards;
  const stats = await getSubtopicStats(session?.user?.id, topic.subtopics.map((u) => u.id));

  const base = `/subjects/${params.subject}/topic/${topic.id}`;
  const questionCount = selected ? selected._count.questions : topic._count.questions;
  const testHref = selected ? `${base}/test?sub=${selected.id}` : `${base}/test`;

  return (
    <main className="container mx-auto px-4 py-8 max-w-3xl min-h-screen flex flex-col">
      <Link href={`/subjects/${params.subject}`} className="inline-flex items-center text-gray-500 hover:text-gray-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> До списку тем
      </Link>

      <h1 className="text-2xl font-bold text-gray-900 mb-4">{topic.title}</h1>

      {topic.subtopics.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          <Link
            href={base}
            className={`px-4 py-2 rounded-full text-sm font-semibold border transition ${
              !selected ? "bg-gray-900 text-white border-gray-900" : "bg-white text-gray-700 border-gray-200 hover:bg-gray-50"
            }`}
          >
            Уся тема
          </Link>
          {topic.subtopics.map((u) => {
            const st = stats.get(u.id);
            return (
              <Link
                key={u.id}
                href={`${base}?sub=${u.id}`}
                className={`px-4 py-2 rounded-full text-sm font-semibold border transition inline-flex items-center gap-2 ${
                  selected?.id === u.id ? "bg-gray-900 text-white border-gray-900" : "bg-white text-gray-700 border-gray-200 hover:bg-gray-50"
                }`}
              >
                {u.title}
                {st && <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${percentBadge(st.latest)}`}>{st.latest}%</span>}
              </Link>
            );
          })}
        </div>
      )}

      <div className="flex flex-wrap gap-3 mb-2">
        {questionCount > 0 ? (
          <Link href={testHref} className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-800 transition">
            {selected ? `Тест по підрозділу (${questionCount})` : `Тест по всій темі (${questionCount})`}
          </Link>
        ) : (
          <span className="text-sm text-gray-500">Питань тут поки немає.</span>
        )}
        {selected && topic._count.questions > 0 && (
          <Link href={`${base}/test`} className="px-4 py-2 bg-white border border-gray-200 text-gray-800 rounded-lg text-sm font-semibold hover:bg-gray-50 transition">
            Тест по всій темі ({topic._count.questions})
          </Link>
        )}
      </div>

      <FlashcardViewer key={selected?.id ?? "all"} cards={cards} />
    </main>
  );
}
