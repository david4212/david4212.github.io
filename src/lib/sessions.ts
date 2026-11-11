import { calculateNmtScore, averageNmt } from "@/lib/score";
import prisma from "@/lib/prisma";
import { recordAnswers, shuffle, type AnswerSource } from "@/lib/answers";
import { SUBJECT_DETAILS, SUBJECT_ORDER, NMT_STRUCTURE, type Subject, type ProbnikDifficulty, type QuestionType } from "@/types";
import { verifiedQuestionWhere } from "@/lib/history-review";

export const SUBJECTS: Subject[] = ["UKRAINIAN", "MATH", "HISTORY", "ENGLISH"];

// Діагностика: 4 × 5 = 20 питань без таймера.
// Пробник НМТ: UA 30, Math 22, History 30, English 32 = 114 питань, 60 хв/предмет (загалом 240 хв)
export const KINDS = {
  DIAGNOSTIC: { perSubject: 5, minutes: null as number | null },
  SIMULATION: { perSubject: null as number | null, minutes: 240 }, // пробник НМТ (було: 10 за предмет, 90 хв)
} as const;
export type Kind = keyof typeof KINDS;

/**
 * Збирає питання для пробника НМТ з урахуванням складності.
 * difficulty: 1 = Easy (30% hard), 2 = Medium (50% hard), 3 = Hard (80% hard)
 * hardPercent — відсоток питань testLevel=3 у тесті.
 * Решта — рівномірно з testLevel 1 і 2.
 */
export async function buildQuestionIds(kind: Kind, difficulty: ProbnikDifficulty = 2): Promise<string[]> {
  // Для історії додаємо фільтр верифікованих питань
  const historyFilter = (subject: string) => subject === "HISTORY" ? verifiedQuestionWhere : {};

  if (kind === "DIAGNOSTIC") {
    const ids: string[] = [];
    for (const subject of SUBJECTS) {
      const rows = await prisma.question.findMany({
        where: { topic: { subject }, questionType: "single_choice", ...historyFilter(subject) },
        select: { id: true },
      });
      ids.push(...shuffle(rows.map((r) => r.id)).slice(0, 5));
    }
    return shuffle(ids);
  }

  // Пробник НМТ — реальний склад за типами питань (NMT_STRUCTURE), порядок: предмет → тип
  const hardPercent = { 1: 30, 2: 50, 3: 80 }[difficulty] ?? 50;
  const ids: string[] = [];
  const TYPE_ORDER: QuestionType[] = ["single_choice", "matching", "sequencing", "choose_multi", "fill_blanks", "short_answer"];

  for (const subject of SUBJECT_ORDER) {
    const hFilter = historyFilter(subject);
    const rows: { id: string; testLevel: number; questionType: string }[] = await prisma.question.findMany({
      where: { topic: { subject }, ...hFilter },
      select: { id: true, testLevel: true, questionType: true },
    });
    const used = new Set<string>();
    const pick = (type: QuestionType, count: number) => {
      const pool = rows.filter((r) => r.questionType === type && !used.has(r.id));
      const hardCount = Math.round((count * hardPercent) / 100);
      const hard = shuffle(pool.filter((r) => r.testLevel === 3).map((r) => r.id)).slice(0, hardCount);
      const rest = shuffle(pool.filter((r) => r.testLevel !== 3).map((r) => r.id)).slice(0, count - hard.length);
      let got: string[] = [...hard, ...rest];
      if (got.length < count) {
        const taken = new Set(got);
        got.push(...shuffle(pool.map((r) => r.id).filter((id) => !taken.has(id))).slice(0, count - got.length));
      }
      got.forEach((id) => used.add(id));
      return got;
    };

    const structure = NMT_STRUCTURE[subject];
    const byType: Partial<Record<QuestionType, string[]>> = {};
    let missing = 0;
    for (const type of TYPE_ORDER) {
      if (type === "single_choice") continue;
      const need = structure[type] ?? 0;
      if (!need) continue;
      byType[type] = pick(type, need);
      missing += need - byType[type]!.length;
    }
    // Нестача рідкісних типів компенсується питаннями з однією відповіддю
    byType.single_choice = pick("single_choice", (structure.single_choice ?? 0) + missing);
    for (const type of TYPE_ORDER) ids.push(...(byType[type] ?? []));
  }

  return ids;
}

/** Максимальна кількість балів за питання (як на НМТ). */
export function maxPoints(subject: Subject, qType: string, meta: any): number {
  if (qType === "matching") return meta?.pairs?.length ?? 1;
  if (qType === "sequencing") return 3;
  if (qType === "choose_multi") return meta?.requiredCount ?? 3;
  if (qType === "fill_blanks") return meta?.blanks?.length ?? 1;
  if (qType === "short_answer") return 2;
  return 1;
}

export async function loadQuestions(ids: string[]) {
  const rows = await prisma.question.findMany({
    where: { id: { in: ids }, ...verifiedQuestionWhere },
    select: { id: true, text: true, options: true, imageUrl: true, questionType: true, metadata: true, topic: { select: { subject: true } } },
  });
  const map = new Map(rows.map((r) => [r.id, r]));
  return ids
    .map((id) => map.get(id))
    .filter((q): q is NonNullable<typeof q> => !!q)
    .map(({ topic, ...q }) => ({ ...q, subject: topic.subject as Subject }));
}

// Оцінює сесію й один раз записує відповіді (банк помилок, streak). Повторний виклик лише перераховує результат.
export async function finishSession(sessionId: string, userId: string) {
  const s = await prisma.testSession.findFirst({ where: { id: sessionId, userId } });
  if (!s) return null;

  const saved = (s.answers && typeof s.answers === "object" ? s.answers : {}) as Record<string, any>;
  const qs = await prisma.question.findMany({
    where: { id: { in: s.questionIds }, ...verifiedQuestionWhere },
    select: { id: true, correctIndex: true, explanation: true, questionType: true, metadata: true, topic: { select: { subject: true } } },
  });
  const map = new Map(qs.map((q) => [q.id, q]));

  const details = s.questionIds
    .map((id) => map.get(id))
    .filter((q): q is NonNullable<typeof q> => !!q)
    .map((q) => {
      const ans = saved[q.id];
      const qType = q.questionType ?? "single_choice";
      const meta = q.metadata as any;
      const subject = q.topic.subject as Subject;
      const max = maxPoints(subject, qType, meta);
      let points = 0;
      let chosen: number | null = null;
      const norm = (v: unknown) => String(v ?? "").trim().toLowerCase().replace(/\s+/g, " ").replace(/’|ʼ|`/g, "'");

      if (qType === "single_choice") {
        chosen = typeof ans === "number" ? ans : null;
        points = chosen === q.correctIndex ? 1 : 0;
      } else if (qType === "matching" && Array.isArray(ans) && meta?.pairs) {
        // пари в БД записані у правильній відповідності: лівий i ↔ правий i; 1 бал за кожну пару
        points = meta.pairs.reduce((n: number, _: unknown, i: number) => n + (ans[i] === i ? 1 : 0), 0);
      } else if (qType === "sequencing" && Array.isArray(ans) && Array.isArray(meta?.correctOrder)) {
        // Правило УЦОЯО: 3 — увесь порядок; 2 — перша й остання на місцях; 1 — лише перша або лише остання
        const co: number[] = meta.correctOrder;
        const last = co.length - 1;
        const all = co.every((v, i) => ans[i] === v);
        const first = ans[0] === co[0];
        const end = ans[last] === co[last];
        points = all ? 3 : first && end ? 2 : first || end ? 1 : 0;
      } else if (qType === "choose_multi" && Array.isArray(ans) && Array.isArray(meta?.correctIndices)) {
        points = Math.min(max, new Set(ans.filter((v: number) => meta.correctIndices.includes(v))).size);
      } else if (qType === "fill_blanks" && Array.isArray(ans) && Array.isArray(meta?.blanks)) {
        points = meta.blanks.reduce((n: number, b: { answer: string; alternatives?: string[] }, i: number) => {
          const u = norm(ans[i]);
          return n + (u && [b.answer, ...(b.alternatives ?? [])].some((a) => norm(a) === u) ? 1 : 0);
        }, 0);
      } else if (qType === "short_answer" && (typeof ans === "string" || typeof ans === "number") && meta?.answer !== undefined) {
        const userVal = String(ans).trim();
        let ok: boolean;
        // кома й крапка рівноцінні, пробіли ігноруються, «−» = «-»
        const toNum = (v: unknown) => {
          const t = String(v ?? "").replace(/\s+/g, "").replace(/[−–—]/g, "-").replace(",", ".");
          return /^[-+]?(\d+\.?\d*|\.\d+)$/.test(t) ? Number(t) : NaN;
        };
        const expected = typeof meta.answer === "number" ? meta.answer : toNum(meta.answer);
        if (!isNaN(expected)) {
          const num = toNum(userVal);
          ok = !isNaN(num) && Math.abs(num - expected) <= (meta.tolerance ?? 1e-9);
        } else ok = norm(userVal) === norm(meta.answer);
        points = ok ? max : 0;
      }
      const isCorrect = points === max;

      return { id: q.id, subject, chosen, correctIndex: q.correctIndex, explanation: q.explanation, isCorrect, points, maxPoints: max };
    });

  const correct = details.filter((d) => d.isCorrect).length;
  const total = details.length;
  const percent = total ? Math.round((correct / total) * 100) : 0;

  const perSubject = SUBJECTS.map((subject) => {
    const part = details.filter((d) => d.subject === subject);
    const c = part.filter((d) => d.isCorrect).length;
    // НМТ-бал рахуємо за тестовими балами (часткові бали за відповідність/послідовність/3 із 7)
    const raw = part.reduce((n, d) => n + d.points, 0);
    const rawMax = part.reduce((n, d) => n + d.maxPoints, 0);
    return { subject, title: SUBJECT_DETAILS[subject].title, correct: c, total: part.length, percent: rawMax ? Math.round((raw / rawMax) * 100) : 0, raw, rawMax, nmt: calculateNmtScore(subject, raw, rawMax) };
  });
  const avgNmt = averageNmt(perSubject.filter((p) => p.total).map((p) => p.nmt));

  if (s.status !== "FINISHED") {
    // Атомарно "захоплюємо" завершення, щоб паралельні запити не записали відповіді двічі
    const claimed = await prisma.testSession.updateMany({
      where: { id: s.id, status: "IN_PROGRESS" },
      data: {
        status: "FINISHED",
        finishedAt: new Date(),
        correct,
        total,
        percent,
        nmtScore: avgNmt,
        subjectScores: perSubject.map((p) => ({ subject: p.subject, correct: p.correct, total: p.total, nmtScore: p.nmt.nmtScore, isPassed: p.nmt.isPassed })),
      },
    });
    if (claimed.count === 1) {
      await recordAnswers(
        userId,
        details.map((d) => ({ questionId: d.id, chosen: d.chosen, isCorrect: d.isCorrect })),
        s.kind as AnswerSource,
        s.id
      );
    }
  }

  return { id: s.id, kind: s.kind, correct, total, percent, perSubject, avgNmt, details };
}
