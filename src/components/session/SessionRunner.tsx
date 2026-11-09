"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSession } from "next-auth/react";
import { ChevronLeft, ChevronRight, Clock, Lightbulb } from "lucide-react";
import ZoomImage from "@/components/shared/ZoomImage";
import LoginPrompt from "@/components/shared/LoginPrompt";
import { SUBJECT_DETAILS, SUBJECT_ORDER, type Subject } from "@/types";

const LETTERS = ["А", "Б", "В", "Г", "Д"];

type Q = { id: string; text: string; options: string[]; imageUrl?: string | null; subject: Subject };
type Run = { id: string; kind: string; deadlineAt: string | null; currentIdx: number; answers: Record<string, number>; questions: Q[]; resumed: boolean };
type Detail = { id: string; subject: Subject; chosen: number | null; correctIndex: number; explanation: string | null; isCorrect: boolean };
type Result = {
  correct: number;
  total: number;
  percent: number;
  perSubject: { subject: Subject; title: string; correct: number; total: number; percent: number }[];
  details: Detail[];
};

const fmt = (ms: number) => {
  const s = Math.max(0, Math.floor(ms / 1000));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = s % 60;
  return `${h ? h + ":" : ""}${String(m).padStart(h ? 2 : 1, "0")}:${String(ss).padStart(2, "0")}`;
};

const level = (p: number) =>
  p > 80 ? { label: "Сильно", cls: "bg-green-100 text-green-700" } : p >= 60 ? { label: "Середньо", cls: "bg-yellow-100 text-yellow-700" } : { label: "Слабко", cls: "bg-red-100 text-red-700" };

export default function SessionRunner({ kind }: { kind: "DIAGNOSTIC" | "SIMULATION" }) {
  const { status } = useSession();
  const [run, setRun] = useState<Run | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [left, setLeft] = useState<number | null>(null);
  const finishing = useRef(false);
  const latest = useRef({ answers, index });
  latest.current = { answers, index };

  const start = async (restart = false) => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kind, restart }),
      });
      if (!res.ok) throw new Error();
      const d: Run = await res.json();
      finishing.current = false;
      setRun(d);
      setAnswers(d.answers ?? {});
      setIndex(d.currentIdx ?? 0);
      setResult(null);
    } catch {
      setError("Не вдалось почати. Перевір, чи є питання в базі.");
    } finally {
      setLoading(false);
    }
  };

  const finish = useCallback(async () => {
    if (!run || finishing.current) return;
    finishing.current = true;
    setLoading(true);
    try {
      const res = await fetch("/api/sessions/finish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: run.id, answers: latest.current.answers }),
      });
      if (!res.ok) throw new Error();
      setResult(await res.json());
    } catch {
      finishing.current = false;
      setError("Не вдалось завершити. Спробуй ще раз.");
    } finally {
      setLoading(false);
    }
  }, [run]);

  // Автозбереження проміжного стану
  useEffect(() => {
    if (!run || result) return;
    const t = setTimeout(() => {
      fetch("/api/sessions", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: run.id, answers, currentIdx: index }),
      }).then((r) => { if (r.status === 409) finish(); }).catch(() => {});
    }, 600);
    return () => clearTimeout(t);
  }, [answers, index, run, result, finish]);

  // Таймер
  useEffect(() => {
    if (!run?.deadlineAt || result) return;
    const end = new Date(run.deadlineAt).getTime();
    const tick = () => {
      const ms = end - Date.now();
      setLeft(ms);
      if (ms <= 0) finish();
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [run, result, finish]);

  if (status === "loading") return null;
  if (status === "unauthenticated") return <LoginPrompt text="Увійди, щоб проходити тести й зберігати прогрес." />;

  /* ---------- Старт ---------- */
  if (!run) {
    return (
      <div className="text-center p-8 mt-8 rounded-3xl bg-white border border-slate-200 shadow-xl">
        <p className="text-5xl mb-3">{kind === "DIAGNOSTIC" ? "🧭" : "⏱️"}</p>
        <button onClick={() => start(false)} disabled={loading} className="px-6 py-3 rounded-xl bg-gradient-to-r from-violet-500 to-pink-500 text-white font-semibold shadow-md disabled:opacity-60">
          {loading ? "Готую питання…" : "Почати / продовжити"}
        </button>
        <p className="text-xs text-slate-500 mt-3">Якщо в тебе є незавершена спроба — вона відновиться з того ж місця.</p>
        {error && <p className="text-red-500 text-sm mt-3">{error}</p>}
      </div>
    );
  }

  /* ---------- Результат ---------- */
  if (result) {
    const weakest = [...result.perSubject].filter((s) => s.total).sort((a, b) => a.percent - b.percent)[0];
    const mistakes = result.details.filter((d) => !d.isCorrect);
    const qMap = new Map(run.questions.map((q) => [q.id, q]));
    return (
      <div className="mt-8">
        <div className="text-center p-8 rounded-3xl bg-white border border-slate-200 shadow-xl">
          <p className="text-slate-500 mb-1">{kind === "DIAGNOSTIC" ? "Твій стартовий розклад знань" : "Результат симуляції"}</p>
          <p className="text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-pink-500">{result.percent}%</p>
          <p className="text-slate-600 mt-1">{result.correct} з {result.total} правильно</p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-6 text-left">
            {result.perSubject.map((s) => {
              const th = SUBJECT_DETAILS[s.subject];
              const lv = level(s.percent);
              return (
                <div key={s.subject} className={`rounded-2xl p-4 text-white bg-gradient-to-br ${th.gradient}`}>
                  <div className="flex justify-between items-center">
                    <p className="font-bold">{th.title}</p>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${lv.cls}`}>{lv.label}</span>
                  </div>
                  <p className="text-3xl font-extrabold mt-1">{s.percent}%</p>
                  <p className="text-sm text-white/80 mb-2">{s.correct} з {s.total}</p>
                  <div className="w-full bg-white/25 rounded-full h-2 overflow-hidden"><div className="h-2 bg-white rounded-full" style={{ width: `${s.percent}%` }} /></div>
                </div>
              );
            })}
          </div>

          {weakest && <p className="mt-5 text-slate-700">Почни з предмета: <b>{SUBJECT_DETAILS[weakest.subject].title}</b> ({weakest.percent}%).</p>}
          <p className="text-xs text-slate-500 mt-2">Помилки автоматично потрапили в Банк помилок.</p>

          <div className="flex flex-wrap gap-3 justify-center mt-6">
            <Link href="/errors" className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold">Повторити помилки</Link>
            <button onClick={() => start(true)} className="px-5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold">Нова спроба</button>
            <Link href="/profile" className="px-5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold">Профіль</Link>
          </div>
        </div>

        {mistakes.length > 0 && (
          <div className="mt-8 space-y-4">
            <h2 className="text-xl font-bold text-slate-800">Помилки ({mistakes.length})</h2>
            {mistakes.map((d) => {
              const q = qMap.get(d.id);
              if (!q) return null;
              return (
                <div key={d.id} className="p-5 rounded-2xl bg-white border border-slate-100 shadow-md">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${SUBJECT_DETAILS[d.subject].pill}`}>{SUBJECT_DETAILS[d.subject].title}</span>
                  {q.imageUrl && <ZoomImage src={q.imageUrl} className="max-h-40 my-3" />}
                  <p className="font-semibold text-slate-800 my-3">{q.text}</p>
                  <p className="text-sm text-red-600">Твоя відповідь: {d.chosen === null ? "не відповів" : `${LETTERS[d.chosen]}. ${q.options[d.chosen]}`}</p>
                  <p className="text-sm text-green-700">Правильно: {LETTERS[d.correctIndex]}. {q.options[d.correctIndex]}</p>
                  {d.explanation && (
                    <p className="mt-3 text-sm text-slate-700 bg-amber-50 rounded-xl p-3 flex gap-2"><Lightbulb className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />{d.explanation}</p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  }

  /* ---------- Проходження ---------- */
  const q = run.questions[index];
  const answered = Object.keys(answers).length;
  const isLast = index === run.questions.length - 1;
  const urgent = left !== null && left < 5 * 60_000;

  return (
    <div className="mt-6">
      <div className="flex justify-between items-center mb-3">
        <span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-bold">{index + 1} / {run.questions.length}</span>
        {left !== null && (
          <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-extrabold tabular-nums ${urgent ? "bg-red-100 text-red-700 animate-pulse" : "bg-slate-100 text-slate-700"}`}>
            <Clock className="w-4 h-4" /> {fmt(left)}
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-x-4 gap-y-2 mb-4">
        {SUBJECT_ORDER.map((s) => {
          const own = run.questions.filter((x) => x.subject === s);
          const done = own.filter((x) => answers[x.id] !== undefined).length;
          const th = SUBJECT_DETAILS[s];
          return (
            <div key={s}>
              <div className="flex justify-between text-xs text-slate-600 mb-1"><span className="font-semibold">{th.title}</span><span>{done}/{own.length}</span></div>
              <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden"><div className={`h-2 rounded-full ${th.bgClass} transition-all`} style={{ width: own.length ? `${(done / own.length) * 100}%` : "0%" }} /></div>
            </div>
          );
        })}
      </div>

      <div className="flex flex-wrap gap-1.5 mb-5">
        {run.questions.map((x, i) => (
          <button
            key={x.id}
            onClick={() => setIndex(i)}
            className={`w-8 h-8 rounded-lg text-xs font-bold transition ${
              i === index ? "bg-indigo-600 text-white ring-2 ring-indigo-300" : answers[x.id] !== undefined ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500 hover:bg-slate-200"
            }`}
          >
            {i + 1}
          </button>
        ))}
      </div>

      <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xl">
        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${SUBJECT_DETAILS[q.subject].pill}`}>{SUBJECT_DETAILS[q.subject].title}</span>
        {q.imageUrl && <div className="flex justify-center my-4"><ZoomImage src={q.imageUrl} className="max-h-72" /></div>}
        <h2 className="text-xl font-semibold text-slate-900 my-4">{q.text}</h2>
        <div className="space-y-3">
          {q.options.map((opt, i) => {
            const selected = answers[q.id] === i;
            return (
              <button
                key={i}
                onClick={() => setAnswers((a) => ({ ...a, [q.id]: i }))}
                className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${selected ? "bg-indigo-600 text-white border-indigo-600 shadow-md" : "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300"}`}
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
        <button onClick={() => setIndex((i) => Math.max(0, i - 1))} disabled={index === 0} className="p-3 rounded-full bg-white shadow-md text-slate-600 disabled:opacity-40">
          <ChevronLeft className="w-6 h-6" />
        </button>
        <button
          onClick={() => { if (answered === run.questions.length || confirm(`Без відповіді: ${run.questions.length - answered}. Завершити?`)) finish(); }}
          disabled={loading}
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-semibold shadow-md disabled:opacity-60"
        >
          {loading ? "Рахую…" : `Завершити (${answered}/${run.questions.length})`}
        </button>
        <button onClick={() => setIndex((i) => Math.min(run.questions.length - 1, i + 1))} disabled={isLast} className="p-3 rounded-full bg-white shadow-md text-slate-600 disabled:opacity-40">
          <ChevronRight className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
}
