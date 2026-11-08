import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import prisma from "@/lib/prisma";

export const dynamic = "force-dynamic";
import FlashcardViewer from "@/components/cards/FlashcardViewer";

export default async function TopicPage({ params }: { params: { subject: string, topicId: string } }) {
  // Дістаємо тему і всі її картки з бази даних
  const topic = await prisma.topic.findUnique({
    where: { id: params.topicId },
    include: { flashcards: true, _count: { select: { questions: true } } }
  });

  if (!topic) {
    return <div className="p-10 text-center text-2xl font-bold">Тему не знайдено</div>;
  }

  return (
    <main className="container mx-auto px-4 py-8 max-w-3xl min-h-screen flex flex-col">
      <Link href={`/subjects/${params.subject}`} className="inline-flex items-center text-gray-500 hover:text-gray-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> До списку тем
      </Link>
      
      <h1 className="text-2xl font-bold text-gray-900 mb-2">{topic.title}</h1>
      {topic._count.questions > 0 && (
        <Link href={`/subjects/${params.subject}/topic/${topic.id}/test`} className="inline-block self-start px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-800 transition">
          Пройти тест ({topic._count.questions})
        </Link>
      )}
      
      {/* Клієнтський компонент з картками */}
      <FlashcardViewer cards={topic.flashcards} />
    </main>
  );
}
