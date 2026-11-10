/* eslint-disable @next/next/no-img-element */
"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, ExternalLink, Map as MapIcon, Images, Landmark, Clapperboard, Search, Maximize2, Eye, EyeOff, BookOpen, ZoomIn, ZoomOut, X, CheckCircle2 } from "lucide-react";
import { HISTORY_VISUALS, type VisualItem } from "@/lib/history-gallery";
import { HISTORY_MAP_NOTES, type MapNote } from "@/lib/history-map-notes";
import { HISTORY_PHOTOS, type HistoryPhoto } from "@/lib/history-photos";

type Tab = "figures" | "maps" | "art" | "cinema";
type OpenVisual = {src:string;title:string;description:string;tip?:string};
const TABS: {id:Tab;title:string;subtitle:string;icon:typeof Images}[] = [
  {id:"figures",title:"Обличчя історії",subtitle:"Фото й портрети",icon:Images},
  {id:"maps",title:"Атлас подій",subtitle:"Карти, схеми, дати",icon:MapIcon},
  {id:"art",title:"Галерея епох",subtitle:"Архітектура й мистецтво",icon:Landmark},
  {id:"cinema",title:"Кадри культури",subtitle:"Режисери та кіно",icon:Clapperboard}
];
const PERIODS:{value:string;label:string}[]=[
 {value:"all",label:"Усі епохи"},
 {value:"early",label:"Русь і Литовська доба"},
 {value:"h3",label:"Козацтво"},
 {value:"h4",label:"XVIII–XIX століття"},
 {value:"h5",label:"Революція 1917–1921"},
 {value:"h6",label:"1919–1945"},
 {value:"h7",label:"1945–1991"},
 {value:"h8",label:"Незалежність"}
];
function mapPeriod(src:string) {
 const n=src.split("/").pop() || "";
 const found=n.match(/(?:map_|tl_)?(h[3-8])_/);
 if(found)return found[1];
 if(/rus|halych|vkl/.test(n))return "early";
 if(/kozak|klejnody|sich|reestr|hetman/.test(n))return "h3";
 if(/avstro|vidrodzhennya|prapory/.test(n))return "h4";
 return "h5";
}
function getNote(item:VisualItem):MapNote|null{
 const key=item.src.split("/").pop()?.replace(/\.svg$/,"")||"";
 return HISTORY_MAP_NOTES[key]||null;
}
function ImageWithFallback({src,title,large=false}:{src:string;title:string;large?:boolean}) {
 const [failed,setFailed]=useState(false);
 if(failed)return <div className="w-full min-h-48 p-6 flex flex-col items-center justify-center gap-2 bg-slate-100 text-center text-slate-600">
  <Images size={26} className="text-slate-400" /><strong className="text-sm">Фото тимчасово недоступне</strong>
  <span className="text-xs">Не показуємо зламане посилання. Назву та пояснення можна вивчити нижче.</span>
 </div>;
 return <img src={src} alt={title} loading={large?"eager":"lazy"} onError={()=>setFailed(true)}
  className={large?"max-h-[72vh] w-full object-contain":"w-full h-56 object-contain p-3 transition-transform duration-300 group-hover:scale-[1.03]"} />;
}
function PhotoCard({item,index,quiz,revealed,onReveal,onOpen}:{item:HistoryPhoto;index:number;quiz:boolean;revealed:boolean;onReveal:()=>void;onOpen:()=>void}){
 const isVisible=!quiz||revealed;
 return <article className="rounded-3xl bg-white border border-slate-200 shadow-sm overflow-hidden hover:shadow-lg transition-shadow flex flex-col">
   <button type="button" onClick={onOpen} aria-label={`Збільшити фото: ${item.title}`} className="group relative w-full bg-gradient-to-br from-slate-50 to-amber-50/40 min-h-56 grid place-items-center">
     <ImageWithFallback src={item.src} title={item.title}/>
     <span className="absolute right-3 bottom-3 rounded-full bg-white/90 px-3 py-1.5 shadow text-xs font-bold text-slate-600 flex items-center gap-1"><Maximize2 size={13}/> Збільшити</span>
   </button>
   <div className="p-4 sm:p-5 flex-1 flex flex-col">
     <span className="uppercase tracking-wide text-[11px] font-extrabold text-amber-700">{item.group}</span>
     {isVisible ? <>
       <h2 className="font-black text-lg text-slate-900 mt-1">{item.title}</h2>
       <p className="text-sm text-slate-600 leading-relaxed mt-2 flex-1">{item.description}</p>
     </> : <>
       <h2 className="font-black text-lg text-slate-800 mt-1">Зображення №{index+1}</h2>
       <p className="text-sm text-slate-500 mt-2">Спробуй назвати людину або пам'ятку та пояснити, чим вона відома.</p>
       <button type="button" onClick={onReveal} className="mt-3 w-fit rounded-xl bg-orange-50 text-orange-700 text-sm font-bold px-4 py-2 hover:bg-orange-100">Показати відповідь</button>
     </>}
     <a href={item.source} target="_blank" rel="noopener noreferrer" className="mt-4 text-xs text-indigo-700 hover:underline flex gap-1 items-center w-fit">
       Джерело добірки: Освіта.ua <ExternalLink size={12}/>
     </a>
   </div>
 </article>;
}
function MapCard({item,quiz,revealed,onReveal,onOpen}:{item:VisualItem;quiz:boolean;revealed:boolean;onReveal:()=>void;onOpen:()=>void}){
 const note=getNote(item);
 if(!note)return null;
 const visible=!quiz||revealed;
 return <article className="rounded-3xl border border-amber-100 bg-white shadow-sm overflow-hidden md:flex hover:shadow-lg transition-shadow">
   <button type="button" onClick={onOpen} className="relative group bg-[#f6f3eb] w-full md:w-[52%] shrink-0 grid place-items-center p-3" aria-label={`Розгорнути карту: ${note.title}`}>
     <img src={item.src} alt={note.title} loading="lazy" className="w-full h-60 md:h-72 object-contain transition-transform duration-300 group-hover:scale-[1.025]" />
     <span className="absolute bottom-4 right-4 rounded-xl bg-white/90 px-3 py-2 text-xs font-bold text-amber-900 shadow flex items-center gap-2"><Maximize2 size={15}/> Відкрити велику карту</span>
   </button>
   <div className="p-5 md:p-6 flex flex-col gap-3">
     <span className="text-[11px] uppercase font-bold tracking-widest text-amber-700">{item.category==="timeline"?"Хронологічна стрічка":item.category==="maps"?"Історична картосхема":"Опорна схема"} · {PERIODS.find(p=>p.value===mapPeriod(item.src))?.label}</span>
     {visible ? <>
       <h2 className="font-black text-xl text-slate-900">{note.title}</h2>
       <p className="text-slate-700 text-sm leading-relaxed">{note.description}</p>
       <div className="bg-amber-50 border-l-4 border-amber-400 p-3 rounded-r-xl text-sm text-slate-800"><strong>Що запам'ятати:</strong> {note.tip}</div>
     </> : <>
       <h2 className="font-black text-xl text-slate-900">Упізнай тему карти</h2>
       <p className="text-sm text-slate-600">Спробуй визначити період, міста та події за умовними позначеннями.</p>
       <button type="button" onClick={onReveal} className="mt-2 w-fit rounded-xl bg-orange-50 text-orange-700 text-sm font-bold px-4 py-2 hover:bg-orange-100">Показати пояснення</button>
     </>}
   </div>
 </article>;
}

export default function HistoryAtlas(){
 const [tab,setTab]=useState<Tab>("figures");
 const [query,setQuery]=useState("");
 const [period,setPeriod]=useState("all");
 const [quiz,setQuiz]=useState(false);
 const [revealed,setRevealed]=useState<string[]>([]);
 const [opened,setOpened]=useState<OpenVisual|null>(null);
 const [zoom,setZoom]=useState(1);
 const q=query.toLocaleLowerCase("uk").trim();
 const photoItems=useMemo(()=>HISTORY_PHOTOS.filter(item=>
   (tab==="figures" ? item.category==="figures" : tab==="art" ? ["art","architecture"].includes(item.category) : item.category==="cinema") &&
   (`${item.title} ${item.group} ${item.description}`).toLocaleLowerCase("uk").includes(q)
 ),[tab,q]);
 const mapItems=useMemo(()=>HISTORY_VISUALS.filter(item=>{
   const n=getNote(item);
   if(!n)return false;
   if(period!=="all"&&mapPeriod(item.src)!==period)return false;
   return !q||(`${n.title} ${n.description} ${n.tip}`).toLocaleLowerCase("uk").includes(q);
 }),[period,q]);
 const currentCount=tab==="maps"?mapItems.length:photoItems.length;
 const openMap=(item:VisualItem)=>{
   const n=getNote(item);if(!n)return;
   setZoom(1);setOpened({src:item.src,title:n.title,description:n.description,tip:n.tip});
 };
 const openPhoto=(item:HistoryPhoto)=>{setZoom(1);setOpened({src:item.src,title:item.title,description:item.description});};
 const countFor=(key:Tab)=>key==="maps"?HISTORY_VISUALS.filter(item=>getNote(item)).length:
   HISTORY_PHOTOS.filter(item=>key==="figures"?item.category==="figures":key==="art"?["art","architecture"].includes(item.category):item.category==="cinema").length;
 return <main className="container mx-auto max-w-6xl px-4 py-6 min-h-screen">
   <Link href="/materials" className="inline-flex gap-2 items-center text-sm text-slate-500 hover:text-indigo-700 mb-5"><ArrowLeft size={16}/> Назад до матеріалів</Link>
   <header className="bg-gradient-to-br from-amber-600 via-orange-600 to-rose-600 rounded-3xl p-6 md:p-9 text-white shadow-xl overflow-hidden">
     <span className="uppercase tracking-widest text-xs font-bold text-amber-100">Візуальна підготовка до НМТ</span>
     <h1 className="font-black text-3xl md:text-5xl mt-2">Історія в кадрі</h1>
     <p className="text-sm md:text-base text-white/95 max-w-3xl mt-3 leading-relaxed">Фото та репродукції з <a className="font-extrabold underline underline-offset-2" href="https://osvita.ua/test/training/history/" target="_blank" rel="noopener noreferrer">добірок Освіта.ua для НМТ</a>, а також підписані карти, схеми та хронології з навчального банку сайту. Розпізнавай об'єкти одразу на сторінці, не переходячи за пошуковими посиланнями.</p>
     <p className="mt-3 text-xs text-white/80">Це навчальна добірка, що доповнюється, а не обіцянка показати всі можливі зображення на іспиті.</p>
   </header>
   <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mt-6" role="tablist" aria-label="Розділи атласу">
     {TABS.map(t=>{const Icon=t.icon; const active=t.id===tab; return <button type="button" role="tab" aria-selected={active} key={t.id}
      onClick={()=>{setTab(t.id);setQuery("");setRevealed([]);}} className={`rounded-2xl text-left p-4 border transition hover:shadow-md ${active?"border-orange-400 bg-orange-50 shadow-md":"border-slate-200 bg-white"}`}>
      <Icon size={23} className={active?"text-orange-600":"text-slate-500"}/>
      <strong className="mt-2 block text-slate-900 text-sm md:text-base">{t.title}</strong>
      <span className="block text-xs text-slate-600 mt-1">{t.subtitle}</span>
      <span className="block text-xs text-orange-700 font-bold mt-2">{countFor(t.id)} матеріалів</span>
     </button>})}
   </div>
   <div className="rounded-2xl border bg-white border-slate-200 mt-5 p-4 flex gap-3 flex-wrap items-center">
     <label className="relative grow min-w-[200px]">
       <Search size={18} className="absolute left-3 top-3 text-slate-400"/>
       <input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Пошук імен, дат, назв, міст…" className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 focus:outline-none focus:ring-2 focus:ring-orange-400"/>
     </label>
     {tab==="maps"&&<select value={period} onChange={e=>setPeriod(e.target.value)} aria-label="Історичний період"
       className="rounded-xl border border-slate-200 bg-slate-50 py-2.5 px-3 text-sm text-slate-700 max-w-full">
       {PERIODS.map(p=><option key={p.value} value={p.value}>{p.label}</option>)}
     </select>}
     <button type="button" onClick={()=>{setQuiz(v=>!v);setRevealed([]);}} aria-pressed={quiz}
       className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-bold ${quiz?"bg-orange-500 text-white":"bg-slate-100 text-slate-800 hover:bg-slate-200"}`}>
       {quiz?<Eye size={16}/>:<EyeOff size={16}/>} {quiz?"Режим перевірки: увімк.":"Приховати відповіді"}
     </button>
   </div>
   <div className="my-5 flex items-center justify-between text-sm text-slate-600">
     <span>Знайдено: <b className="text-slate-900">{currentCount}</b></span>
     <span className="text-slate-400 hidden sm:inline">Натисни на зображення, щоб збільшити</span>
   </div>
   {tab==="maps"?<section className="space-y-5">
     {mapItems.map(item=><MapCard key={item.id} item={item} quiz={quiz} revealed={revealed.includes(item.id)} onReveal={()=>setRevealed(r=>[...r,item.id])} onOpen={()=>openMap(item)}/>)}
   </section>:<section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
     {photoItems.map((item,i)=><PhotoCard key={item.src} item={item} index={i} quiz={quiz} revealed={revealed.includes(item.src)} onReveal={()=>setRevealed(r=>[...r,item.src])} onOpen={()=>openPhoto(item)}/>)}
   </section>}
   {currentCount===0&&<p className="text-center text-slate-500 py-14 bg-white rounded-2xl border border-slate-200">За цим запитом нічого не знайдено. Спробуй інше слово або період.</p>}
   <aside className="my-8 bg-indigo-50 rounded-2xl p-5 text-indigo-900 text-sm leading-relaxed">
     <div className="flex items-center gap-2 font-bold mb-2"><CheckCircle2 size={19}/> Як підготуватися</div>
     Спочатку впізнай зображення, а тоді поясни, <strong>хто / що це, коли й де відбувалася подія та з чим її пов'язують</strong>.
     Увімкни режим перевірки, щоб приховати підписи та згадати відповідь самостійно. Карти — спрощені навчальні картосхеми, а не історичні атласи з точними державними кордонами.
   </aside>
   {opened&&<div className="fixed inset-0 z-50 bg-slate-950/95 flex flex-col" role="dialog" aria-label={opened.title} aria-modal="true">
     <div className="p-3 sm:p-4 border-b border-white/20 text-white flex justify-between gap-3 items-center">
       <strong className="text-sm sm:text-lg truncate">{opened.title}</strong>
       <div className="flex items-center gap-2 shrink-0">
         <button type="button" onClick={()=>setZoom(z=>Math.max(1,z-0.5))} aria-label="Зменшити" className="p-2 rounded-xl hover:bg-white/10"><ZoomOut size={21}/></button>
         <span className="text-xs sm:text-sm w-10 text-center">{Math.round(zoom*100)}%</span>
         <button type="button" onClick={()=>setZoom(z=>Math.min(3,z+0.5))} aria-label="Збільшити" className="p-2 rounded-xl hover:bg-white/10"><ZoomIn size={21}/></button>
         <button type="button" onClick={()=>setOpened(null)} aria-label="Закрити" className="p-2 rounded-xl hover:bg-white/10"><X size={24}/></button>
       </div>
     </div>
     <div className="flex-1 min-h-0 overflow-auto flex items-start justify-center p-5">
       <div className="min-w-min mx-auto" style={{width:`${Math.round(zoom*100)}%`,maxWidth:zoom===1?"1200px":undefined}}>
         <ImageWithFallback key={opened.src} src={opened.src} title={opened.title} large/>
       </div>
     </div>
     <div className="p-4 sm:px-6 bg-slate-900 text-white text-sm border-t border-white/15">
       <p>{opened.description}</p>
       {opened.tip&&<p className="text-amber-200 mt-1"><strong>Запам'ятай:</strong> {opened.tip}</p>}
     </div>
   </div>}
 </main>;
}
