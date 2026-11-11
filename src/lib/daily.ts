import prisma from "@/lib/prisma";
import { kyivDate } from "@/lib/kyiv";
import { isUnverifiedHistoryQuestion, verifiedQuestionWhere } from "@/lib/history-review";

const MIN_ANSWERS = 5;

// «Питання-пастка»: питання з найнижчою часткою правильних відповідей (мін. 5 відповідей).
// Якщо статистики ще немає — випадкове. Результат кешується в DailyQuestion на добу.
export async function getDailyQuestionId(date = kyivDate()): Promise<string | null> {
  const existing = await prisma.dailyQuestion.findUnique({ where: { date } });
  if (existing) {
    const q = await prisma.question.findUnique({ where: { id: existing.questionId }, select: { imageUrl: true } });
    // Do not show an already-cached daily question if its historical illustration is under review.
    return q && !isUnverifiedHistoryQuestion(q.imageUrl) ? existing.questionId : null;
  }

  const used = (await prisma.dailyQuestion.findMany({ orderBy: { date: "desc" }, take: 60, select: { questionId: true } })).map((d) => d.questionId);

  const [total, correct] = await Promise.all([
    prisma.userAnswer.groupBy({ by: ["questionId"], where: { questionId: { notIn: used } }, _count: { _all: true } }),
    prisma.userAnswer.groupBy({ by: ["questionId"], where: { isCorrect: true, questionId: { notIn: used } }, _count: { _all: true } }),
  ]);
  const okMap = new Map(correct.map((c) => [c.questionId, c._count._all]));
  const trap = total
    .filter((t) => t._count._all >= MIN_ANSWERS)
    .map((t) => ({ id: t.questionId, rate: (okMap.get(t.questionId) ?? 0) / t._count._all }))
    .sort((a, b) => a.rate - b.rate)[0];

  // Trap questions also go through the same review guard as ordinary quizzes.
  const safeTrap = trap ? await prisma.question.findFirst({
    where: { id: trap.id, ...verifiedQuestionWhere },
    select: { id: true },
  }) : null;
  let questionId = safeTrap?.id ?? null;
  if (!questionId) {
    const all = await prisma.question.findMany({ where: { id: { notIn: used }, ...verifiedQuestionWhere }, select: { id: true } });
    const pool = all.length ? all : await prisma.question.findMany({ where: verifiedQuestionWhere, select: { id: true } });
    if (pool.length === 0) return null;
    questionId = pool[Math.floor(Math.random() * pool.length)].id;
  }

  try {
    await prisma.dailyQuestion.create({ data: { date, questionId } });
    return questionId;
  } catch {
    // паралельний запит уже створив запис
    return (await prisma.dailyQuestion.findUnique({ where: { date } }))?.questionId ?? questionId;
  }
}
