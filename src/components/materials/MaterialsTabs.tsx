"use client";

import { useState } from "react";
import { MATERIALS } from "@/lib/materials";
import { SUBJECT_DETAILS, SUBJECT_ORDER, type Subject } from "@/types";

export default function MaterialsTabs() {
  const [subject, setSubject] = useState<Subject>("UKRAINIAN");
  const [query, setQuery] = useState("");
  const theme = SUBJECT_DETAILS[subject];
  const q = query.trim().toLowerCase();

  const sections = MATERIALS[subject]
    .map((sec) => ({ ...sec, rows: q ? sec.rows.filter((r) => r.some((c) => c.toLowerCase().includes(q))) : sec.rows }))
    .filter((sec) => sec.rows.length > 0);

  return (
    <div className="mt-6">
      <div className="flex flex-wrap gap-2 mb-4">
        {SUBJECT_ORDER.map((s) => {
          const th = SUBJECT_DETAILS[s];
          const active = s === subject;
          return (
            <button
              key={s}
              onClick={() => setSubject(s)}
              className={`px-4 py-2 rounded-full text-sm font-bold transition ${active ? `bg-gradient-to-r ${th.gradient} text-white shadow-md` : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"}`}
            >
              {th.title}
            </button>
          );
        })}
      </div>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Пошук по таблицях…"
        className="w-full mb-5 px-4 py-2 rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-300"
      />

      {sections.length === 0 && <p className="text-slate-500 text-center py-8">Нічого не знайдено.</p>}

      <div className="space-y-6">
        {sections.map((sec) => (
          <section key={sec.title} className="rounded-3xl bg-white border border-slate-100 shadow-md overflow-hidden">
            <div className={`px-5 py-3 text-white font-bold bg-gradient-to-r ${theme.gradient}`}>{sec.title}</div>
            {sec.note && <p className="px-5 pt-3 text-xs text-slate-500">{sec.note}</p>}
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-500 border-b border-slate-100">
                    {sec.columns.map((c) => (
                      <th key={c} className="px-5 py-2 font-semibold">{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {sec.rows.map((r, i) => (
                    <tr key={i} className="border-b border-slate-50 last:border-0 odd:bg-slate-50/50 align-top">
                      {r.map((c, j) => (
                        <td key={j} className={`px-5 py-2 ${j === 0 ? "font-semibold text-slate-800 whitespace-nowrap" : "text-slate-700"}`}>{c}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
