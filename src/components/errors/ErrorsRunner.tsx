"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useSession } from "next-auth/react";
import { CheckCircle2, Flame, Lightbulb, XCircle } from "lucide-react";
import ZoomImage from "@/components/shared/ZoomImage";
import LoginPrompt from "@/components/shared/LoginPrompt";

const LETTERS = ["А", "Б", "В", "Г", "Д"];

type Q = { id: string; text: string; options: string[]; imageUrl?: string | null; failCount: number; consecutiveCorrect: number };
type Data = { sessionId: string; open: number; resolved: number; need: number; questions: Q[] };
type Feedback = { chosen: number; correct: boolean; correctIndex: number; explanation: string | null; consecutiveCorrect: number; isResolved: boolean };

export function Flames({ value, need = 3 }: { value: number; need?: number }) {
  return (
    <div className="flex items-center gap-1" title={`${value}/${need}`}>
      {Array.from({ length: need }).map((_, i) => (
        <Flame key={i} className={`w-6 h-6 transition ${i < value ? "text-orange-500 fill-orange-400" : "text-slate-300"}`} />
      ))}
      <span className="ml-1 text-sm font-bold text-slate-600">{value}/{need}</span>
    </div>
  );
}

export default function ErrorsRunner() {
  const { status } = useSession();
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [index, setIndex] = useState(0);
  const [fb, setFb] = useState<Feedback | null>(null);
  const [busy, setBusy] = useState(false);
  const [stats, setStats] = useState({ right: 0, wrong: 0, resolved: 0 });

  const load = async () => {
    setLoading(true);
    setError("");
    setIndex(0);
    setFb(null);
    setStats({ right: 0, wrong: 0, resolved: 0 });
    try {
      const res = await fetch("/api/errors?limit=20", { cache: "no-store" });
      if (!res.ok) throw new Error();
      setData(await res.json());
    } catch {
      setError("Не вдалось завантажити помилки.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (status === "authenticated") load();
    else if (status === "unauthenticated") setLoading(false);
  }, [status]);

  if (status === "unauthenticated") return <LoginPrompt text="Увійди, щоб бачити свій банк помилок." />;
  if (loading || !data) return <p className="text-center text-slate-500 mt-10">{error || "Завантаження…"}</p>;

  const q = data.questions[index];

  if (!q) {
    const done = data.questions.length > 0;
    return (
      <div className="text-center p-8 mt-8 rounded-3xl bg-white border border-slate-200 shadow-xl">
        <p className="text-5xl mb-3">{done ? "🎯" : "🎉"}</p>
        <p className="text-xl font-bold text-slate-800">{done ? "Серію завершено" : "Відкритих помилок немає"}</p>
        {done && (
          <p className="text-slate-600 mt-2">
            Правильно: {stats.right} · Неправильно: {stats.wrong} · Закрито: {stats.resolved}
          </p>
        )}
        <p className="text-sm text-slate-500 mt-2">Закрито за весь час: {data.resolved + stats.resolved}</p>
        <div className="flex gap-3 justify-center mt-6">
          {done && <button onClick={load} className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold">Ще серія</button>}
          <Link href="/profile" className="px-5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold">Профіль</Link>
        </div>
      </div>
    );
  }

  const answer = async (i: number) => {
    if (fb || busy) return;
    setBusy(true);
    try {
      const res = await fetch("/api/errors", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: data.sessionId, questionId: q.id, chosen: i }),
      });
      if (!res.ok) throw new Error();
      const r = await res.json();
      setFb({ chosen: i, ...r });
      setStats((s) => ({ right: s.right + (r.correct ? 1 : 0), wrong: s.wrong + (r.correct ? 0 : 1), resolved: s.resolved + (r.isResolved ? 1 : 0) }));
    } catch {
      setError("Не вдалось зберегти відповідь.");
    } finally {
      setBusy(false);
    }
  };

  const shownFlames = fb ? fb.consecutiveCorrect : q.consecutiveCorrect;

  return (
    <div className="mt-6">
      <div className="flex justify-between items-center mb-4">
        <Flames value={shownFlames} need={data.need} />
        <span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-bold">
          {index + 1} / {data.questions.length}
        </span>
      </div>
      <p className="text-xs text-slate-500 mb-2">Помилок у цьому питанні: {q.failCount} · відкритих у банку: {data.open}</p>

      <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xl">
        {q.imageUrl && <div className="flex justify-center mb-5"><ZoomImage src={q.imageUrl} className="max-h-72" /></div>}
        <h2 className="text-xl font-semibold text-slate-900 mb-5">{q.text}</h2>
        <div className="space-y-3">
          {q.options.map((opt, i) => {
            let cls = "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300";
            if (fb) {
              if (i === fb.correctIndex) cls = "bg-green-50 border-green-500 text-green-900";
              else if (i === fb.chosen) cls = "bg-red-50 border-red-400 text-red-900";
              else cls = "bg-slate-50 border-slate-200 opacity-60";
            }
            return (
              <button key={i} onClick={() => answer(i)} disabled={!!fb || busy} className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${cls}`}>
                <span className="font-bold text-slate-400">{LETTERS[i]}</span>
                <span>{opt}</span>
              </button>
            );
          })}
        </div>
      </div>

      {fb && (
        <div className="mt-5 rounded-3xl border border-slate-200 bg-white shadow-xl overflow-hidden">
          <div className={`px-5 py-3 flex items-center gap-2 font-bold ${fb.correct ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
            {fb.correct ? <CheckCircle2 className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
            {fb.isResolved ? "Правильно! Помилку закрито 🎉" : fb.correct ? "Правильно!" : "Неправильно — лічильник скинуто"}
          </div>
          <div className="p-5 space-y-4">
            <div>
              <p className="flex items-center gap-2 font-bold text-amber-700 mb-1"><Lightbulb className="w-5 h-5" /> Обґрунтування</p>
              <p className="text-slate-700">{fb.explanation ?? "Для цього питання обґрунтування ще не додано."}</p>
            </div>
            <div>
              <p className="font-bold text-slate-800 mb-2">Чому інші варіанти не підходять</p>
              <ul className="space-y-1 text-sm">
                {q.options.map((opt, i) =>
                  i === fb.correctIndex ? null : (
                    <li key={i} className={`flex gap-2 ${i === fb.chosen ? "text-red-700 font-semibold" : "text-slate-600"}`}>
                      <span>✗</span>
                      <span>{LETTERS[i]}. {opt}{i === fb.chosen ? " — твоя відповідь" : ""}</span>
                    </li>
                  )
                )}
              </ul>
              <p className="text-sm text-green-700 mt-2">Правильно: {LETTERS[fb.correctIndex]}. {q.options[fb.correctIndex]}</p>
            </div>
          </div>
        </div>
      )}

      {error && <p className="text-red-500 text-sm text-center mt-4">{error}</p>}
      {fb && (
        <div className="flex justify-end mt-5">
          <button onClick={() => { setFb(null); setIndex((i) => i + 1); }} className="px-6 py-3 rounded-xl bg-gradient-to-r from-violet-500 to-pink-500 text-white font-semibold shadow-md">
            {index + 1 === data.questions.length ? "Підсумок" : "Далі"}
          </button>
        </div>
      )}
    </div>
  );
}
