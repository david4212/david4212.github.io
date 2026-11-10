"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      router.push("/login"); // Після успішної реєстрації кидаємо на вхід
    } else {
      const data = await res.json();
      setError(data.error || "Щось пішло не так");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md p-8 rounded-3xl bg-glass backdrop-blur-glass border border-glassBorder shadow-glass">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">Реєстрація</h1>
        
        {error && <p className="text-red-500 text-sm text-center mb-4">{error}</p>}
        
        <form onSubmit={handleRegister} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Придумай логін"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="px-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            required
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="px-4 py-3 rounded-xl bg-white/50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            required
          />
          <button
            type="submit"
            className="mt-2 py-3 rounded-xl bg-gray-900 text-white font-semibold hover:bg-gray-800 transition shadow-lg"
          >
            Створити акаунт
          </button>
        </form>
        
        <p className="mt-5 text-xs leading-relaxed text-gray-500">
          Результати тестів і час останньої активності зберігаються для особистого прогресу та загальної статистики сайту. Адміністратор має доступ до цієї статистики.
        </p>
        
        <p className="mt-6 text-center text-gray-600 text-sm">
          Вже маєш акаунт? <Link href="/login" className="text-blue-600 font-semibold hover:underline">Увійти</Link>
        </p>
      </div>
    </div>
  );
}
