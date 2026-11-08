"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const res = await signIn("credentials", {
      username,
      password,
      redirect: false,
    });

    if (res?.error) {
      setError("Невірний логін або пароль");
    } else {
      router.push("/"); // Після входу кидаємо на головну
      router.refresh(); // Оновлюємо стан, щоб підтягнулась сесія
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md p-8 rounded-3xl bg-glass backdrop-blur-glass border border-glassBorder shadow-glass">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">Вхід</h1>
        
        {error && <p className="text-red-500 text-sm text-center mb-4">{error}</p>}
        
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Твій логін"
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
            className="mt-2 py-3 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition shadow-lg shadow-blue-500/30"
          >
            Увійти
          </button>
        </form>
        
        <p className="mt-6 text-center text-gray-600 text-sm">
          Ще немає акаунту? <Link href="/register" className="text-blue-600 font-semibold hover:underline">Зареєструватися</Link>
        </p>
      </div>
    </div>
  );
}
