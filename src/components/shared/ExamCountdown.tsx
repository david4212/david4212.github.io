"use client";

import { useEffect, useState } from "react";

// Таймер до закінчення пробного НМТ
export default function ExamCountdown({ endTime }: { endTime: string }) {
  const [text, setText] = useState("");

  useEffect(() => {
    const end = new Date(endTime).getTime();
    const tick = () => {
      const d = end - Date.now();
      if (d <= 0) return setText("завершено");
      const days = Math.floor(d / 86400000);
      const hours = Math.floor((d % 86400000) / 3600000);
      const mins = Math.floor((d % 3600000) / 60000);
      setText(`${days} д ${hours} год ${mins} хв`);
    };
    tick();
    const t = setInterval(tick, 30000);
    return () => clearInterval(t);
  }, [endTime]);

  return <span>{text || "…"}</span>;
}
