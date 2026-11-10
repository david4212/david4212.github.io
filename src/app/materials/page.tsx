import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import MaterialsTabs from "@/components/materials/MaterialsTabs";

export const metadata = { title: "Матеріали для підготовки | НМТ на 200" };

export default function MaterialsPage() {
  return (
    <main className="container mx-auto px-4 py-6 max-w-3xl min-h-screen">
      <Link href="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> На головну
      </Link>
      <h1 className="text-3xl font-extrabold text-slate-900">Матеріали для підготовки</h1>
      <p className="text-slate-500 text-sm mt-1">Конспекти за темами НМТ, формули й правила, візуальний атлас історії, пошук і самоперевірка.</p>
      <div className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="rounded-2xl bg-blue-50 border border-blue-100 p-4"><p className="font-bold text-blue-900">Математика</p><p className="text-xs mt-1 text-blue-700">Алгоритми, формули, типові пастки</p></div>
        <div className="rounded-2xl bg-emerald-50 border border-emerald-100 p-4"><p className="font-bold text-emerald-900">Українська мова</p><p className="text-xs mt-1 text-emerald-700">Правопис, морфологія, синтаксис</p></div>
        <Link href="/materials/history" className="rounded-2xl bg-amber-50 border border-amber-200 p-4 hover:shadow-md transition"><p className="font-bold text-amber-900">Історія в кадрі →</p><p className="text-xs mt-1 text-amber-700">Карти, персоналії, мистецтво, кіно</p></Link>
      </div>
      <MaterialsTabs />
    </main>
  );
}
