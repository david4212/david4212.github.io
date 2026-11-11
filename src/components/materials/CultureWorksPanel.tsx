/* eslint-disable react/no-unescaped-entities */
"use client";

import { Clapperboard, Theater, ExternalLink } from "lucide-react";
import { NMT_CULTURE_WORKS } from "@/lib/history-culture";

export default function CultureWorksPanel({query}:{query:string}){
 const q=query.trim().toLocaleLowerCase("uk");
 const items=NMT_CULTURE_WORKS.filter(item=>
   `${item.title} ${item.director} ${item.author} ${item.year} ${item.nmtHint} ${item.cast||""}`.toLocaleLowerCase("uk").includes(q)
 );
 return <section className="mb-8 space-y-4">
   <div className="rounded-2xl bg-indigo-50 border border-indigo-100 p-5">
     <h2 className="font-black text-lg text-indigo-950">Кіно й театр: хто створив і чим відоме</h2>
     <p className="text-sm text-indigo-950/80 mt-2">Окремо від портретів — фільми, театральні об'єднання, режисери, оператори, сценаристи, актори та важливі для історії культурні події. Для давніх фільмів зазначаємо кіностудію, а не вигадуємо сучасну посаду продюсера.</p>
   </div>
   {items.map(item=><article key={item.title} className="rounded-2xl border border-slate-200 p-5 md:p-6 bg-white shadow-sm">
     <div className="flex justify-between gap-4 items-start">
       <div><span className="text-[11px] tracking-widest uppercase font-bold text-indigo-700">{item.category} · {item.year}</span>
         <h3 className="font-black text-xl sm:text-2xl text-slate-900 mt-1">{item.title}</h3>
       </div>
       {item.category==="Кіно"?<Clapperboard size={26} className="text-indigo-500 shrink-0"/>:<Theater size={26} className="text-indigo-500 shrink-0"/>}
     </div>
     <div className="grid sm:grid-cols-2 gap-x-7 gap-y-3 mt-5 text-sm leading-relaxed">
       <p><strong>Режисер / керівник:</strong> {item.director}</p>
       <p><strong>Автор / літературна основа:</strong> {item.author}</p>
       {item.studio&&<p><strong>Кіностудія:</strong> {item.studio}</p>}
       {item.script&&<p><strong>Сценаристи:</strong> {item.script}</p>}
       {item.camera&&<p><strong>Оператор:</strong> {item.camera}</p>}
       {item.cast&&<p><strong>Актори:</strong> {item.cast}</p>}
     </div>
     <p className="mt-5 text-sm text-slate-700 leading-relaxed">{item.historicalContext}</p>
     <div className="rounded-xl mt-4 p-4 bg-indigo-50 border-l-4 border-indigo-400 text-sm text-indigo-950 leading-relaxed"><strong>Що потрібно пов'язати для НМТ:</strong> {item.nmtHint}</div>
     <div className="mt-4 flex flex-wrap gap-4 text-sm">
       <a className="font-semibold text-indigo-700 hover:underline inline-flex gap-1 items-center" href={item.sourceUrl} target="_blank" rel="noopener noreferrer">Джерело відомостей <ExternalLink size={13}/></a>
       <a className="font-semibold text-indigo-700 hover:underline inline-flex gap-1 items-center" href={item.examSourceUrl} target="_blank" rel="noopener noreferrer">Візуальні завдання ЗНО/НМТ <ExternalLink size={13}/></a>
     </div>
   </article>)}
   {items.length===0&&<p className="text-sm text-center text-slate-500 p-6 bg-white border rounded-xl">За цим пошуком культурних творів немає.</p>}
 </section>;
}
