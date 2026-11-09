"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

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
          <h2 className="text-lg font-bold text-slate-800 mb-1">Останній тест ({s.lastTest.kind === "SIMULATION" ? "симуляція" : "діагностика"})</h2>
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
        <h2 className="text-lg font-bold text-slate-800 mb-1">Аналітика за 7 днів</h2>
        <p className="text-xs text-slate-500 mb-4">Відповідей за тиждень: {s.answers}</p>
        <p className="font-bold text-green-700 mb-2">🟢 Сильні сторони (&gt;80%)</p>
        <List items={s.strengths} tone="green" />
        <p className="font-bold text-red-700 mt-5 mb-2">🔴 Пастки / Слабкі теми (&lt;60%)</p>
        <List items={s.traps} tone="red" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-sm font-semibold">
        {[["/errors", "Банк помилок"], ["/diagnostic", "Діагностика"], ["/simulation", "Симуляція НМТ"], ["/materials", "Матеріали"]].map(([href, label]) => (
          <Link key={href} href={href} className="px-3 py-3 rounded-xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition">{label}</Link>
        ))}
      </div>
    </div>
  );
}
