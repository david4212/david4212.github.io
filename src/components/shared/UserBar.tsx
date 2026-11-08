"use client";

import Link from "next/link";
import { signOut, useSession } from "next-auth/react";

export default function UserBar() {
  const { data, status } = useSession();

  return (
    <div className="container mx-auto max-w-5xl px-4 pt-4 flex justify-end items-center gap-4 text-sm min-h-[3rem]">
      {status === "loading" ? null : data?.user ? (
        <>
          <span className="text-gray-600">{data.user.name}</span>
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
  );
}
