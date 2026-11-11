// Приводить питання з контенту до внутрішнього формату БД.
// Підтримує два формати JSON:
//  • внутрішній: { questionType, options, correctIndex, metadata }
//  • «формат УЦОЯО» (ТЗ): { type, left/right/correctMapping, items/correctOrder, options[{id,text}]/correctAnswers, correctAnswer }
// Повертає { q } або { error }.

const UA = ["А", "Б", "В", "Г", "Д", "Е", "Є"];
const LAT = ["A", "B", "C", "D", "E", "F", "G"];

const letterIndex = (v) => {
  const s = String(v ?? "").trim().toUpperCase();
  let i = UA.indexOf(s);
  if (i < 0) i = LAT.indexOf(s);
  if (i < 0 && /^\d+$/.test(s)) i = Number(s) - 1; // "1" → 0
  return i;
};

export function parseNumber(v) {
  if (typeof v === "number") return v;
  const s = String(v ?? "").replace(/\s+/g, "").replace(/[−–—]/g, "-").replace(",", ".");
  if (!/^[-+]?(\d+\.?\d*|\.\d+)$/.test(s)) return null;
  return Number(s);
}

const TYPE_ALIASES = {
  single_choice: "single_choice", single: "single_choice",
  matching: "matching",
  sequence: "sequencing", sequencing: "sequencing",
  multiple_choice_3_of_7: "choose_multi", choose_multi: "choose_multi", choose_3_of_7: "choose_multi",
  fill_blanks: "fill_blanks",
  short_answer: "short_answer",
};

export function normalizeQuestion(raw) {
  const q = { ...raw };
  const type = TYPE_ALIASES[q.questionType ?? q.type ?? "single_choice"];
  if (!type) return { error: `невідомий тип ${q.questionType ?? q.type}` };
  q.questionType = type;
  delete q.type;
  if (q.testLevel === undefined) q.testLevel = q.level ?? q.difficulty;
  if (q.text === undefined) q.text = q.question;

  if (type === "single_choice") {
    if (!Number.isInteger(q.correctIndex) && q.correctAnswer !== undefined && Array.isArray(q.options)) {
      let i = q.options.indexOf(q.correctAnswer);
      if (i < 0) i = letterIndex(q.correctAnswer);
      q.correctIndex = i;
    }
  } else if (type === "matching" && !q.metadata && Array.isArray(q.left) && Array.isArray(q.right) && q.correctMapping) {
    const used = new Set();
    const pairs = [];
    for (let i = 0; i < q.left.length; i++) {
      const r = letterIndex(q.correctMapping[String(i + 1)] ?? q.correctMapping[i]);
      if (r < 0 || r >= q.right.length) return { error: `matching: немає відповіді для ${i + 1}` };
      used.add(r);
      pairs.push([q.left[i], q.right[r]]);
    }
    q.metadata = { pairs, distractors: q.right.filter((_, i) => !used.has(i)) };
  } else if (type === "sequencing" && !q.metadata && Array.isArray(q.items) && Array.isArray(q.correctOrder)) {
    const ids = q.items.map((it) => String(it.id ?? "").trim().toUpperCase());
    const correctOrder = q.correctOrder.map((id) => ids.indexOf(String(id).trim().toUpperCase()));
    if (correctOrder.some((i) => i < 0)) return { error: "sequence: correctOrder містить невідомий id" };
    q.metadata = { items: q.items.map((it) => it.text), correctOrder };
  } else if (type === "choose_multi" && !q.metadata && Array.isArray(q.options) && Array.isArray(q.correctAnswers)) {
    const opts = q.options.map((o, i) => (typeof o === "string" ? { id: i + 1, text: o } : o)).sort((a, b) => a.id - b.id);
    const correctIndices = q.correctAnswers.map((id) => opts.findIndex((o) => Number(o.id) === Number(id)));
    if (correctIndices.some((i) => i < 0)) return { error: "3 з 7: correctAnswers містить невідомий номер" };
    q.options = opts.map((o) => o.text);
    q.metadata = { correctIndices: correctIndices.sort((a, b) => a - b), requiredCount: correctIndices.length };
  } else if (type === "short_answer" && !q.metadata && q.correctAnswer !== undefined) {
    const n = parseNumber(q.correctAnswer);
    q.metadata = { answer: n ?? String(q.correctAnswer).trim() };
  }

  if (type !== "single_choice" && type !== "choose_multi") q.options = q.options ?? [];
  if (type !== "single_choice") q.correctIndex = 0;
  for (const k of ["left", "right", "correctMapping", "items", "correctOrder", "correctAnswers", "correctAnswer", "level", "difficulty", "question"]) delete q[k];
  if (!q.explanation) q.explanation = "";
  return { q };
}

// Postgres jsonb переставляє ключі, тому серіалізуємо зі стабільним порядком.
const stable = (v) => Array.isArray(v) ? "[" + v.map(stable).join(",") + "]"
  : v && typeof v === "object" ? "{" + Object.keys(v).sort().map((k) => JSON.stringify(k) + ":" + stable(v[k])).join(",") + "}"
  : JSON.stringify(v ?? null);

/**
 * Ключ дублікату — однаковий для JSON і для рядка з БД.
 * Для нових типів береться «незмінна частина» (ліва колонка / події / варіанти), тож виправлення
 * відповідей чи зайвих варіантів оновлює наявне питання, а не створює копію.
 */
export function questionKey(q) {
  const t = q.questionType ?? "single_choice";
  const m = q.metadata ?? {};
  const sorted = (a) => stable([...(a ?? [])].map(String).sort());
  let core;
  if (t === "single_choice") return q.text + "\u0001" + [...(q.options ?? [])].sort().join("|");
  else if (t === "matching") core = sorted((m.pairs ?? []).map((p) => p[0]));
  else if (t === "sequencing") core = sorted(m.items);
  else if (t === "choose_multi") core = sorted(q.options);
  else core = "";
  return q.text + "\u0001" + t + "\u0001" + core;
}

export const sameMeta = (a, b) => stable(a) === stable(b);
