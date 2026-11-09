// 3 рівні тестів у кожній темі та пороги успішності
export const LEVELS = [
  { level: 1, name: "Базовий", pass: 60, gradient: "from-emerald-500 to-teal-600", soft: "bg-emerald-100 text-emerald-800" },
  { level: 2, name: "Середній", pass: 75, gradient: "from-amber-500 to-orange-600", soft: "bg-amber-100 text-amber-800" },
  { level: 3, name: "Поглиблений", pass: 90, gradient: "from-rose-500 to-pink-600", soft: "bg-rose-100 text-rose-800" },
] as const;

export function getLevel(level: number) {
  return LEVELS.find((l) => l.level === level);
}
