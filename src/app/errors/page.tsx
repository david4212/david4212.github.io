import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import ErrorsRunner from "@/components/errors/ErrorsRunner";

export const dynamic = "force-dynamic";

export default function ErrorsPage() {
  return (
    <main className="container mx-auto px-4 py-6 max-w-2xl min-h-screen">
      <Link href="/profile" className="inline-flex items-center text-slate-500 hover:text-slate-900 transition mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> Профіль
      </Link>
      <h1 className="text-3xl font-extrabold text-slate-900">Банк помилок</h1>
      <p className="text-slate-500 text-sm mt-1">Питання закриваються після 3 правильних відповідей поспіль у різних сесіях.</p>
      <ErrorsRunner />
    </main>
  );
}
