/* eslint-disable react/no-unescaped-entities, @next/next/no-img-element */
"use client";

import { useState } from "react";
import { Maximize2, X, ShieldCheck, ExternalLink, Map as MapIcon } from "lucide-react";
import { VERIFIED_EXAM_MAPS, HISTORY_MAP_SOURCE_COLLECTIONS } from "@/lib/verified-exam-maps";

export default function VerifiedMapsPanel({ query, quiz }: { query: string; quiz: boolean }) {
 const [revealed, setRevealed] = useState<string[]>([]);
 const [opened, setOpened] = useState<string|null>(null);
 const [broken, setBroken] = useState<string[]>([]);
 const q = query.trim().toLocaleLowerCase("uk");
 const maps = VERIFIED_EXAM_MAPS.filter(x => `${x.title} ${x.period} ${x.key} ${x.explanation}`.toLocaleLowerCase("uk").includes(q));
 return <div className="space-y-5">
   <div className="rounded-2xl bg-amber-50 border border-amber-200 p-5 text-amber-950">
     <h2 className="font-black text-lg">Оригінальні картосхеми НМТ / ЗНО</h2>
     <p className="text-sm mt-2 leading-relaxed">Неперевірені саморобні карти та блок прапорів прибрано з атласу. Тут відображаються лише ті карти, для яких звірено ілюстрацію, рік, завдання й правильну відповідь з оприлюдненим екзаменаційним джерелом.</p>
     <p className="text-xs mt-2 font-semibold">Перевірених карт зараз: {VERIFIED_EXAM_MAPS.length}. Нові картки додаються після перевірки, а не за кількістю.</p>
   </div>
   {maps.map(item => {
     const show = !quiz || revealed.includes(item.id);
     return <article key={item.id} className="overflow-hidden rounded-3xl bg-white border border-slate-200 shadow-sm">
       <div className="px-5 py-4 bg-[#1c453d] text-white">
         <span className="flex gap-2 items-center text-emerald-100 uppercase tracking-widest text-xs font-bold"><ShieldCheck size={16}/> Перевірене джерело · {item.sourceName}</span>
         <h2 className="font-black text-xl mt-2">{item.title}</h2>
         <p className="text-sm text-emerald-100 mt-1">{item.period}</p>
       </div>
       <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(290px,1fr)]">
         <button type="button" onClick={()=>setOpened(item.id)} className="p-4 sm:p-6 bg-[#f0ede5] text-left" aria-label={`Збільшити карту: ${item.title}`}>
           {item.imageUrl&&!broken.includes(item.id) ? <img src={item.imageUrl} alt={item.title} className="w-full max-h-[440px] object-contain rounded-lg shadow-md bg-white" loading="lazy" onError={()=>setBroken(old=>[...old,item.id])}/> :
             <div className="p-10 text-sm text-center text-slate-600 bg-white rounded-xl">Мініатюру не завантажено — відкрий оригінальний документ УЦОЯО за посиланням праворуч.</div>}
           <p className="inline-flex gap-2 items-center text-sm font-bold text-[#20544a] mt-3"><Maximize2 size={15}/> Переглянути карту</p>
         </button>
         <div className="p-5 sm:p-6 flex flex-col gap-4">
           <div><h3 className="uppercase text-xs font-black tracking-widest text-emerald-800">Як читати карту</h3><p className="text-sm leading-relaxed text-slate-700 mt-2">{item.key}</p></div>
           {show ? <div className="bg-emerald-50 rounded-xl border border-emerald-200 p-4">
             <p className="font-black text-emerald-900">Правильна позначка: {item.answer}</p>
             <p className="text-sm text-slate-800 mt-2 leading-relaxed">{item.explanation}</p>
           </div> : <button type="button" className="w-fit px-4 py-2 rounded-xl bg-emerald-700 text-white font-bold text-sm" onClick={()=>setRevealed(x=>[...x,item.id])}>Показати відповідь</button>}
           <div className="mt-auto pt-3 flex flex-wrap gap-3 text-sm">
             <a href={item.officialUrl} target="_blank" rel="noopener noreferrer" className="font-bold text-indigo-700 hover:underline inline-flex items-center gap-1">Оригінал УЦОЯО <ExternalLink size={13}/></a>
             <a href={item.sourceUrl} target="_blank" rel="noopener noreferrer" className="font-bold text-indigo-700 hover:underline inline-flex items-center gap-1">Архів та пояснення <ExternalLink size={13}/></a>
           </div>
         </div>
       </div>
     </article>;
   })}
   {maps.length===0&&<p className="rounded-xl border bg-white p-8 text-center text-slate-500">Перевірених карт за таким пошуком поки немає.</p>}
   <div className="rounded-2xl border border-slate-200 bg-white p-5">
     <div className="flex items-center gap-2 mb-4"><MapIcon className="text-emerald-700"/><h2 className="font-black text-lg">Де тренуватися на оригінальних картах</h2></div>
     <div className="space-y-4">{HISTORY_MAP_SOURCE_COLLECTIONS.map(s=><div key={s.url}>
       <a href={s.url} target="_blank" rel="noopener noreferrer" className="font-bold text-indigo-700 hover:underline">{s.title} ↗</a>
       <p className="text-sm text-slate-600 mt-1">{s.description}</p>
     </div>)}</div>
   </div>
   {opened&&<div role="dialog" aria-modal="true" aria-label="Оригінальна карта НМТ" className="fixed inset-0 z-[100] bg-slate-950/90 p-4 flex flex-col" onClick={()=>setOpened(null)}>
     <div className="flex justify-between items-center gap-3 pb-3 text-white"><strong className="truncate">{VERIFIED_EXAM_MAPS.find(x=>x.id===opened)?.title}</strong><button type="button" className="rounded-xl p-2 bg-white/15" onClick={()=>setOpened(null)} aria-label="Закрити"><X size={23}/></button></div>
     <div className="flex-1 min-h-0 overflow-auto flex justify-center items-center" onClick={e=>e.stopPropagation()}>
       {VERIFIED_EXAM_MAPS.find(x=>x.id===opened)?.imageUrl&&<img src={VERIFIED_EXAM_MAPS.find(x=>x.id===opened)?.imageUrl} alt="Збільшена картосхема з НМТ" className="max-w-full max-h-full object-contain" />}
     </div>
   </div>}
 </div>;
}
