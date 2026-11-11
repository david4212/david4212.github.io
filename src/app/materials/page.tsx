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
      <p className="text-slate-500 text-sm mt-2">Обери предмет нижче: там зібрані правила, формули, приклади та довідкові матеріали для повторення.</p>
      <MaterialsTabs />
    </main>
  );
}
