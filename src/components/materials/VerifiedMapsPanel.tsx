/* eslint-disable react/no-unescaped-entities, @next/next/no-img-element */
"use client";

import { useMemo, useState } from "react";
import { Maximize2, X, ShieldCheck, ExternalLink, Map as MapIcon, BookOpen, Eye, Layers3 } from "lucide-react";
import { VERIFIED_EXAM_MAPS, HISTORY_MAP_SOURCE_COLLECTIONS } from "@/lib/verified-exam-maps";
import { HISTORY_EDUCATIONAL_MAPS } from "@/lib/history-educational-maps";

type MapCard = {
 id:string; title:string; period:string; periodKey:string; imageUrl?:string;
 sourceName:string; sourceUrl:string; key:string; explanation:string; legend?:string[];
 kind:"exam"|"educational"; officialUrl?:string; answer?:string;
};
const PERIODS = [
 ["ancient","Стародавня історія"],["early","Русь і Королівство Руське"],
 ["h3","Козацька доба"],["h4","XIX — початок XX ст."],
 ["rev","Українська революція"],["interwar","Міжвоєнна доба"],
 ["ww2","Друга світова війна"],["postwar","Післявоєнна доба"],
 ["independence","Незалежна Україна"]
] as const;
const ORDER = PERIODS.map(p=>p[0]);
const ALL_MAPS:MapCard[] = [
 ...VERIFIED_EXAM_MAPS.map(m=>({...m,kind:"exam" as const})),
 ...HISTORY_EDUCATIONAL_MAPS
].sort((a,b)=>ORDER.indexOf(a.periodKey as typeof ORDER[number])-ORDER.indexOf(b.periodKey as typeof ORDER[number]));

export default function VerifiedMapsPanel({query,quiz}:{query:string;quiz:boolean}){
 const [period,setPeriod]=useState("all");
 const [type,setType]=useState("all");
 const [limit,setLimit]=useState(12);
 const [revealed,setRevealed]=useState<string[]>([]);
 const [opened,setOpened]=useState<string|null>(null);
 const [broken,setBroken]=useState<string[]>([]);
 const q=query.trim().toLocaleLowerCase("uk");
 const maps=useMemo(()=>ALL_MAPS.filter(m=>
   (period==="all"||period===m.periodKey) &&
   (type==="all"||type===m.kind) &&
   (`${m.title} ${m.period} ${m.key} ${m.explanation} ${(m.legend||[]).join(" ")}`).toLocaleLowerCase("uk").includes(q)
 ),[period,type,q]);
 const visible=maps.slice(0,limit);
 const selected=opened?ALL_MAPS.find(m=>m.id===opened):null;

 return <div className="space-y-5">
   <header className="rounded-2xl bg-emerald-50 border border-emerald-200 p-5 text-emerald-950">
     <h2 className="font-black text-xl flex gap-2 items-center"><MapIcon size={22}/> Історичний атлас: {ALL_MAPS.length} картосхеми</h2>
     <p className="text-sm mt-2 leading-relaxed">Історія України від античних міст і Русі до подій незалежності. Зображення, підказки, пояснення та легенди — прямо тут, без переходу на інший сайт.</p>
     <div className="flex gap-2 flex-wrap text-xs font-semibold mt-3">
       <span className="rounded-full bg-white border border-emerald-200 px-3 py-1">Завдання з архіву НМТ: {VERIFIED_EXAM_MAPS.length}</span>
       <span className="rounded-full bg-white border border-emerald-200 px-3 py-1">Навчальні історичні карти: {HISTORY_EDUCATIONAL_MAPS.length}</span>
     </div>
     <p className="mt-3 text-xs text-emerald-900/80">Навчальні карти УІНП та підручників не видаються за оригінальні завдання НМТ. Деякі зовнішні зображення можуть не завантажитися, якщо джерело недоступне.</p>
   </header>
   <div className="rounded-2xl border border-slate-200 bg-white p-4 flex flex-wrap gap-3 items-center">
     <label className="text-sm font-semibold text-slate-700" htmlFor="atlas-period">Епоха</label>
     <select id="atlas-period" value={period} onChange={e=>{setPeriod(e.target.value);setLimit(12);}} className="rounded-xl border border-slate-300 px-3 py-2 text-sm bg-white grow sm:grow-0 min-w-48">
       <option value="all">Усі епохи</option>
       {PERIODS.map(([value,label])=><option value={value} key={value}>{label} ({ALL_MAPS.filter(m=>m.periodKey===value).length})</option>)}
     </select>
     <label className="text-sm font-semibold text-slate-700" htmlFor="atlas-type">Джерело</label>
     <select id="atlas-type" value={type} onChange={e=>{setType(e.target.value);setLimit(12);}} className="rounded-xl border border-slate-300 px-3 py-2 text-sm bg-white grow sm:grow-0">
       <option value="all">Усі карти</option>
       <option value="exam">Завдання НМТ</option>
       <option value="educational">Навчальні карти</option>
     </select>
     <span className="text-xs text-slate-500 ml-auto">Знайдено: {maps.length}</span>
   </div>
   {visible.map(item=>{
     const show=!quiz||revealed.includes(item.id);
     const isExam=item.kind==="exam";
     return <article key={item.id} className="overflow-hidden rounded-3xl bg-white border border-slate-200 shadow-sm">
       <div className="p-4 sm:p-5 bg-[#1c453d] text-white">
         <p className="flex gap-2 items-center text-emerald-100 text-xs font-bold tracking-wide">
           {isExam?<ShieldCheck size={15}/>:<BookOpen size={15}/>}
           {isExam?"Оригінальне завдання НМТ / архів":"Навчальна історична карта"} · {item.sourceName}
         </p>
         <h2 className="font-black text-lg sm:text-xl mt-2">{item.title}</h2>
         <p className="text-sm text-emerald-100 mt-1">{item.period}</p>
       </div>
       <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(290px,1fr)]">
         <button type="button" className="p-4 sm:p-6 bg-[#f0ede5] text-left" onClick={()=>setOpened(item.id)} aria-label={`Збільшити карту: ${item.title}`}>
           {item.imageUrl&&!broken.includes(item.id)?
             <img src={item.imageUrl} alt={item.title} className="w-full max-h-[470px] object-contain bg-white rounded-xl shadow-sm" loading="lazy" onError={()=>setBroken(prev=>prev.includes(item.id)?prev:[...prev,item.id])}/>
             :<div className="rounded-xl bg-white p-9 text-sm text-center text-slate-600">Джерело зображення недоступне. Пояснення карти наведено поруч; адреса оригіналу вказана внизу.</div>}
           <span className="inline-flex gap-2 items-center text-sm font-bold text-emerald-800 mt-3"><Maximize2 size={15}/> Збільшити карту</span>
         </button>
         <div className="p-5 sm:p-6 flex flex-col gap-4">
           <div>
             <h3 className="text-xs uppercase font-black tracking-wider text-emerald-800">Що впізнати на карті</h3>
             <p className="mt-2 text-sm leading-relaxed text-slate-700">{show?item.key:"Спробуй назвати епоху, території, історичні процеси та позначення на зображенні."}</p>
           </div>
           {show&&item.legend&&item.legend.length>0&&<div className="rounded-xl bg-slate-50 border border-slate-200 p-4">
             <h3 className="text-sm font-black text-slate-900 mb-2 flex items-center gap-2"><Layers3 size={16}/> Легенда та орієнтири</h3>
             <ul className="text-sm leading-relaxed text-slate-700 space-y-2 list-disc pl-4">{item.legend.map((p,i)=><li key={i}>{p}</li>)}</ul>
           </div>}
           {show?<div className="rounded-xl bg-emerald-50 border border-emerald-200 p-4">
             <h3 className="font-bold text-emerald-950">{isExam?`Відповідь: ${item.answer||"дивись пояснення"}`:"Історичний контекст"}</h3>
             <p className="mt-2 text-sm leading-relaxed text-slate-800">{item.explanation}</p>
           </div>:<button type="button" className="rounded-xl bg-emerald-700 text-white text-sm font-bold px-4 py-2 w-fit" onClick={()=>setRevealed(a=>[...a,item.id])}><Eye size={15} className="inline mr-2"/>Показати пояснення</button>}
           <details className="mt-auto text-sm">
             <summary className="cursor-pointer font-semibold text-indigo-700">Першоджерело та авторство</summary>
             <div className="pt-2 flex flex-col gap-2">
               <a href={item.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-indigo-700 hover:underline inline-flex items-center gap-1">Оригінальна публікація <ExternalLink size={13}/></a>
               {isExam&&item.officialUrl&&item.officialUrl!==item.sourceUrl&&<a href={item.officialUrl} target="_blank" rel="noopener noreferrer" className="text-indigo-700 hover:underline inline-flex items-center gap-1">Тест або документ <ExternalLink size={13}/></a>}
             </div>
           </details>
         </div>
       </div>
     </article>;
   })}
   {maps.length>visible.length&&<button type="button" className="w-full rounded-2xl border border-emerald-300 text-emerald-900 bg-emerald-50 px-4 py-3 font-bold hover:bg-emerald-100" onClick={()=>setLimit(n=>n+12)}>Показати ще 12 карт ({maps.length-visible.length} залишилося)</button>}
   {maps.length===0&&<p className="rounded-xl bg-white border p-8 text-center text-slate-600">Карт за цим періодом або запитом не знайдено. Спробуй інший фільтр.</p>}
   <details className="rounded-2xl bg-white border border-slate-200 p-4">
     <summary className="cursor-pointer text-sm font-bold text-slate-800">Колекції та офіційні джерела карт</summary>
     <div className="pt-4 space-y-3">
       <a href="https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020" target="_blank" rel="noopener noreferrer" className="text-sm block text-indigo-700 hover:underline">Український інститут національної пам'яті — колекція історичних карт</a>
       {HISTORY_MAP_SOURCE_COLLECTIONS.map(s=><p className="text-sm" key={s.url}><a className="text-indigo-700 hover:underline font-semibold" href={s.url} target="_blank" rel="noopener noreferrer">{s.title}</a><span className="text-slate-600 block text-xs mt-1">{s.description}</span></p>)}
     </div>
   </details>
   {selected&&<div role="dialog" aria-modal="true" aria-label={`Карта: ${selected.title}`} className="fixed inset-0 z-[100] bg-slate-950/90 p-3 sm:p-5 flex flex-col" onClick={()=>setOpened(null)}>
     <div className="flex justify-between items-center gap-3 pb-3 text-white"><strong className="truncate">{selected.title}</strong><button type="button" className="rounded-xl p-2 bg-white/15" aria-label="Закрити" onClick={()=>setOpened(null)}><X size={22}/></button></div>
     <div className="flex-1 min-h-0 overflow-auto flex justify-center items-center" onClick={e=>e.stopPropagation()}>
       {selected.imageUrl&&<img src={selected.imageUrl} alt={selected.title} className="max-w-full max-h-full object-contain"/>}
     </div>
   </div>}
 </div>;
}
