import CountdownTimer from "@/components/shared/CountdownTimer";
import Link from "next/link";

const subjects = [
  { id: "UKRAINIAN", name: "Українська мова", color: "bg-ukrainian" },
  { id: "MATH", name: "Математика", color: "bg-math" },
  { id: "HISTORY", name: "Історія України", color: "bg-history" },
  { id: "ENGLISH", name: "Англійська мова", color: "bg-english" },
];

export default function Home() {
  return (
    <main className="container mx-auto px-4 py-10 max-w-5xl">
      {/* Заголовок */}
      <header className="text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 mb-4 tracking-tight">
          НМТ на <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">200</span>
        </h1>
        <p className="text-lg text-gray-600">Відслідковуй прогрес, вчи флеш-картки та досягай мети</p>
      </header>

      {/* Таймер */}
      <section className="mb-16">
        <CountdownTimer />
      </section>

      {/* Картки предметів */}
      <section>
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Твої предмети</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {subjects.map((sub) => (
            <Link href={`/subjects/${sub.id.toLowerCase()}`} key={sub.id}>
              <div className="relative overflow-hidden p-6 rounded-3xl bg-glass backdrop-blur-glass border border-glassBorder shadow-glass hover:-translate-y-1 hover:shadow-xl transition-all duration-300 group cursor-pointer">
                
                {/* Кольоровий акцент у кутку картки */}
                <div className={`absolute top-0 right-0 w-24 h-24 opacity-20 rounded-bl-full transition-all group-hover:scale-110 ${sub.color}`}></div>
                
                <h3 className="text-2xl font-bold text-gray-800 mb-2">{sub.name}</h3>
                
                {/* Заглушка прогрес-бару (пізніше підключимо сюди реальні дані з БД) */}
                <div className="mt-6">
                  <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Загальний прогрес:</span>
                    <span className="font-bold">0%</span>
                  </div>
                  <div className="w-full bg-gray-200/50 rounded-full h-3 backdrop-blur-sm overflow-hidden">
                    <div className={`h-3 rounded-full ${sub.color} w-[0%] transition-all duration-1000`}></div>
                  </div>
                </div>

              </div>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
