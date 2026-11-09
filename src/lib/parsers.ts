// Парсери текстових шаблонів, які адмін надсилає боту.

export type ParsedQuestion = { text: string; options: string[]; correctIndex: number; imageUrl?: string };
export type ParsedCard = { question: string; answer: string; imageUrl?: string };
export type ParseResult<T> = { items: T[]; errors: string[] };

// Кирилиця А Б В Г Д Е та латиниця A B C D E (різні символи, тому мапимо обидва)
const LETTER_INDEX: Record<string, number> = {
  "А": 0, "Б": 1, "В": 2, "Г": 3, "Д": 4, "Е": 4,
  "A": 0, "B": 1, "C": 2, "D": 3, "E": 4,
  "1": 0, "2": 1, "3": 2, "4": 3, "5": 4,
};

function letterToIndex(raw: string): number | null {
  const ch = raw.trim().charAt(0).toUpperCase();
  return ch in LETTER_INDEX ? LETTER_INDEX[ch] : null;
}

const QUESTION_HEADER = /^\s*Питання\s*(?:№?\s*\d+)?\s*[:.)]\s*(.*)$/i;
const OPTION_LINE = /^\s*([А-ЕA-E1-5])\s*[:.)\-–—]\s*(.*\S)\s*$/i;
const ANSWER_LINE = /^\s*(?:Правильна\s+)?Відповідь\s*[:\-–—]\s*(.*\S)\s*$/i;

// Рядок «Фото: https://...» (також розуміє markdown-посилання [url](url))
const PHOTO_LINE = /^\s*(?:Фото|Photo|Image|Картинка)\s*[:\-–—]\s*(.*)$/i;
const URL_IN_TEXT = /(https?:\/\/[^\s\]\)>]+)/;
function photoUrl(raw: string): string | null {
  const m = raw.match(URL_IN_TEXT);
  return m ? m[1] : null;
}

const preview = (s: string) => (s.length > 40 ? s.slice(0, 40) + "…" : s);

export function parseQuestions(input: string): ParseResult<ParsedQuestion> {
  const lines = input.replace(/\r/g, "").split("\n");
  const blocks: string[][] = [];
  for (const line of lines) {
    if (QUESTION_HEADER.test(line)) blocks.push([line]);
    else if (blocks.length > 0) blocks[blocks.length - 1].push(line);
  }

  const items: ParsedQuestion[] = [];
  const errors: string[] = [];

  blocks.forEach((block, i) => {
    const n = i + 1;
    const questionLines: string[] = [];
    const options: (string | undefined)[] = [];
    let lastOption = -1;
    let answerRaw: string | null = null;
    let imageUrl: string | undefined;
    let photoError = false;

    for (const line of block) {
      const header = line.match(QUESTION_HEADER);
      if (header && questionLines.length === 0 && lastOption === -1 && block[0] === line) {
        if (header[1].trim()) questionLines.push(header[1].trim());
        continue;
      }
      if (!line.trim()) continue;

      const photo = line.match(PHOTO_LINE);
      if (photo) {
        const url = photoUrl(photo[1]);
        if (url) imageUrl = url;
        else photoError = true;
        continue;
      }

      const ans = line.match(ANSWER_LINE);
      if (ans) {
        answerRaw = ans[1];
        continue;
      }
      const opt = line.match(OPTION_LINE);
      if (opt) {
        const idx = letterToIndex(opt[1]);
        if (idx !== null) {
          options[idx] = opt[2].trim();
          lastOption = idx;
          continue;
        }
      }
      // продовження тексту питання або попереднього варіанта
      if (lastOption === -1) questionLines.push(line.trim());
      else options[lastOption] = `${options[lastOption]} ${line.trim()}`;
    }

    const text = questionLines.join(" ").trim();
    const label = `Питання №${n}${text ? ` («${preview(text)}»)` : ""}`;

    if (!text) return void errors.push(`${label}: немає тексту питання`);
    if (photoError) return void errors.push(`${label}: у рядку «Фото:» немає посилання (https://...)`);
    const count = options.length;
    if (count < 2 || count > 5 || Array.from(options).some((o) => !o)) {
      return void errors.push(`${label}: потрібно від 2 до 5 варіантів підряд (А, Б, В, Г…)`);
    }
    if (!answerRaw) return void errors.push(`${label}: немає рядка «Відповідь: …»`);
    const correctIndex = letterToIndex(answerRaw);
    if (correctIndex === null || correctIndex >= count) {
      return void errors.push(`${label}: відповідь «${answerRaw}» не збігається з варіантами`);
    }

    items.push({ text, options: options as string[], correctIndex, ...(imageUrl ? { imageUrl } : {}) });
  });

  if (blocks.length === 0) {
    errors.push("Не знайшов жодного блоку. Кожне питання має починатись з «Питання:».");
  }
  return { items, errors };
}

const TERM_LINE = /^\s*Термін\s*[:.)]\s*(.*)$/i;
const EXPLAIN_LINE = /^\s*Пояснення\s*[:.)]\s*(.*)$/i;

export function parseCards(input: string): ParseResult<ParsedCard> {
  const lines = input.replace(/\r/g, "").split("\n");
  const cards: { term: string[]; explain: string[]; imageUrl?: string; photoError?: boolean }[] = [];
  let current: "term" | "explain" = "term";

  for (const line of lines) {
    const t = line.match(TERM_LINE);
    if (t) {
      cards.push({ term: [t[1].trim()], explain: [] });
      current = "term";
      continue;
    }
    if (cards.length === 0) continue;
    const ph = line.match(PHOTO_LINE);
    if (ph) {
      const url = photoUrl(ph[1]);
      if (url) cards[cards.length - 1].imageUrl = url;
      else cards[cards.length - 1].photoError = true;
      continue;
    }
    const e = line.match(EXPLAIN_LINE);
    if (e) {
      cards[cards.length - 1].explain.push(e[1].trim());
      current = "explain";
      continue;
    }
    if (line.trim()) cards[cards.length - 1][current].push(line.trim());
  }

  const items: ParsedCard[] = [];
  const errors: string[] = [];
  cards.forEach((c, i) => {
    const question = c.term.join(" ").trim();
    const answer = c.explain.join(" ").trim();
    if (c.photoError) {
      errors.push(`Картка №${i + 1}${question ? ` («${preview(question)}»)` : ""}: у рядку «Фото:» немає посилання (https://...)`);
    } else if (!question || !answer) {
      errors.push(`Картка №${i + 1}${question ? ` («${preview(question)}»)` : ""}: потрібні і «Термін:», і «Пояснення:»`);
    } else {
      items.push({ question, answer, ...(c.imageUrl ? { imageUrl: c.imageUrl } : {}) });
    }
  });

  if (cards.length === 0) {
    errors.push("Не знайшов жодної картки. Кожна має починатись з «Термін:».");
  }
  return { items, errors };
}
