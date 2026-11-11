// Перевірка файлів content/: node scripts/validate-content.mjs
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";

const root = new URL("../content", import.meta.url).pathname;
const files = [];
(function walk(d) {
  for (const n of readdirSync(d)) {
    const f = join(d, n);
    statSync(f).isDirectory() ? walk(f) : n.endsWith(".json") && files.push(f);
  }
})(root);

let bad = 0, total = 0;
const perTopic = new Map(); // "SUBJECT|topic" -> [n1, n2, n3]
const seenTopic = new Map(); // дублі між файлами однієї теми
for (const f of files) {
  const d = JSON.parse(readFileSync(f, "utf-8"));
  const tk = d.subject + "|" + d.topic;
  if (!seenTopic.has(tk)) seenTopic.set(tk, new Set());
  const seen = seenTopic.get(tk);
  if (!perTopic.has(tk)) perTopic.set(tk, [0, 0, 0]);
  d.questions.forEach((q, i) => {
    total++;
    const err = (m) => { bad++; console.log(`✗ ${f.split("/").pop()} #${i + 1}: ${m}`); };
    if (!q.text) err("немає тексту");
    if (q.image) {
      const p = new URL("../public" + q.image, import.meta.url).pathname;
      if (!existsSync(p)) err("немає файлу зображення " + q.image);
    }
    if ([1, 2, 3].includes(q.testLevel)) perTopic.get(tk)[q.testLevel - 1]++;
    const qt = q.questionType || "single_choice";
    const m = q.metadata || {};
    const key = q.text + "\u0001" + (qt === "single_choice" ? [...(q.options || [])].sort().join("|") : JSON.stringify(m));
    if (seen.has(key)) err("дубль");
    seen.add(key);
    if (![1, 2, 3].includes(q.testLevel)) err("testLevel");
    if (!q.explanation || q.explanation.length < (qt === "short_answer" ? 10 : 30)) err("коротке/відсутнє explanation");
    if (qt === "single_choice") {
      if (!Array.isArray(q.options) || q.options.length < 2 || q.options.length > 5) err("кількість варіантів");
      else {
        if (new Set(q.options).size !== q.options.length) err("однакові варіанти");
        if (!(q.correctIndex >= 0 && q.correctIndex < q.options.length)) err("correctIndex");
      }
      if (!(d.legacy) && (!/💡/.test(q.explanation || "") || !/❌/.test(q.explanation || "") || !/✅/.test(q.explanation || ""))) err("explanation без 💡/❌/✅");
    } else if (qt === "matching") {
      const p = m.pairs;
      if (!Array.isArray(p) || p.length < 3 || p.length > 5 || !p.every((x) => Array.isArray(x) && x.length === 2 && x[0] && x[1])) err("matching: pairs");
      else if (new Set(p.map((x) => x[1])).size !== p.length || new Set(p.map((x) => x[0])).size !== p.length) err("matching: однакові частини");
    } else if (qt === "sequencing") {
      const it = m.items, co = m.correctOrder;
      if (!Array.isArray(it) || it.length < 3 || !Array.isArray(co) || co.length !== it.length || [...co].sort((a, b) => a - b).some((v, k) => v !== k)) err("sequencing: items/correctOrder");
    } else if (qt === "choose_multi") {
      const ci = m.correctIndices;
      if (!Array.isArray(q.options) || q.options.length !== 7 || new Set(q.options).size !== 7) err("choose_multi: потрібно 7 різних варіантів");
      if (!Array.isArray(ci) || ci.length !== m.requiredCount || new Set(ci).size !== ci.length || ci.some((v) => !(v >= 0 && v < 7))) err("choose_multi: correctIndices");
    } else if (qt === "fill_blanks") {
      const b = m.blanks;
      const gaps = (q.text.match(/\(\d+\)_{2,}/g) || []).length;
      if (!Array.isArray(b) || !b.length || !b.every((x) => x && typeof x.answer === "string" && x.answer.trim())) err("fill_blanks: blanks");
      else if (gaps !== b.length) err(`fill_blanks: у тексті ${gaps} пропусків, а blanks ${b.length}`);
    } else if (qt === "short_answer") {
      if (!(typeof m.answer === "number" || (typeof m.answer === "string" && m.answer.trim()))) err("short_answer: answer");
    } else err("невідомий questionType " + qt);
  });
  const lv = [1, 2, 3].map((l) => d.questions.filter((q) => q.testLevel === l).length);
  console.log(`${f.split("/").pop()}: ${d.questions.length} питань (рівні ${lv.join("/")}), карток ${d.cards.length}`);
}
let short = 0;
for (const [k, v] of perTopic) {
  const ok = v.every((n) => n >= 50);
  if (!ok) short++;
  console.log(`${ok ? "✔" : "…"} ${k.split("|")[1].slice(0, 45)}: ${v.join("/")} ${ok ? "" : "(потрібно по 50 на рівень)"}`);
}
console.log(`Тем повністю готово (50/50/50): ${perTopic.size - short} з ${perTopic.size}`);
console.log(bad ? `Помилок: ${bad}` : `OK, питань: ${total}`);
process.exit(bad ? 1 : 0);
