import Link from "next/link";

export default function LoginPrompt({ text = "Увійди, щоб користуватись цим розділом." }: { text?: string }) {
  return (
    <div className="text-center p-10 mt-8 bg-white rounded-3xl border border-slate-100 shadow-md">
      <p className="text-slate-600 mb-4">{text}</p>
      <Link href="/login" className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold">Увійти</Link>
    </div>
  );
}
