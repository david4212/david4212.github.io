import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import TestRunner from "@/components/cards/TestRunner";

export const dynamic = "force-dynamic";

export default async function TestPage({ params }: { params: { subject: string; topicId: string } }) {
  const session = await getServerSession(authOptions);

  // correctIndex навмисно НЕ вибираємо — браузер не має знати правильні відповіді
  const topic = await prisma.topic.findUnique({
    where: { id: params.topicId },
    include: {
      questions: { select: { id: true, text: true, options: true }, orderBy: { createdAt: "asc" } },
    },
  });

  if (!topic) {
    return <div className="p-10 text-center text-2xl font-bold">Тему не знайдено</div>;
  }

  return (
    <main className="container mx-auto px-4 py-8 max-w-2xl min-h-screen">
      <Link href={`/subjects/${params.subject}`} className="inline-flex items-center text-gray-500 hover:text-gray-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> До списку тем
      </Link>
      <h1 className="text-2xl font-bold text-gray-900">{topic.title}</h1>
      <p className="text-gray-500 text-sm mt-1">Тест</p>

      {topic.questions.length === 0 ? (
        <div className="text-center p-10 mt-8 bg-white rounded-2xl border border-gray-100 shadow-sm">
          <p className="text-gray-500">У цій темі поки немає питань. Додай їх через Telegram-бота.</p>
        </div>
      ) : (
        <TestRunner topicId={topic.id} subject={params.subject} questions={topic.questions} loggedIn={!!session?.user?.id} />
      )}
    </main>
  );
}
