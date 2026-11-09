import Link from "next/link";
import { ArrowLeft, Flame } from "lucide-react";
import { getServerSession } from "next-auth";
import prisma from "@/lib/prisma";
import { authOptions } from "@/lib/auth";
import TestRunner from "@/components/cards/TestRunner";
import ExamCountdown from "@/components/shared/ExamCountdown";

export const dynamic = "force-dynamic";

export default async function ExamPage({ params }: { params: { id: string } }) {
  const session = await getServerSession(authOptions);

  // correctIndex не вибираємо: правильні відповіді браузер не бачить
  const exam = await prisma.weeklyExam.findUnique({
    where: { id: params.id },
    include: { questions: { select: { id: true, text: true, options: true, imageUrl: true }, orderBy: { createdAt: "asc" } } },
  });

  const now = new Date();
  const available = !!exam && exam.isActive && exam.startTime <= now && exam.endTime > now;

  return (
    <main className="container mx-auto px-4 py-6 max-w-2xl min-h-screen">
      <Link href="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>

      {!exam || !available ? (
        <div className="text-center p-10 mt-8 bg-white rounded-3xl border border-slate-100 shadow-md">
          <p className="text-slate-600">Це пробне НМТ зараз недоступне. Повернись на головну, там з’явиться актуальне.</p>
        </div>
      ) : (
        <>
          <div className="rounded-3xl bg-gradient-to-r from-amber-500 to-rose-500 p-6 text-white shadow-xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-sm font-bold mb-2">
              <Flame className="w-4 h-4" /> Пробне НМТ
            </div>
            <h1 className="text-2xl font-extrabold">{exam.title}</h1>
            <p className="text-white/90 text-sm mt-1">
              Питань: {exam.questions.length} · до кінця: <ExamCountdown endTime={exam.endTime.toISOString()} />
            </p>
          </div>

          {exam.questions.length === 0 ? (
            <p className="text-center text-slate-500 mt-8">У цьому пробному ще немає питань.</p>
          ) : (
            <TestRunner
              questions={exam.questions}
              submitUrl="/api/exam/submit"
              payload={{ examId: exam.id }}
              backHref="/"
              backLabel="На головну"
              loggedIn={!!session?.user?.id}
            />
          )}
        </>
      )}
    </main>
  );
}
