"use client";

import { useState } from "react";
import { ChevronRight, ChevronLeft, RotateCcw } from "lucide-react";

type Flashcard = {
  id: string;
  question: string;
  answer: string;
};

export default function FlashcardViewer({ cards }: { cards: Flashcard[] }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  if (!cards || cards.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-white/50 backdrop-blur-sm rounded-3xl border border-gray-200 mt-10">
        <p className="text-xl text-gray-500 mb-2">У цій темі поки немає карток.</p>
        <p className="text-sm text-gray-400">Додай їх через Telegram-бота!</p>
      </div>
    );
  }

  const nextCard = () => {
    setIsFlipped(false);
    if (currentIndex < cards.length - 1) setCurrentIndex(prev => prev + 1);
  };

  const prevCard = () => {
    setIsFlipped(false);
    if (currentIndex > 0) setCurrentIndex(prev => prev - 1);
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center perspective-1000 mt-8">
      <div className="flex justify-between w-full max-w-xl mb-4 px-4">
        <span className="text-gray-500 font-medium">Прогрес:</span>
        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-bold">
          {currentIndex + 1} / {cards.length}
        </span>
      </div>

      <div 
        onClick={() => setIsFlipped(!isFlipped)}
        className="relative w-full max-w-xl h-80 cursor-pointer group"
        style={{ perspective: "1000px" }}
      >
        <div 
          className="w-full h-full relative transition-transform duration-500 transform-style-3d shadow-glass rounded-3xl"
          style={{ transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)", transformStyle: "preserve-3d" }}
        >
          {/* Передня сторона */}
          <div className="absolute w-full h-full bg-glass backdrop-blur-glass border border-glassBorder rounded-3xl p-8 flex flex-col items-center justify-center backface-hidden" style={{ backfaceVisibility: "hidden" }}>
            <span className="text-sm uppercase text-gray-500 font-bold mb-4">Запитання</span>
            <p className="text-2xl text-center font-semibold text-gray-800">
              {cards[currentIndex].question}
            </p>
            <div className="absolute bottom-6 flex items-center text-gray-400 text-sm">
              <RotateCcw className="w-4 h-4 mr-2" /> Натисни, щоб перевернути
            </div>
          </div>

          {/* Задня сторона */}
          <div className="absolute w-full h-full bg-gray-900 text-white rounded-3xl p-8 flex flex-col items-center justify-center backface-hidden shadow-2xl" style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)" }}>
            <span className="text-sm uppercase text-gray-400 font-bold mb-4">Відповідь</span>
            <p className="text-2xl text-center font-semibold text-white">
              {cards[currentIndex].answer}
            </p>
          </div>
        </div>
      </div>

      {/* Кнопки */}
      <div className="flex gap-4 mt-10">
        <button onClick={prevCard} disabled={currentIndex === 0} className="p-4 rounded-full bg-white shadow-soft text-gray-600 disabled:opacity-50 hover:bg-gray-50 transition">
          <ChevronLeft className="w-6 h-6" />
        </button>
        <button onClick={nextCard} disabled={currentIndex === cards.length - 1} className="p-4 rounded-full bg-white shadow-soft text-gray-600 disabled:opacity-50 hover:bg-gray-50 transition">
          <ChevronRight className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
}
