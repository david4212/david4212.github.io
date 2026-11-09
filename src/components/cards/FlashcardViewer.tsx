"use client";

import { useState } from "react";
import { ChevronRight, ChevronLeft, RotateCcw } from "lucide-react";
import ZoomImage from "@/components/shared/ZoomImage";

type Flashcard = {
  id: string;
  question: string;
  answer: string;
  imageUrl?: string | null;
};

export default function FlashcardViewer({ cards }: { cards: Flashcard[] }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  if (!cards || cards.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-white/70 backdrop-blur-sm rounded-3xl border border-slate-200 mt-10">
        <p className="text-xl text-slate-500 mb-2">Тут поки немає карток.</p>
        <p className="text-sm text-slate-400">Додай їх через Telegram-бота!</p>
      </div>
    );
  }

  const card = cards[currentIndex];

  const nextCard = () => {
    setIsFlipped(false);
    if (currentIndex < cards.length - 1) setCurrentIndex((prev) => prev + 1);
  };

  const prevCard = () => {
    setIsFlipped(false);
    if (currentIndex > 0) setCurrentIndex((prev) => prev - 1);
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center mt-8">
      <div className="flex justify-between w-full max-w-xl mb-4 px-4">
        <span className="text-slate-500 font-medium">Прогрес:</span>
        <span className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-bold">
          {currentIndex + 1} / {cards.length}
        </span>
      </div>

      <div
        onClick={() => setIsFlipped(!isFlipped)}
        className={`relative w-full max-w-xl cursor-pointer ${card.imageUrl ? "h-[28rem]" : "h-80"}`}
        style={{ perspective: "1000px" }}
      >
        <div
          className="w-full h-full relative transition-transform duration-500 shadow-xl rounded-3xl"
          style={{ transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)", transformStyle: "preserve-3d" }}
        >
          {/* Передня сторона */}
          <div className="absolute w-full h-full bg-white border border-slate-200 rounded-3xl p-6 flex flex-col items-center justify-center" style={{ backfaceVisibility: "hidden" }}>
            <span className="text-sm uppercase text-indigo-500 font-bold mb-3">Запитання</span>
            {card.imageUrl && <ZoomImage src={card.imageUrl} className="max-h-48 mb-4" />}
            <p className="text-2xl text-center font-semibold text-slate-800">{card.question}</p>
            <div className="absolute bottom-5 flex items-center text-slate-400 text-sm">
              <RotateCcw className="w-4 h-4 mr-2" /> Натисни, щоб перевернути
            </div>
          </div>

          {/* Задня сторона */}
          <div
            className="absolute w-full h-full bg-gradient-to-br from-indigo-600 to-violet-700 text-white rounded-3xl p-8 flex flex-col items-center justify-center shadow-2xl"
            style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)" }}
          >
            <span className="text-sm uppercase text-white/70 font-bold mb-4">Відповідь</span>
            <p className="text-2xl text-center font-semibold">{card.answer}</p>
          </div>
        </div>
      </div>

      <div className="flex gap-4 mt-10">
        <button onClick={prevCard} disabled={currentIndex === 0} className="p-4 rounded-full bg-white shadow-md text-slate-600 disabled:opacity-40 hover:bg-slate-50 transition">
          <ChevronLeft className="w-6 h-6" />
        </button>
        <button onClick={nextCard} disabled={currentIndex === cards.length - 1} className="p-4 rounded-full bg-white shadow-md text-slate-600 disabled:opacity-40 hover:bg-slate-50 transition">
          <ChevronRight className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
}
