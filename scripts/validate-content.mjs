// Перевірка файлів content/: node scripts/validate-content.mjs
import { readFileSync, readdirSync, statSync } from "node:fs";
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
for (const f of files) {
  const d = JSON.parse(readFileSync(f, "utf-8"));
  const seen = new Set();
  d.questions.forEach((q, i) => {
    total++;
    const err = (m) => { bad++; console.log(`✗ ${f.split("/").pop()} #${i + 1}: ${m}`); };
    if (!q.text) err("немає тексту");
    const key = q.text + "\u0001" + [...(q.options || [])].sort().join("|");
    if (seen.has(key)) err("дубль");
    seen.add(key);
    if (!Array.isArray(q.options) || q.options.length < 2 || q.options.length > 5) err("кількість варіантів");
    else {
      if (new Set(q.options).size !== q.options.length) err("однакові варіанти");
      if (!(q.correctIndex >= 0 && q.correctIndex < q.options.length)) err("correctIndex");
    }
    if (!q.explanation || q.explanation.length < 30) err("коротке/відсутнє explanation");
    if (![1, 2, 3].includes(q.testLevel)) err("testLevel");
    if (!(d.legacy) && (!/💡/.test(q.explanation || "") || !/❌/.test(q.explanation || "") || !/✅/.test(q.explanation || ""))) err("explanation без 💡/❌/✅");
  });
  const lv = [1, 2, 3].map((l) => d.questions.filter((q) => q.testLevel === l).length);
  if (d.questions.length < 50 || d.cards.length < 20) console.log(`⚠ ${f.split("/").pop()}: менше 50 питань або 20 карток`);
  console.log(`${f.split("/").pop()}: ${d.questions.length} питань (рівні ${lv.join("/")}), карток ${d.cards.length}`);
}
console.log(bad ? `Помилок: ${bad}` : `OK, питань: ${total}`);
process.exit(bad ? 1 : 0);
