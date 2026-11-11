"use client";

import { useState, useCallback } from "react";
import { ArrowUp, ArrowDown, GripVertical } from "lucide-react";
import type { QuestionType, MatchingMeta, SequencingMeta, ChooseMultiMeta, FillBlanksMeta } from "@/types";

/* ────── answer format per type ──────
 *  single_choice → number (option index)
 *  matching      → number[] (right-side index for each left item; [-1] = not matched)
 *  sequencing    → number[] (indices in user-chosen order)
 *  choose_multi  → number[] (selected option indices, sorted)
 *  fill_blanks   → string[] (one per blank)
 *  short_answer  → string
 */
export type FlexAnswer = any;

const LETTERS = ["А", "Б", "В", "Г", "Д", "Е", "Є"];

/* ───── props ───── */
interface Props {
  questionType: QuestionType;
  options: string[];
  metadata: any;
  answer: FlexAnswer | undefined;
  onChange: (v: FlexAnswer) => void;
}

/* ═══════ SINGLE CHOICE ═══════ */
function SingleChoice({ options, answer, onChange }: { options: string[]; answer: number | undefined; onChange: (v: number) => void }) {
  return (
    <div className="space-y-3">
      {options.map((opt, i) => {
        const selected = answer === i;
        return (
          <button key={i} onClick={() => onChange(i)} className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${selected ? "bg-indigo-600 text-white border-indigo-600 shadow-md" : "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300"}`}>
            <span className={`font-bold ${selected ? "text-white" : "text-slate-400"}`}>{LETTERS[i]}</span>
            <span>{opt}</span>
          </button>
        );
      })}
    </div>
  );
}

/* ═══════ MATCHING ═══════ */
function Matching({ metadata, answer, onChange }: { metadata: MatchingMeta; answer: number[] | undefined; onChange: (v: number[]) => void }) {
  const pairs = metadata.pairs;
  const leftItems = pairs.map(p => p[0]);
  const rightItems = pairs.map(p => p[1]);
  // Shuffled right side (stable via metadata — but we shuffle once)
  const [shuffledRight] = useState(() => {
    const indices = rightItems.map((_, i) => i);
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    return indices;
  });
  const current = answer ?? leftItems.map(() => -1);
  const [activeLeft, setActiveLeft] = useState<number | null>(null);

  const handleRightClick = useCallback((rightOrigIdx: number) => {
    if (activeLeft === null) return;
    const next = [...current];
    // Clear any previous assignment of this right item
    const prevLeft = next.indexOf(rightOrigIdx);
    if (prevLeft !== -1) next[prevLeft] = -1;
    next[activeLeft] = rightOrigIdx;
    setActiveLeft(null);
    onChange(next);
  }, [activeLeft, current, onChange]);

  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-500">Натисни ліву частину, потім праву, щоб з&apos;єднати пару</p>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          {leftItems.map((item, i) => {
            const isActive = activeLeft === i;
            const matched = current[i] !== -1;
            return (
              <button key={i} onClick={() => setActiveLeft(i)} className={`w-full text-left px-3 py-2.5 rounded-xl border text-sm transition ${isActive ? "bg-indigo-100 border-indigo-400 ring-2 ring-indigo-300" : matched ? "bg-emerald-50 border-emerald-300" : "bg-slate-50 border-slate-200 hover:border-indigo-200"}`}>
                <span className="font-bold text-slate-400 mr-2">{i + 1}.</span>
                {item}
                {matched && <span className="float-right text-emerald-600 text-xs font-bold">→ {LETTERS[shuffledRight.indexOf(current[i])]}</span>}
              </button>
            );
          })}
        </div>
        <div className="space-y-2">
          {shuffledRight.map((origIdx, dispIdx) => {
            const used = current.includes(origIdx);
            return (
              <button key={dispIdx} onClick={() => handleRightClick(origIdx)} className={`w-full text-left px-3 py-2.5 rounded-xl border text-sm transition ${used ? "bg-emerald-50 border-emerald-300 opacity-60" : activeLeft !== null ? "bg-white border-indigo-200 hover:bg-indigo-50 cursor-pointer" : "bg-slate-50 border-slate-200"}`}>
                <span className="font-bold text-slate-400 mr-2">{LETTERS[dispIdx]}</span>
                {rightItems[origIdx]}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ═══════ SEQUENCING ═══════ */
function Sequencing({ metadata, answer, onChange }: { metadata: SequencingMeta; answer: number[] | undefined; onChange: (v: number[]) => void }) {
  const items = metadata.items;
  // Start with shuffled order
  const [initial] = useState(() => {
    const arr = items.map((_, i) => i);
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  });
  const order = answer ?? initial;

  const move = useCallback((from: number, dir: -1 | 1) => {
    const to = from + dir;
    if (to < 0 || to >= order.length) return;
    const next = [...order];
    [next[from], next[to]] = [next[to], next[from]];
    onChange(next);
  }, [order, onChange]);

  return (
    <div className="space-y-2">
      <p className="text-sm text-slate-500">Розташуй у правильній послідовності (використовуй стрілки)</p>
      {order.map((itemIdx, pos) => (
        <div key={itemIdx} className="flex items-center gap-2 px-3 py-2.5 rounded-xl border bg-white border-slate-200 shadow-sm">
          <GripVertical className="w-4 h-4 text-slate-300 flex-shrink-0" />
          <span className="font-bold text-indigo-500 mr-1">{pos + 1}.</span>
          <span className="flex-1 text-sm">{items[itemIdx]}</span>
          <button onClick={() => move(pos, -1)} disabled={pos === 0} className="p-1 rounded hover:bg-slate-100 disabled:opacity-30"><ArrowUp className="w-4 h-4" /></button>
          <button onClick={() => move(pos, 1)} disabled={pos === order.length - 1} className="p-1 rounded hover:bg-slate-100 disabled:opacity-30"><ArrowDown className="w-4 h-4" /></button>
        </div>
      ))}
    </div>
  );
}

/* ═══════ CHOOSE MULTI (3 of 7) ═══════ */
function ChooseMulti({ options, metadata, answer, onChange }: { options: string[]; metadata: ChooseMultiMeta; answer: number[] | undefined; onChange: (v: number[]) => void }) {
  const required = metadata.requiredCount;
  const selected = answer ?? [];

  const toggle = useCallback((idx: number) => {
    let next: number[];
    if (selected.includes(idx)) {
      next = selected.filter(x => x !== idx);
    } else {
      if (selected.length >= required) return; // max reached
      next = [...selected, idx].sort((a, b) => a - b);
    }
    onChange(next);
  }, [selected, required, onChange]);

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-500">Обери {required} з {options.length} варіантів</p>
      {options.map((opt, i) => {
        const isSelected = selected.includes(i);
        const maxReached = selected.length >= required && !isSelected;
        return (
          <button key={i} onClick={() => toggle(i)} disabled={maxReached} className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 ${isSelected ? "bg-indigo-600 text-white border-indigo-600 shadow-md" : maxReached ? "bg-slate-100 border-slate-200 opacity-50 cursor-not-allowed" : "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300"}`}>
            <span className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 mt-0.5 ${isSelected ? "bg-white border-white" : "border-slate-300"}`}>
              {isSelected && <span className="text-indigo-600 text-xs font-bold">✓</span>}
            </span>
            <span>{opt}</span>
          </button>
        );
      })}
      <p className="text-xs text-slate-400 text-center">Обрано: {selected.length} / {required}</p>
    </div>
  );
}

/* ═══════ FILL BLANKS ═══════ */
function FillBlanks({ metadata, answer, onChange }: { metadata: FillBlanksMeta; answer: string[] | undefined; onChange: (v: string[]) => void }) {
  const blanks = metadata.blanks;
  const values = answer ?? blanks.map(() => "");

  const handleChange = useCallback((idx: number, val: string) => {
    const next = [...values];
    next[idx] = val;
    onChange(next);
  }, [values, onChange]);

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-500">Заповни пропуски</p>
      {blanks.map((_, i) => (
        <div key={i} className="flex items-center gap-3">
          <span className="font-bold text-indigo-500 text-sm">{i + 1}.</span>
          <input
            type="text"
            value={values[i] ?? ""}
            onChange={(e) => handleChange(i, e.target.value)}
            placeholder={`Пропуск ${i + 1}`}
            className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 outline-none text-sm transition"
          />
        </div>
      ))}
    </div>
  );
}

/* ═══════ SHORT ANSWER ═══════ */
function ShortAnswer({ answer, onChange }: { answer: string | undefined; onChange: (v: string) => void }) {
  return (
    <div className="space-y-2">
      <p className="text-sm text-slate-500">Введи відповідь (число або текст)</p>
      <input
        type="text"
        value={answer ?? ""}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Твоя відповідь…"
        className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 outline-none text-base transition"
      />
    </div>
  );
}

/* ═══════ MAIN RENDERER ═══════ */
export default function QuestionRenderer({ questionType, options, metadata, answer, onChange }: Props) {
  switch (questionType) {
    case "matching":
      return <Matching metadata={metadata as MatchingMeta} answer={answer} onChange={onChange} />;
    case "sequencing":
      return <Sequencing metadata={metadata as SequencingMeta} answer={answer} onChange={onChange} />;
    case "choose_multi":
      return <ChooseMulti options={options} metadata={metadata as ChooseMultiMeta} answer={answer} onChange={onChange} />;
    case "fill_blanks":
      return <FillBlanks metadata={metadata as FillBlanksMeta} answer={answer} onChange={onChange} />;
    case "short_answer":
      return <ShortAnswer answer={answer} onChange={onChange} />;
    default:
      return <SingleChoice options={options} answer={answer} onChange={onChange} />;
  }
}
