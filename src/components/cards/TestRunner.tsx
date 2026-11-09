"use client";

import { useState } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight, CheckCircle2, XCircle } from "lucide-react";
import ZoomImage from "@/components/shared/ZoomImage";

type Q = { id: string; text: string; options: string[]; imageUrl?: string | null };
type Detail = { id: string; correctIndex: number; chosen: number | null };
type Result = {
  correct: number;
  total: number;
  percent: number;
  saved: boolean;
  details: Detail[];
  threshold?: number;
  passed?: boolean;
  score?: number;
  bestScore?: number;
};

const LETTERS = ["А", "Б", "В", "Г", "Д"];

function resultColor(p: number) {
  if (p >= 80) return "text-green-600";
  if (p >= 50) return "text-yellow-600";
  return "text-red-600";
}

// Універсальний тест: працює і для тестів теми, і для практики по підрозділу, і для пробного НМТ
export default function TestRunner({
  questions,
  submitUrl,
  payload,
  backHref,
  backLabel,
  loggedIn,
}: {
  questions: Q[];
  submitUrl: string;
  payload: Record<string, unknown>;
  backHref: string;
  backLabel: string;
  loggedIn: boolean;
}) {
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const q = questions[index];
  const answeredCount = Object.keys(answers).length;
  const isLast = index === questions.length - 1;

  const finish = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(submitUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...payload, answers }),
      });
      if (!res.ok) throw new Error();
      setResult(await res.json());
    } catch {
      setError("Не вдалось порахувати результат. Спробуй ще раз.");
    } finally {
      setLoading(false);
    }
  };

  const restart = () => {
    setAnswers({});
    setIndex(0);
    setResult(null);
  };

  if (result) {
    const mistakes = questions
      .map((question) => ({ question, d: result.details.find((x) => x.id === question.id)! }))
      .filter(({ d }) => d.chosen !== d.correctIndex);

    return (
      <div className="mt-8">
        <div className="text-center p-8 rounded-3xl bg-white border border-slate-200 shadow-xl">
          {result.score !== undefined ? (
            <>
              <p className="text-slate-500 mb-2">Твій бал (шкала 100–200)</p>
              <p className="text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-pink-500">{result.score}</p>
              <p className="text-slate-600 mt-2">
                {result.correct} з {result.total} правильно ({result.percent}%)
              </p>
              {result.bestScore !== undefined && loggedIn && (
                <p className="text-sm text-indigo-600 font-semibold mt-2">Твоя найкраща спроба: {result.bestScore}</p>
              )}
            </>
          ) : (
            <>
              <p className="text-slate-500 mb-2">Твій результат</p>
              <p className={`text-7xl font-extrabold ${resultColor(result.percent)}`}>{result.percent}%</p>
              <p className="text-slate-600 mt-2">
                {result.correct} з {result.total} правильно
              </p>
              {result.threshold !== undefined && (
                <p className={`inline-flex items-center gap-2 mt-4 px-4 py-2 rounded-full font-bold ${result.passed ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                  {result.passed ? <CheckCircle2 className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
                  {result.passed ? `Складено! Поріг ${result.threshold}%` : `Не складено. Потрібно ${result.threshold}%`}
                </p>
              )}
            </>
          )}

          <p className="text-sm text-slate-500 mt-4">
            {result.saved ? (
              "Результат збережено в твоєму прогресі."
            ) : loggedIn ? (
              "Не вдалось зберегти результат."
            ) : (
              <>
                Щоб результат зберігався, <Link href="/login" className="text-indigo-600 underline">увійди</Link> в акаунт.
              </>
            )}
          </p>
          <div className="flex gap-3 justify-center mt-6">
            <button onClick={restart} className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold hover:bg-slate-800 transition">
              Пройти ще раз
            </button>
            <Link href={backHref} className="px-5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 transition">
              {backLabel}
            </Link>
          </div>
        </div>

        {mistakes.length > 0 && (
          <div className="mt-8 space-y-4">
            <h2 className="text-xl font-bold text-slate-800">Помилки ({mistakes.length})</h2>
            {mistakes.map(({ question, d }) => (
              <div key={question.id} className="p-5 rounded-2xl bg-white border border-slate-100 shadow-md">
                {question.imageUrl && <ZoomImage src={question.imageUrl} className="max-h-40 mb-3" />}
                <p className="font-semibold text-slate-800 mb-3">{question.text}</p>
                <p className="text-sm text-red-600">
                  Твоя відповідь: {d.chosen === null ? "не відповів" : `${LETTERS[d.chosen]}. ${question.options[d.chosen]}`}
                </p>
                <p className="text-sm text-green-700">
                  Правильно: {LETTERS[d.correctIndex]}. {question.options[d.correctIndex]}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="mt-8">
      <div className="flex justify-between items-center mb-4">
        <span className="text-slate-500 font-medium">Питання</span>
        <span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-bold">
          {index + 1} / {questions.length}
        </span>
      </div>
      <div className="w-full bg-slate-200 rounded-full h-2 mb-6 overflow-hidden">
        <div className="h-2 rounded-full bg-gradient-to-r from-violet-500 to-pink-500 transition-all" style={{ width: `${(answeredCount / questions.length) * 100}%` }} />
      </div>

      <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xl">
        {q.imageUrl && (
          <div className="flex justify-center mb-5">
            <ZoomImage src={q.imageUrl} className="max-h-72" />
          </div>
        )}
        <h2 className="text-xl font-semibold text-slate-900 mb-5">{q.text}</h2>
        <div className="space-y-3">
          {q.options.map((opt, i) => {
            const selected = answers[q.id] === i;
            return (
              <button
                key={i}
                onClick={() => setAnswers((a) => ({ ...a, [q.id]: i }))}
                className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${
                  selected ? "bg-indigo-600 text-white border-indigo-600 shadow-md" : "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300"
                }`}
              >
                <span className={`font-bold ${selected ? "text-white" : "text-slate-400"}`}>{LETTERS[i]}</span>
                <span>{opt}</span>
              </button>
            );
          })}
        </div>
      </div>

      {error && <p className="text-red-500 text-sm text-center mt-4">{error}</p>}

      <div className="flex justify-between items-center mt-6">
        <button
          onClick={() => setIndex((i) => Math.max(0, i - 1))}
          disabled={index === 0}
          className="p-3 rounded-full bg-white shadow-md text-slate-600 disabled:opacity-40 hover:bg-slate-50 transition"
        >
          <ChevronLeft className="w-6 h-6" />
        </button>

        {isLast ? (
          <button
            onClick={finish}
            disabled={loading}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-semibold hover:opacity-90 transition disabled:opacity-60 shadow-md"
          >
            {loading ? "Рахую..." : `Завершити (${answeredCount}/${questions.length})`}
          </button>
        ) : (
          <button
            onClick={() => setIndex((i) => Math.min(questions.length - 1, i + 1))}
            className="p-3 rounded-full bg-white shadow-md text-slate-600 hover:bg-slate-50 transition"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        )}
      </div>
    </div>
  );
}
