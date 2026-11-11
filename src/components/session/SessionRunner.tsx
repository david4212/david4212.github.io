"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSession } from "next-auth/react";
import { ChevronLeft, ChevronRight, Clock, Lightbulb, Zap, Shield, Flame } from "lucide-react";
import ZoomImage from "@/components/shared/ZoomImage";
import LoginPrompt from "@/components/shared/LoginPrompt";
import QuestionRenderer, { type FlexAnswer } from "@/components/session/QuestionRenderer";
import { SUBJECT_DETAILS, SUBJECT_ORDER, NMT_CONFIG, DIFFICULTY_LABELS, type Subject, type ProbnikDifficulty, type QuestionType } from "@/types";

const LETTERS = ["А", "Б", "В", "Г", "Д"];

type Q = { id: string; text: string; options: string[]; imageUrl?: string | null; subject: Subject; questionType?: QuestionType; metadata?: unknown };
type Run = { id: string; kind: string; difficulty: number; deadlineAt: string | null; currentIdx: number; answers: Record<string, FlexAnswer>; questions: Q[]; resumed: boolean };
type Detail = { id: string; subject: Subject; chosen: number | null; correctIndex: number; explanation: string | null; isCorrect: boolean };
type Result = {
  correct: number;
  total: number;
  percent: number;
  perSubject: { subject: Subject; title: string; correct: number; total: number; percent: number; nmt: { nmtScore: number | null; isPassed: boolean } }[];
  avgNmt: number | null;
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

const DIFF_ICONS = { 1: Zap, 2: Shield, 3: Flame } as const;
const DIFF_COLORS = {
  1: "from-green-500 to-emerald-600",
  2: "from-blue-500 to-indigo-600",
  3: "from-red-500 to-rose-600",
} as const;

export default function SessionRunner({ kind }: { kind: "DIAGNOSTIC" | "SIMULATION" }) {
  const { status } = useSession();
  const [run, setRun] = useState<Run | null>(null);
  const [answers, setAnswers] = useState<Record<string, FlexAnswer>>({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [left, setLeft] = useState<number | null>(null);
  const [difficulty, setDifficulty] = useState<ProbnikDifficulty>(2);
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
        body: JSON.stringify({ kind, restart, difficulty }),
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

  const isProbnik = kind === "SIMULATION";
  const kindLabel = isProbnik ? "Пробник НМТ" : "Діагностика";

  /* ---------- Старт з вибором складності ---------- */
  if (!run) {
    return (
      <div className="mt-8">
        {isProbnik && (
          <div className="mb-6">
            <h2 className="text-lg font-bold text-slate-800 mb-3">Обери рівень складності</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {([1, 2, 3] as ProbnikDifficulty[]).map((d) => {
                const cfg = DIFFICULTY_LABELS[d];
                const Icon = DIFF_ICONS[d];
                const selected = difficulty === d;
                return (
                  <button
                    key={d}
                    onClick={() => setDifficulty(d)}
                    className={`relative p-4 rounded-2xl border-2 transition-all text-left ${
                      selected
                        ? `border-transparent bg-gradient-to-br ${DIFF_COLORS[d]} text-white shadow-lg scale-[1.02]`
                        : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
                    }`}
                  >
                    <Icon className={`w-6 h-6 mb-2 ${selected ? "text-white" : "text-slate-400"}`} />
                    <p className="font-bold text-lg">{cfg.label}</p>
                    <p className={`text-sm ${selected ? "text-white/80" : "text-slate-500"}`}>{cfg.description}</p>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {isProbnik && (
          <div className="rounded-2xl bg-slate-50 border border-slate-200 p-4 mb-6 text-sm text-slate-600">
            <p className="font-semibold text-slate-800 mb-2">📋 Структура пробника</p>
            <div className="grid grid-cols-2 gap-2">
              {SUBJECT_ORDER.map((s) => {
                const cfg = NMT_CONFIG[s];
                const th = SUBJECT_DETAILS[s];
                return (
                  <div key={s} className="flex justify-between px-3 py-2 rounded-xl bg-white border border-slate-100">
                    <span className={`font-medium ${th.text}`}>{th.title}</span>
                    <span className="text-slate-500">{cfg.questions} питань</span>
                  </div>
                );
              })}
            </div>
            <p className="mt-2 text-xs text-slate-500">Загалом 114 питань · 4 години · Шкала 100–200</p>
          </div>
        )}

        <div className="text-center p-8 rounded-3xl bg-white border border-slate-200 shadow-xl">
          <p className="text-5xl mb-3">{isProbnik ? "📝" : "🧭"}</p>
          <button onClick={() => start(false)} disabled={loading} className="px-6 py-3 rounded-xl bg-gradient-to-r from-violet-500 to-pink-500 text-white font-semibold shadow-md disabled:opacity-60">
            {loading ? "Готую питання…" : "Почати / продовжити"}
          </button>
          <p className="text-xs text-slate-500 mt-3">Якщо в тебе є незавершена спроба — вона відновиться з того ж місця.</p>
          {error && <p className="text-red-500 text-sm mt-3">{error}</p>}
        </div>
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
          <p className="text-slate-500 mb-1">{isProbnik ? `Результат пробника (${DIFFICULTY_LABELS[run.difficulty as ProbnikDifficulty]?.label ?? ""})` : "Твій стартовий розклад знань"}</p>
          {result.avgNmt !== null ? (
            <p className="text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-pink-500">{result.avgNmt}</p>
          ) : (
            <p className="text-4xl font-extrabold text-red-600">Поріг не подолано</p>
          )}
          <p className="text-slate-600 mt-1">{result.correct} з {result.total} правильно ({result.percent}%)</p>

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
                  <p className="text-sm text-white/80">{s.correct} з {s.total}</p>
                  <p className="text-sm font-bold mb-2">{s.total ? (s.nmt.nmtScore !== null ? `≈ ${s.nmt.nmtScore} балів (100–200)` : "Не склав (нижче порогу)") : ""}</p>
                  <div className="w-full bg-white/25 rounded-full h-2 overflow-hidden"><div className="h-2 bg-white rounded-full" style={{ width: `${s.percent}%` }} /></div>
                </div>
              );
            })}
          </div>

          {weakest && <p className="mt-5 text-slate-700">Почни з предмета: <b>{SUBJECT_DETAILS[weakest.subject].title}</b> ({weakest.percent}%).</p>}
          <p className="text-xs text-slate-500 mt-2">Помилки автоматично потрапили в Банк помилок.</p>

          <div className="flex flex-wrap gap-3 justify-center mt-6">
            <Link href="/errors" className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold">Повторити помилки</Link>
            <button onClick={() => { setRun(null); setResult(null); }} className="px-5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold">Новий пробник</button>
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
                  {(!q.questionType || q.questionType === "single_choice") ? (
                    <>
                      <p className="text-sm text-red-600">Твоя відповідь: {d.chosen === null ? "не відповів" : `${LETTERS[d.chosen]}. ${q.options[d.chosen]}`}</p>
                      <p className="text-sm text-green-700">Правильно: {LETTERS[d.correctIndex]}. {q.options[d.correctIndex]}</p>
                    </>
                  ) : (
                    <p className="text-sm text-red-600">Неправильна відповідь</p>
                  )}
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
        <QuestionRenderer
          questionType={(q.questionType ?? "single_choice") as QuestionType}
          options={q.options}
          metadata={q.metadata}
          answer={answers[q.id]}
          onChange={(v: FlexAnswer) => setAnswers((a) => ({ ...a, [q.id]: v }))}
        />
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
