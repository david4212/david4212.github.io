"use client";

import { useState, useEffect } from "react";
import { Flame } from "lucide-react";

// ТУТ МОЖНА ЗМІНИТИ ДАТУ НМТ
const NMT_DATE = new Date("2027-05-14T00:00:00");

const TILES = [
  { key: "days", label: "Днів" },
  { key: "hours", label: "Годин" },
  { key: "minutes", label: "Хвилин" },
  { key: "seconds", label: "Секунд" },
] as const;

export default function CountdownTimer() {
  const [timeLeft, setTimeLeft] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });

  useEffect(() => {
    const tick = () => {
      const distance = NMT_DATE.getTime() - Date.now();
      if (distance < 0) return;
      setTimeLeft({
        days: Math.floor(distance / (1000 * 60 * 60 * 24)),
        hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((distance % (1000 * 60)) / 1000),
      });
    };
    tick();
    const timer = setInterval(tick, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-violet-600 via-indigo-600 to-pink-500 p-6 md:p-10 shadow-xl text-white">
      <div className="absolute -top-10 -right-10 w-48 h-48 rounded-full bg-white/10" />
      <div className="absolute -bottom-12 -left-8 w-40 h-40 rounded-full bg-white/10" />

      <div className="relative flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1 rounded-full bg-white/20 backdrop-blur-md text-sm font-semibold mb-4">
          <Flame className="w-4 h-4" /> Час працює на тебе
        </div>
        <h2 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-6 drop-shadow-lg">До НМТ залишилось</h2>

        <div className="grid grid-cols-4 gap-3 md:gap-5 w-full max-w-xl">
          {TILES.map((t) => (
            <div key={t.key} className="backdrop-blur-md bg-white/20 text-white rounded-2xl p-3 md:p-4 shadow-lg">
              <div className="text-3xl md:text-5xl font-extrabold tabular-nums">{timeLeft[t.key]}</div>
              <div className="text-[10px] md:text-xs uppercase tracking-wider mt-1 text-white/80">{t.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
