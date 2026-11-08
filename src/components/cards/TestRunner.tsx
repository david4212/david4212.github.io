"use client";

import { useState } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight } from "lucide-react";

type Q = { id: string; text: string; options: string[] };
type Detail = { id: string; correctIndex: number; chosen: number | null };
type Result = { correct: number; total: number; percent: number; saved: boolean; details: Detail[] };

const LETTERS = ["А", "Б", "В", "Г", "Д"];

function resultColor(p: number) {
  if (p >= 80) return "text-green-600";
  if (p >= 50) return "text-yellow-600";
  return "text-red-600";
}

export default function TestRunner({
  topicId,
  subject,
  questions,
  loggedIn,
}: {
  topicId: string;
  subject: string;
  questions: Q[];
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
      const res = await fetch("/api/results", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topicId, answers }),
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
        <div className="text-center p-8 rounded-3xl bg-glass backdrop-blur-glass border border-glassBorder shadow-glass">
          <p className="text-gray-500 mb-2">Твій результат</p>
          <p className={`text-6xl font-extrabold ${resultColor(result.percent)}`}>{result.percent}%</p>
          <p className="text-gray-600 mt-2">
            {result.correct} з {result.total} правильно
          </p>
          <p className="text-sm text-gray-500 mt-4">
            {result.saved ? (
              "Результат збережено в твоєму прогресі."
            ) : loggedIn ? (
              "Не вдалось зберегти результат."
            ) : (
              <>
                Щоб результат зберігався, <Link href="/login" className="text-blue-600 underline">увійди</Link> в акаунт.
              </>
            )}
          </p>
          <div className="flex gap-3 justify-center mt-6">
            <button onClick={restart} className="px-5 py-2 rounded-xl bg-gray-900 text-white font-semibold hover:bg-gray-800 transition">
              Пройти ще раз
            </button>
            <Link href={`/subjects/${subject}`} className="px-5 py-2 rounded-xl bg-white border border-gray-200 text-gray-700 font-semibold hover:bg-gray-50 transition">
              До тем
            </Link>
          </div>
        </div>

        {mistakes.length > 0 && (
          <div className="mt-8 space-y-4">
            <h2 className="text-xl font-bold text-gray-800">Помилки ({mistakes.length})</h2>
            {mistakes.map(({ question, d }) => (
              <div key={question.id} className="p-5 rounded-2xl bg-white border border-gray-100 shadow-soft">
                <p className="font-semibold text-gray-800 mb-3">{question.text}</p>
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
        <span className="text-gray-500 font-medium">Питання</span>
        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-bold">
          {index + 1} / {questions.length}
        </span>
      </div>
      <div className="w-full bg-gray-200/60 rounded-full h-2 mb-6 overflow-hidden">
        <div className="h-2 rounded-full bg-blue-600 transition-all" style={{ width: `${(answeredCount / questions.length) * 100}%` }} />
      </div>

      <div className="p-6 rounded-3xl bg-glass backdrop-blur-glass border border-glassBorder shadow-glass">
        <h2 className="text-xl font-semibold text-gray-900 mb-5">{q.text}</h2>
        <div className="space-y-3">
          {q.options.map((opt, i) => {
            const selected = answers[q.id] === i;
            return (
              <button
                key={i}
                onClick={() => setAnswers((a) => ({ ...a, [q.id]: i }))}
                className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${
                  selected ? "bg-blue-600 text-white border-blue-600" : "bg-white/70 border-gray-200 hover:bg-white"
                }`}
              >
                <span className={`font-bold ${selected ? "text-white" : "text-gray-400"}`}>{LETTERS[i]}</span>
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
          className="p-3 rounded-full bg-white shadow-soft text-gray-600 disabled:opacity-40 hover:bg-gray-50 transition"
        >
          <ChevronLeft className="w-6 h-6" />
        </button>

        {isLast ? (
          <button
            onClick={finish}
            disabled={loading}
            className="px-6 py-3 rounded-xl bg-green-600 text-white font-semibold hover:bg-green-700 transition disabled:opacity-60"
          >
            {loading ? "Рахую..." : `Завершити (${answeredCount}/${questions.length})`}
          </button>
        ) : (
          <button
            onClick={() => setIndex((i) => Math.min(questions.length - 1, i + 1))}
            className="p-3 rounded-full bg-white shadow-soft text-gray-600 hover:bg-gray-50 transition"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        )}
      </div>
    </div>
  );
}
