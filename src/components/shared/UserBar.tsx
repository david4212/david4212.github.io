"use client";

import Link from "next/link";
import { signOut, useSession } from "next-auth/react";
import { GraduationCap } from "lucide-react";

const NAV = [
  { href: "/materials", label: "Матеріали" },
  { href: "/errors", label: "Помилки" },
  { href: "/diagnostic", label: "Діагностика" },
  { href: "/simulation", label: "Пробник НМТ" },
];

export default function UserBar() {
  const { data, status } = useSession();
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 bg-white/95 shadow-sm backdrop-blur-xl supports-[backdrop-filter]:bg-white/85">
      <div className="container mx-auto max-w-6xl px-4 py-2.5">
        <div className="flex items-center justify-between gap-3">
          <Link href="/" aria-label="НМТ на 200 — на головну" className="flex shrink-0 items-center gap-2 text-indigo-700 font-black tracking-tight">
            <span className="grid size-9 place-items-center rounded-xl bg-indigo-600 text-white"><GraduationCap size={21} /></span>
            <span className="hidden sm:inline">НМТ на <span className="text-rose-500">200</span></span>
            <span className="sm:hidden">НМТ 200</span>
          </Link>
          <div className="flex min-w-0 items-center gap-3 text-xs sm:text-sm">
            {status === "loading" ? <span className="text-slate-400">Завантаження…</span> : data?.user ? (
              <>
                {data.user.isAdmin && <Link href="/admin" className="hidden sm:inline text-indigo-700 font-semibold hover:underline">Адмінка</Link>}
                <Link href="/profile" className="max-w-[100px] sm:max-w-[190px] truncate text-indigo-700 font-bold hover:underline">{data.user.name || "Профіль"}</Link>
                <button type="button" onClick={() => signOut({ callbackUrl: "/" })} className="shrink-0 text-slate-500 hover:text-slate-900">Вийти</button>
              </>
            ) : (
              <>
                <Link href="/login" className="font-bold text-indigo-700 hover:underline">Увійти</Link>
                <Link href="/register" className="text-slate-600 hover:text-slate-900">Реєстрація</Link>
              </>
            )}
          </div>
        </div>
        <nav aria-label="Основна навігація" className="mt-2 flex items-center gap-1 overflow-x-auto whitespace-nowrap pb-0.5 text-xs sm:text-sm md:gap-2">
          <Link href="/" className="shrink-0 rounded-lg px-3 py-2 font-semibold text-slate-600 transition-colors hover:bg-indigo-50 hover:text-indigo-700">Головна</Link>
          {NAV.map(n => <Link key={n.href} href={n.href} className="shrink-0 rounded-lg px-3 py-2 font-semibold text-slate-600 transition-colors hover:bg-indigo-50 hover:text-indigo-700">{n.label}</Link>)}
          {data?.user?.isAdmin && <Link href="/admin" className="shrink-0 rounded-lg px-3 py-2 font-semibold text-indigo-700 hover:bg-indigo-50 sm:hidden">Адмінка</Link>}
        </nav>
      </div>
    </header>
  );
}
