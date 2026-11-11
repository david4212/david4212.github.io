/* eslint-disable react/no-unescaped-entities */
"use client";

import { useState } from "react";
import { Clapperboard, Theater, ExternalLink, EyeOff, Eye } from "lucide-react";
import { NMT_CINEMA_PEOPLE } from "@/lib/history-cinema-people";

export default function CultureWorksPanel({query}:{query:string}){
 const [hideRoles,setHideRoles]=useState(false);
 const q=query.trim().toLocaleLowerCase("uk");
 const people=NMT_CINEMA_PEOPLE.filter(person=>
  (`${person.name} ${person.field} ${person.period} ${person.focus} ${person.works.map(w=>w.title+" "+w.role+" "+w.year).join(" ")}`).toLocaleLowerCase("uk").includes(q)
 );
 return <section className="mb-8 space-y-5">
   <div className="rounded-2xl bg-indigo-50 border border-indigo-100 p-5">
     <div className="flex flex-wrap items-center justify-between gap-3">
       <div>
         <h2 className="font-black text-lg text-indigo-950">Кіно НМТ: діяч → фільм → конкретна роль</h2>
         <p className="text-sm text-indigo-950/80 mt-2">Не випадкова добірка фільмів, а люди, твори й ролі з тем історії України та завдань ЗНО/НМТ. Розрізняй <strong>режисера, сценариста, оператора й актора</strong>.</p>
       </div>
       <button type="button" className="inline-flex items-center gap-2 rounded-xl bg-white border border-indigo-200 px-3 py-2 text-indigo-900 text-sm font-semibold" onClick={()=>setHideRoles(v=>!v)}>{hideRoles?<Eye size={15}/>:<EyeOff size={15}/>} {hideRoles?"Показати ролі":"Приховати ролі"}</button>
     </div>
     <p className="text-xs text-indigo-800 mt-3">Позначка «основне» — ключовий матеріал для впізнавання; «контекст» — додаткова робота діяча, а не обіцянка, що саме цей твір буде в тесті.</p>
   </div>
   {people.map(person=><article key={person.name} className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
     <div className="px-5 py-4 sm:px-6 bg-slate-50 border-b border-slate-100 flex items-start justify-between gap-3">
       <div>
         <p className="text-xs uppercase tracking-wide text-indigo-700 font-bold">{person.period} · {person.field}</p>
         <h3 className="text-xl font-black text-slate-900 mt-1">{person.name}</h3>
       </div>
       {person.field.includes("Театр")||person.field.includes("театраль")?<Theater size={25} className="text-indigo-600 shrink-0"/>:<Clapperboard size={25} className="text-indigo-600 shrink-0"/>}
     </div>
     <div className="p-5 sm:p-6">
       <div className="overflow-x-auto">
         <table className="w-full text-sm min-w-[360px]">
           <thead><tr className="text-left text-slate-500 border-b border-slate-200"><th className="pb-2 pr-3 w-2/5">Фільм або твір</th><th className="pb-2 pr-3">Рік</th><th className="pb-2">Хто він у цьому творі?</th></tr></thead>
           <tbody>{person.works.map(work=><tr key={work.title} className="border-b border-slate-100 last:border-0 align-top">
             <td className="py-3 pr-3 font-bold text-slate-900">{work.title}{work.level==="основне"&&<span className="block text-[11px] text-emerald-700 font-semibold mt-1">Ключовий зв’язок</span>}<span className="block text-xs text-slate-500 font-normal mt-1">{work.fact}</span></td>
             <td className="py-3 pr-3 text-slate-600">{work.year}</td>
             <td className="py-3 text-slate-800 font-semibold">{hideRoles?"Приховано для самоперевірки":work.role}</td>
           </tr>)}</tbody>
         </table>
       </div>
       <div className="mt-4 rounded-xl bg-indigo-50 p-4 text-indigo-950 text-sm leading-relaxed">
         <strong>Що запам'ятати для НМТ:</strong> {hideRoles?"Пригадай професію діяча, його головний твір і конкретну роль у ньому.":person.focus}
       </div>
       <details className="mt-4 text-xs text-slate-500">
         <summary className="cursor-pointer text-indigo-700 font-bold">Перевірити джерела</summary>
         <div className="pt-2 space-y-2">{person.sources.map((url,i)=><a key={url} href={url} target="_blank" rel="noopener noreferrer" className="flex gap-1 items-center text-indigo-700 hover:underline">Джерело {i+1} <ExternalLink size={12}/></a>)}</div>
       </details>
     </div>
   </article>)}
   {people.length===0&&<p className="rounded-xl bg-white p-6 border text-center text-slate-500">За цим пошуком немає діячів або фільмів.</p>}
 </section>;
}
