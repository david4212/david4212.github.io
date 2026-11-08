import Link from "next/link";
import { ArrowLeft, BookOpen } from "lucide-react";
import { SUBJECT_DETAILS, Subject } from "@/types";
import prisma from "@/lib/prisma";

export const dynamic = "force-dynamic";

export default async function SubjectPage({ params }: { params: { subject: string } }) {
  const subjectKey = params.subject.toUpperCase() as Subject;
  const subjectInfo = SUBJECT_DETAILS[subjectKey];

  if (!subjectInfo) {
    return <div className="p-10 text-center text-2xl font-bold">Предмет не знайдено</div>;
  }

  // ТЯГНЕМО РЕАЛЬНІ ДАНІ З БАЗИ
  const topics = await prisma.topic.findMany({
    where: { subject: subjectKey },
    orderBy: { order: 'asc' },
    include: {
      _count: {
        select: { flashcards: true } // Одразу рахуємо кількість карток у темі
      }
    }
  });

  return (
    <main className="container mx-auto px-4 py-8 max-w-4xl">
      <Link href="/" className="inline-flex items-center text-gray-500 hover:text-gray-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>
      
      <div className="flex items-center gap-4 mb-10">
        <div className={`w-4 h-12 rounded-full ${subjectInfo.bgClass}`}></div>
        <h1 className="text-4xl font-extrabold text-gray-900">{subjectInfo.title}</h1>
      </div>

      {topics.length === 0 ? (
        <div className="text-center p-10 bg-white rounded-2xl border border-gray-100 shadow-sm">
          <p className="text-gray-500">Тем поки немає. Запусти ініціалізацію бази.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {topics.map((topic, index) => (
            <div key={topic.id} className="p-5 rounded-2xl bg-white border border-gray-100 shadow-soft hover:shadow-md transition-shadow flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              
              <div className="flex items-start gap-4">
                <span className="text-2xl font-bold text-gray-300">{(index + 1).toString().padStart(2, '0')}</span>
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">{topic.title}</h3>
                  <div className="flex items-center text-sm text-gray-500 mt-1 gap-2">
                    <BookOpen className="w-4 h-4" />
                    <span>{topic._count.flashcards} карток</span>
                  </div>
                  <div className="text-xs text-gray-400 mt-1">ID теми для бота: <code className="bg-gray-100 px-1 rounded">{topic.id}</code></div>
                </div>
              </div>

              <div className="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
                {/* Тимчасово статус "Не почато", поки не додамо збереження прогресу для юзера */}
                <span className="px-3 py-1 bg-gray-200 text-gray-600 rounded-full text-xs font-bold uppercase">Не почато</span>
                
                <Link href={`/subjects/${params.subject}/topic/${topic.id}`}>
                  <button className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-800 transition">
                    Вчити
                  </button>
                </Link>
              </div>
              
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
