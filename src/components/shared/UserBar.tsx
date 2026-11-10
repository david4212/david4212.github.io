"use client";

import Link from "next/link";
import { signOut, useSession } from "next-auth/react";

const NAV = [
  { href: "/materials", label: "Матеріали" },
  { href: "/errors", label: "Помилки" },
  { href: "/diagnostic", label: "Діагностика" },
  { href: "/simulation", label: "Симуляція" },
];

export default function UserBar() {
  const { data, status } = useSession();

  return (
    <div className="container mx-auto max-w-5xl px-4 pt-4 flex flex-wrap justify-between items-center gap-x-4 gap-y-2 text-sm min-h-[3rem]">
      <nav className="flex flex-wrap gap-x-4 gap-y-1">
        {NAV.map((n) => (
          <Link key={n.href} href={n.href} className="text-slate-600 font-medium hover:text-indigo-700">{n.label}</Link>
        ))}
      </nav>
      <div className="flex items-center gap-4">
        {status === "loading" ? null : data?.user ? (
          <>
            {data.user.isAdmin ? (
              <Link href="/admin" className="font-semibold text-indigo-700 hover:underline">Адмін-панель</Link>
            ) : null}
            <Link href="/profile" className="text-indigo-700 font-semibold hover:underline">{data.user.name}</Link>
            <button onClick={() => signOut({ callbackUrl: "/" })} className="text-gray-500 hover:text-gray-900 underline">
              Вийти
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="text-blue-600 font-semibold hover:underline">Увійти</Link>
            <Link href="/register" className="text-gray-500 hover:text-gray-900">Реєстрація</Link>
          </>
        )}
      </div>
    </div>
  );
}
