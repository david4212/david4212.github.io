import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import SessionRunner from "@/components/session/SessionRunner";

export const dynamic = "force-dynamic";

export default function Page() {
  return (
    <main className="container mx-auto px-4 py-6 max-w-2xl min-h-screen">
      <Link href="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>
      <h1 className="text-3xl font-extrabold text-slate-900">Симуляція НМТ</h1>
      <p className="text-slate-500 text-sm mt-1">40 питань і 90 хвилин. Прогрес зберігається — можна повернутись і продовжити.</p>
      <SessionRunner kind="SIMULATION" />
    </main>
  );
}
