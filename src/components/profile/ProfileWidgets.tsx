"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { TrendingUp, Clock, BarChart3 } from "lucide-react";

type T = { topicId: string; title: string; subject: string; percent: number; correct: number; total: number };
type Stats = { answers: number; strengths: T[]; traps: T[]; openErrors: number; streak: { current: number; longest: number }; lastTest: { kind: string; avgNmt: number | null; subjects: { subject: string; correct: number; total: number; nmtScore: number | null }[] } | null };

function List({ items, tone }: { items: T[]; tone: "green" | "red" }) {
  const c = tone === "green" ? "bg-green-50 border-green-200 text-green-800" : "bg-red-50 border-red-200 text-red-800";
  if (items.length === 0) return <p className="text-sm text-slate-500">Поки замало даних (потрібно ≥3 відповідей на тему).</p>;
  return (
    <ul className="space-y-2">
      {items.map((t) => (
        <li key={t.topicId} className={`flex justify-between items-center gap-3 px-3 py-2 rounded-xl border ${c}`}>
          <span className="text-sm font-medium">{t.title}</span>
          <span className="font-extrabold whitespace-nowrap">{t.percent}% <span className="text-xs font-normal opacity-70">({t.correct}/{t.total})</span></span>
        </li>
      ))}
    </ul>
  );
}

type ProbnikSession = {
  id: string; difficulty: number; correct: number; total: number; percent: number;
  nmtScore: number | null; subjectScores: { subject: string; correct: number; total: number; nmtScore: number | null; isPassed: boolean }[] | null;
  startedAt: string; finishedAt: string | null; durationMin: number | null;
};

const SUBJ_NAMES: Record<string, string> = { UKRAINIAN: "Укр", MATH: "Мат", HISTORY: "Іст", ENGLISH: "Англ" };
const DIFF_NAMES: Record<number, string> = { 1: "Легкий", 2: "Середній", 3: "Важкий" };

function ProbnikHistory() {
  const [data, setData] = useState<ProbnikSession[] | null>(null);
  useEffect(() => {
    fetch("/api/stats/probnik-history", { cache: "no-store" }).then((r) => r.ok ? r.json() : null).then((d) => setData(d?.sessions ?? [])).catch(() => setData([]));
  }, []);

  if (data === null) return <p className="text-slate-400 text-sm">Завантажую історію пробників…</p>;
  if (data.length === 0) return <p className="text-slate-500 text-sm">Ти ще не завершив жодного пробника. <Link href="/simulation" className="text-indigo-600 underline">Спробуй зараз!</Link></p>;

  // Progress graph — last 10 sessions NMT scores
  const graphData = data.filter(s => s.nmtScore !== null).slice(0, 10).reverse();
  const maxScore = 200;
  const minScore = 100;

  return (
    <div className="space-y-4">
      {/* Mini progress graph */}
      {graphData.length >= 2 && (
        <div className="rounded-2xl p-4 bg-white border border-slate-100 shadow-md">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-4 h-4 text-indigo-500" />
            <h3 className="text-sm font-bold text-slate-700">Прогрес (середній бал НМТ)</h3>
          </div>
          <div className="flex items-end gap-1 h-24">
            {graphData.map((s, i) => {
              const score = s.nmtScore ?? minScore;
              const pct = Math.max(5, ((score - minScore) / (maxScore - minScore)) * 100);
              const color = score >= 180 ? "bg-emerald-500" : score >= 160 ? "bg-indigo-500" : score >= 140 ? "bg-amber-500" : "bg-red-400";
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <span className="text-[10px] font-bold text-slate-500">{score}</span>
                  <div className={`w-full rounded-t-md ${color} transition-all`} style={{ height: `${pct}%` }} />
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Scrollable list */}
      <div className="max-h-80 overflow-y-auto space-y-2 pr-1">
        {data.map((s) => (
          <div key={s.id} className="p-4 rounded-2xl bg-white border border-slate-100 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-indigo-400" />
                <span className="font-bold text-lg text-slate-800">{s.nmtScore ?? "—"}</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">{DIFF_NAMES[s.difficulty] ?? "?"}</span>
              </div>
              <div className="text-right text-xs text-slate-400">
                {s.finishedAt && new Date(s.finishedAt).toLocaleDateString("uk-UA", { day: "numeric", month: "short" })}
                {s.durationMin !== null && <span className="ml-2 inline-flex items-center gap-0.5"><Clock className="w-3 h-3" />{s.durationMin} хв</span>}
              </div>
            </div>
            {Array.isArray(s.subjectScores) && (
              <div className="grid grid-cols-4 gap-1 text-xs">
                {s.subjectScores.map((sub) => (
                  <div key={sub.subject} className={`text-center px-1 py-1 rounded-lg ${sub.isPassed ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-600"}`}>
                    <span className="font-medium">{SUBJ_NAMES[sub.subject] ?? sub.subject}</span>
                    <span className="font-bold ml-1">{sub.nmtScore ?? "—"}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function ProfileWidgets() {
  const [s, setS] = useState<Stats | null>(null);

  useEffect(() => {
    fetch("/api/stats/weekly", { cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).then(setS).catch(() => {});
  }, []);

  if (!s) return <p className="text-slate-400 text-sm mb-8">Завантажую статистику…</p>;

  return (
    <div className="space-y-4 mb-8">
      <div className="rounded-3xl p-5 text-white shadow-xl bg-gradient-to-br from-orange-500 to-rose-600 flex items-center justify-between">
        <div>
          <p className="text-sm text-white/80">Daily Streak</p>
          <p className="text-5xl font-extrabold">🔥 {s.streak.current} <span className="text-lg font-semibold">{s.streak.current === 1 ? "день" : "днів"}</span></p>
          <p className="text-sm text-white/80 mt-1">Рекорд: {s.streak.longest}. Відповідай хоча б на 1 питання щодня.</p>
        </div>
        <Link href="/errors" className="text-center bg-white/20 hover:bg-white/30 transition rounded-2xl px-4 py-3">
          <p className="text-3xl font-extrabold">{s.openErrors}</p>
          <p className="text-xs">помилок у банку</p>
        </Link>
      </div>

      {s.lastTest && (
        <div className="rounded-3xl p-5 bg-white border border-slate-100 shadow-md">
          <h2 className="text-lg font-bold text-slate-800 mb-1">Останній тест ({s.lastTest.kind === "SIMULATION" ? "пробник" : "діагностика"})</h2>
          <p className="text-sm text-slate-600 mb-3">Орієнтовний бал НМТ: <span className="font-extrabold text-violet-600 text-xl">{s.lastTest.avgNmt ?? "поріг не подолано"}</span></p>
          <div className="grid grid-cols-2 gap-2 text-sm">
            {s.lastTest.subjects.map((x) => (
              <div key={x.subject} className="px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 flex justify-between">
                <span>{{ UKRAINIAN: "Українська", MATH: "Математика", HISTORY: "Історія", ENGLISH: "Англійська" }[x.subject] ?? x.subject}</span>
                <span className="font-bold">{x.nmtScore ?? "—"}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="rounded-3xl p-5 bg-white border border-slate-100 shadow-md">
        <h2 className="text-lg font-bold text-slate-800 mb-3">Історія пробників НМТ</h2>
        <ProbnikHistory />
      </div>

      <div className="rounded-3xl p-5 bg-white border border-slate-100 shadow-md">
        <h2 className="text-lg font-bold text-slate-800 mb-1">Аналітика за 7 днів</h2>
        <p className="text-xs text-slate-500 mb-4">Відповідей за тиждень: {s.answers}</p>
        <p className="font-bold text-green-700 mb-2">🟢 Сильні сторони (&gt;80%)</p>
        <List items={s.strengths} tone="green" />
        <p className="font-bold text-red-700 mt-5 mb-2">🔴 Пастки / Слабкі теми (&lt;60%)</p>
        <List items={s.traps} tone="red" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-sm font-semibold">
        {[["/errors", "Банк помилок"], ["/diagnostic", "Діагностика"], ["/simulation", "Пробник НМТ"], ["/materials", "Матеріали"]].map(([href, label]) => (
          <Link key={href} href={href} className="px-3 py-3 rounded-xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition">{label}</Link>
        ))}
      </div>
    </div>
  );
}
