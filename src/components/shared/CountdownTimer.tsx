"use client";

import { useState, useEffect } from 'react';

// ТУТ МОЖНА ЗМІНИТИ ДАТУ НМТ
const NMT_DATE = new Date('2027-05-14T00:00:00');

export default function CountdownTimer() {
  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date().getTime();
      const distance = NMT_DATE.getTime() - now;

      if (distance < 0) {
        clearInterval(timer);
        return;
      }

      setTimeLeft({
        days: Math.floor(distance / (1000 * 60 * 60 * 24)),
        hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((distance % (1000 * 60)) / 1000),
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-glass backdrop-blur-glass border border-glassBorder shadow-glass text-white w-full max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white/90">До НМТ залишилось:</h2>
      
      <div className="flex gap-4 text-center">
        <div className="flex flex-col">
          <span className="text-4xl font-bold text-ukrainian">{timeLeft.days}</span>
          <span className="text-xs uppercase text-gray-500 mt-1">Днів</span>
        </div>
        <span className="text-4xl font-bold text-gray-400">:</span>
        
        <div className="flex flex-col">
          <span className="text-4xl font-bold text-math">{timeLeft.hours}</span>
          <span className="text-xs uppercase text-gray-500 mt-1">Годин</span>
        </div>
        <span className="text-4xl font-bold text-gray-400">:</span>
        
        <div className="flex flex-col">
          <span className="text-4xl font-bold text-history">{timeLeft.minutes}</span>
          <span className="text-xs uppercase text-gray-500 mt-1">Хвилин</span>
        </div>
      </div>
    </div>
  );
}
