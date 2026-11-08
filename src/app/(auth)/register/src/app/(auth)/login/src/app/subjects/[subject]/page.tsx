import Link from "next/link";
import { ArrowLeft, BookOpen } from "lucide-react";
import { SUBJECT_DETAILS, Subject } from "@/types";

export default function SubjectPage({ params }: { params: { subject: string } }) {
  const subjectKey = params.subject.toUpperCase() as Subject;
  const subjectInfo = SUBJECT_DETAILS[subjectKey];

  if (!subjectInfo) {
    return <div className="p-10 text-center text-2xl font-bold">Предмет не знайдено</div>;
  }

  // Тимчасові дані (заглушки). Пізніше ми будемо тягнути це з бази даних (Prisma).
  const mockTopics = [
    { id: "1", title: "Вступна тема", status: "LEARNED", flashcards: 15 },
    { id: "2", title: "Основні поняття та терміни", status: "IN_PROGRESS", flashcards: 42 },
    { id: "3", title: "Практичне застосування", status: "NOT_STARTED", flashcards: 10 },
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "LEARNED": return <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold uppercase">Вивчено</span>;
      case "IN_PROGRESS": return <span className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-bold uppercase">В процесі</span>;
      default: return <span className="px-3 py-1 bg-gray-200 text-gray-600 rounded-full text-xs font-bold uppercase">Не почато</span>;
    }
  };

  return (
    <main className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Шапка */}
      <Link href="/" className="inline-flex items-center text-gray-500 hover:text-gray-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>
      
      <div className="flex items-center gap-4 mb-10">
        <div className={`w-4 h-12 rounded-full ${subjectInfo.bgClass}`}></div>
        <h1 className="text-4xl font-extrabold text-gray-900">{subjectInfo.title}</h1>
      </div>

      {/* Список тем */}
      <div className="space-y-4">
        {mockTopics.map((topic, index) => (
          <div key={topic.id} className="p-5 rounded-2xl bg-white border border-gray-100 shadow-soft hover:shadow-md transition-shadow flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            
            <div className="flex items-start gap-4">
              <span className="text-2xl font-bold text-gray-300">{(index + 1).toString().padStart(2, '0')}</span>
              <div>
                <h3 className="text-lg font-semibold text-gray-800">{topic.title}</h3>
                <div className="flex items-center text-sm text-gray-500 mt-1 gap-2">
                  <BookOpen className="w-4 h-4" />
                  <span>{topic.flashcards} карток</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
              {getStatusBadge(topic.status)}
              
              <Link href={`/subjects/${params.subject}/topic/${topic.id}`}>
                <button className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-800 transition">
                  Відкрити
                </button>
              </Link>
            </div>
            
          </div>
        ))}
      </div>
    </main>
  );
}
