"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import Link from "next/link";
import { useSession } from "next-auth/react";
import { CheckCircle2, Lightbulb, X, XCircle } from "lucide-react";
import ZoomImage from "@/components/shared/ZoomImage";

const LETTERS = ["А", "Б", "В", "Г", "Д"];

type Q = { id: string; text: string; options: string[]; imageUrl?: string | null };
type Answered = { chosen: number | null; isCorrect: boolean; correctIndex: number; explanation: string | null };

export default function DailyQuestion() {
  const { status } = useSession();
  const [q, setQ] = useState<Q | null>(null);
  const [res, setRes] = useState<(Answered & { streak: number }) | null>(null);
  const [streak, setStreak] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (status === "loading") return;
    fetch("/api/daily", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (!d) return;
        setQ(d.question);
        setStreak(d.streak ?? 0);
        if (d.answered) setRes({ ...d.answered, streak: d.streak ?? 0 });
      })
      .catch(() => {});
  }, [status]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    document.addEventListener("keydown", onKey);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = previousOverflow;
    };
  }, [open]);

  if (!q) return null;

  const answer = async (i: number) => {
    if (res || busy) return;
    setBusy(true);
    setError("");
    try {
      const r = await fetch("/api/daily", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ chosen: i }) });
      if (!r.ok) throw new Error();
      const d = await r.json();
      setRes({ chosen: i, isCorrect: d.correct, correctIndex: d.correctIndex, explanation: d.explanation, streak: d.streak });
      setStreak(d.streak);
    } catch {
      setError("Не вдалось зберегти відповідь.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <div className="flex justify-center">
        {res ? (
          <button
            onClick={() => setOpen(true)}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50 text-emerald-700 text-sm font-semibold border border-emerald-200"
          >
            <CheckCircle2 className="w-4 h-4" /> Питання дня виконано · 🔥 {streak}
          </button>
        ) : (
          <button
            onClick={() => setOpen(true)}
            aria-label="Відкрити питання дня"
            className="group relative inline-flex items-center gap-3 px-6 py-3 rounded-full bg-gradient-to-r from-orange-500 to-pink-600 text-white font-extrabold shadow-lg shadow-orange-400/50 hover:scale-105 transition"
          >
            <span className="absolute inset-0 rounded-full bg-orange-400/60 animate-ping" aria-hidden />
            <span className="relative text-2xl animate-pulse">🔥</span>
            <span className="relative">Питання дня</span>
          </button>
        )}
      </div>

      {open && createPortal(
        <div role="dialog" aria-modal="true" aria-label="Питання дня" className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-3 bg-black/55 backdrop-blur-sm" onClick={() => setOpen(false)}>
          <div className="w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-3xl bg-white shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="px-5 py-3 flex justify-between items-center text-white font-bold bg-gradient-to-r from-violet-600 to-pink-500 rounded-t-3xl">
              <span>🎯 Питання дня · 🔥 {streak}</span>
              <button onClick={() => setOpen(false)} aria-label="Закрити" className="p-1 rounded-full hover:bg-white/20"><X className="w-5 h-5" /></button>
            </div>
            <div className="p-5">
              {q.imageUrl && <div className="flex justify-center mb-4"><ZoomImage src={q.imageUrl} className="max-h-60" /></div>}
              <p className="text-lg font-semibold text-slate-900 mb-4">{q.text}</p>
              <div className="space-y-2">
                {q.options.map((opt, i) => {
                  let cls = "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300";
                  if (res) cls = i === res.correctIndex ? "bg-green-50 border-green-500 text-green-900" : i === res.chosen ? "bg-red-50 border-red-400 text-red-900" : "bg-slate-50 border-slate-200 opacity-60";
                  return (
                    <button key={i} onClick={() => answer(i)} disabled={!!res || busy || status === "unauthenticated"} className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${cls}`}>
                      <span className="font-bold text-slate-400">{LETTERS[i]}</span>
                      <span>{opt}</span>
                    </button>
                  );
                })}
              </div>

              {status === "unauthenticated" && (
                <p className="text-sm text-slate-500 mt-3"><Link href="/login" className="text-indigo-600 underline">Увійди</Link>, щоб відповісти й вести серію 🔥</p>
              )}
              {error && <p className="text-red-500 text-sm mt-3">{error}</p>}

              {res && (
                <div className="mt-4 rounded-2xl border border-slate-200 overflow-hidden">
                  <div className={`px-4 py-2 flex items-center gap-2 font-bold ${res.isCorrect ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
                    {res.isCorrect ? <CheckCircle2 className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
                    {res.isCorrect ? "Правильно!" : "Неправильно"} · серія 🔥 {res.streak}
                  </div>
                  <div className="p-4 text-sm text-slate-700">
                    <p className="flex items-center gap-2 font-bold text-amber-700 mb-1"><Lightbulb className="w-4 h-4" /> Обґрунтування</p>
                    {res.explanation ?? "Обґрунтування ще не додано."}
                    {!res.isCorrect && <p className="text-green-700 mt-2">Правильно: {LETTERS[res.correctIndex]}. {q.options[res.correctIndex]}</p>}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>,
        document.body
      )}
    </>
  );
}
