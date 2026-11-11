"use client";

import { useState, useCallback, useMemo } from "react";
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

/* ═══════ Спільна сітка «рядки × літери» як у бланку НМТ ═══════ */
function AnswerGrid({ rows, cols, value, onPick }: { rows: string[]; cols: number; value: number[]; onPick: (row: number, col: number) => void }) {
  return (
    <div className="overflow-x-auto">
      <table className="mx-auto border-separate border-spacing-1">
        <thead>
          <tr>
            <th />
            {Array.from({ length: cols }, (_, c) => (
              <th key={c} className="w-10 text-center text-sm font-bold text-slate-500">{LETTERS[c]}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((label, r) => (
            <tr key={r}>
              <th className="pr-2 text-right text-sm font-bold text-slate-500 whitespace-nowrap">{label}</th>
              {Array.from({ length: cols }, (_, c) => {
                const on = value[r] === c;
                return (
                  <td key={c}>
                    <button
                      type="button"
                      aria-label={`${label} — ${LETTERS[c]}`}
                      aria-pressed={on}
                      onClick={() => onPick(r, c)}
                      className={`w-10 h-10 rounded-lg border-2 transition flex items-center justify-center ${on ? "bg-indigo-600 border-indigo-600 text-white" : "bg-white border-slate-300 hover:border-indigo-400"}`}
                    >
                      {on && <span className="text-sm font-bold">✕</span>}
                    </button>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// У кожному стовпчику може бути лише одна позначка (як у бланку НМТ)
const pickUnique = (cur: number[], row: number, col: number) => {
  const next = cur.map((v) => (v === col ? -1 : v));
  next[row] = cur[row] === col ? -1 : col;
  return next;
};

/* ═══════ MATCHING ═══════ */
function Matching({ metadata, answer, onChange }: { metadata: MatchingMeta; answer: number[] | undefined; onChange: (v: number[]) => void }) {
  const pairs = metadata.pairs;
  const leftItems = pairs.map((p) => p[0]);
  // Права колонка: правильні відповіді + зайві варіанти (як А–Д на НМТ); індекс ≥ pairs.length — дистрактор
  const rightItems = [...pairs.map((p) => p[1]), ...(metadata.distractors ?? [])];
  const [shuffledRight] = useState(() => {
    const idx = rightItems.map((_, i) => i);
    for (let i = idx.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [idx[i], idx[j]] = [idx[j], idx[i]];
    }
    return idx;
  });
  // answer[i] — початковий індекс правого варіанта; у сітці зберігаємо позицію літери
  const current = answer ?? leftItems.map(() => -1);
  const asCols = current.map((orig) => (orig < 0 ? -1 : shuffledRight.indexOf(orig)));
  const L = metadata.leftLabels?.[0];
  const R = metadata.rightLabels?.[0];

  return (
    <div className="space-y-4">
      <div className="grid sm:grid-cols-2 gap-4">
        <div className="space-y-2">
          {L && <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{L}</p>}
          {leftItems.map((item, i) => (
            <div key={i} className="flex gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-sm">
              <span className="font-bold text-indigo-500">{i + 1}</span>
              <span>{item}</span>
            </div>
          ))}
        </div>
        <div className="space-y-2">
          {R && <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{R}</p>}
          {shuffledRight.map((orig, d) => (
            <div key={d} className="flex gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-sm">
              <span className="font-bold text-indigo-500">{LETTERS[d]}</span>
              <span>{rightItems[orig]}</span>
            </div>
          ))}
        </div>
      </div>
      <p className="text-sm text-slate-500 text-center">Познач відповідність у таблиці: рядок — цифра, стовпчик — літера</p>
      <AnswerGrid
        rows={leftItems.map((_, i) => String(i + 1))}
        cols={rightItems.length}
        value={asCols}
        onPick={(r, c) => onChange(pickUnique(asCols, r, c).map((col) => (col < 0 ? -1 : shuffledRight[col])))}
      />
    </div>
  );
}

/* ═══════ SEQUENCING ═══════ */
function Sequencing({ metadata, answer, onChange }: { metadata: SequencingMeta; answer: number[] | undefined; onChange: (v: number[]) => void }) {
  const items = metadata.items;
  // answer[pos] — індекс події (літери), яку учень поставив на позицію pos
  const current = answer ?? items.map(() => -1);
  return (
    <div className="space-y-4">
      <div className="space-y-2">
        {items.map((item, i) => (
          <div key={i} className="flex gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-sm">
            <span className="font-bold text-indigo-500">{LETTERS[i]}</span>
            <span>{item}</span>
          </div>
        ))}
      </div>
      <p className="text-sm text-slate-500 text-center">Для кожної позиції (1 — найраніша) познач літеру події</p>
      <AnswerGrid rows={items.map((_, i) => `${i + 1}`)} cols={items.length} value={current} onPick={(r, c) => onChange(pickUnique(current, r, c))} />
    </div>
  );
}

/* ═══════ CHOOSE MULTI (3 of 7) ═══════ */
function ChooseMulti({ options, metadata, answer, onChange }: { options: string[]; metadata: ChooseMultiMeta; answer: number[] | undefined; onChange: (v: number[]) => void }) {
  const required = metadata.requiredCount;
  const selected = useMemo(() => answer ?? [], [answer]);

  const toggle = useCallback((idx: number) => {
    let next: number[];
    if (selected.includes(idx)) {
      next = selected.filter((x) => x !== idx);
    } else {
      if (selected.length >= required) return; // після 3-го вибору решта блокується
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
          <button key={i} type="button" role="checkbox" aria-checked={isSelected} onClick={() => toggle(i)} disabled={maxReached} className={`w-full text-left px-4 py-3 rounded-xl border transition flex gap-3 items-start ${isSelected ? "bg-indigo-600 text-white border-indigo-600 shadow-md" : maxReached ? "bg-slate-100 border-slate-200 opacity-50 cursor-not-allowed" : "bg-slate-50 border-slate-200 hover:bg-white hover:border-indigo-300"}`}>
            <span className={`w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 text-xs font-bold ${isSelected ? "bg-white border-white text-indigo-600" : "border-slate-300 text-slate-500"}`}>
              {isSelected ? "✓" : i + 1}
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
      <p className="text-sm text-slate-500">Запиши відповідь числом (десятковий дріб — через кому або крапку)</p>
      <input
        type="text"
        inputMode="decimal"
        autoComplete="off"
        value={answer ?? ""}
        onChange={(e) => onChange(e.target.value.replace(/[^0-9.,\-−\s/]/g, "").slice(0, 30))}
        placeholder="Наприклад: −3,5"
        className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 outline-none text-lg font-mono transition"
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
