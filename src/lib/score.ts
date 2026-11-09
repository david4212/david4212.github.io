// Переведення тестових балів НМТ у шкалу 100–200 (офіційні таблиці УЦОЯО, Додаток 5 до Порядку прийому 2026).
// Кожен масив починається з порогового балу (min): TABLES[subject].scale[0] = 100.
// Оновлюється щороку — міняй лише масиви нижче.
export type NmtSubject = "UKRAINIAN" | "MATH" | "HISTORY" | "ENGLISH";

type Table = { min: number; max: number; scale: number[] };

const TABLES: Record<NmtSubject, Table> = {
  UKRAINIAN: { min: 8, max: 45, scale: [100, 105, 110, 120, 125, 130, 134, 136, 138, 140, 142, 143, 144, 145, 146, 148, 149, 150, 152, 154, 156, 157, 159, 160, 162, 163, 165, 167, 170, 172, 175, 177, 180, 183, 186, 191, 195, 200] },
  MATH: { min: 5, max: 32, scale: [100, 108, 115, 123, 131, 134, 137, 140, 143, 145, 147, 148, 149, 150, 151, 152, 155, 159, 163, 167, 170, 173, 176, 180, 184, 189, 194, 200] },
  HISTORY: { min: 9, max: 54, scale: [100, 105, 110, 115, 120, 125, 130, 132, 134, 136, 138, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 154, 156, 158, 160, 163, 166, 168, 169, 170, 172, 173, 175, 177, 179, 181, 183, 185, 188, 191, 194, 197, 200] },
  ENGLISH: { min: 5, max: 32, scale: [100, 109, 118, 125, 131, 134, 137, 140, 143, 145, 147, 148, 149, 150, 151, 152, 153, 155, 157, 159, 162, 166, 169, 173, 179, 185, 191, 200] },
};

// Самоперевірка таблиць при завантаженні модуля (довжина = max - min + 1)
for (const [k, t] of Object.entries(TABLES)) {
  if (t.scale.length !== t.max - t.min + 1) throw new Error(`score.ts: таблиця ${k} має ${t.scale.length} значень замість ${t.max - t.min + 1}`);
}

export const NMT_MAX_RAW: Record<NmtSubject, number> = { UKRAINIAN: 45, MATH: 32, HISTORY: 54, ENGLISH: 32 };
export const NMT_THRESHOLD: Record<NmtSubject, number> = { UKRAINIAN: 8, MATH: 5, HISTORY: 9, ENGLISH: 5 };

export type NmtScore = { rawScore: number; maxPossibleRaw: number; nmtScore: number | null; isPassed: boolean };

/**
 * rawScore — кількість правильних відповідей у пробнику, maxPossibleRaw — кількість питань у ньому.
 * Якщо питань менше, ніж офіційний максимум, бал масштабується: round(raw / total * officialMax).
 */
export function calculateNmtScore(subject: string, rawScore: number, maxPossibleRaw: number): NmtScore {
  const t = TABLES[subject as NmtSubject];
  const total = Math.max(0, Math.floor(maxPossibleRaw));
  const raw = Math.max(0, Math.min(total, Math.floor(rawScore)));
  if (!t || total === 0) return { rawScore: raw, maxPossibleRaw: total, nmtScore: null, isPassed: false };
  const scaled = total === t.max ? raw : Math.round((raw / total) * t.max);
  if (scaled < t.min) return { rawScore: raw, maxPossibleRaw: total, nmtScore: null, isPassed: false };
  return { rawScore: raw, maxPossibleRaw: total, nmtScore: t.scale[Math.min(scaled, t.max) - t.min], isPassed: true };
}

/** Середній бал за предметами, складеними успішно; null, якщо хоча б один не складено. */
export function averageNmt(items: NmtScore[]): number | null {
  if (!items.length || items.some((i) => i.nmtScore === null)) return null;
  return Math.round(items.reduce((s, i) => s + (i.nmtScore as number), 0) / items.length);
}

// Лінійне наближення для змішаного тижневого пробного (кілька предметів в одному тесті)
export function mockScore(percent: number): number {
  return 100 + Math.max(0, Math.min(100, Math.round(percent)));
}
