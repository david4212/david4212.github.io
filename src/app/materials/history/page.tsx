/* eslint-disable react/no-unescaped-entities, @next/next/no-img-element */
"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, ExternalLink, Map as MapIcon, Images, Landmark, Clapperboard, Search, Maximize2, Eye, EyeOff, BookOpen, ZoomIn, ZoomOut, X, CheckCircle2 } from "lucide-react";
import { HISTORY_VISUALS, type VisualItem } from "@/lib/history-gallery";
import { HISTORY_MAP_NOTES, type MapNote } from "@/lib/history-map-notes";
import { getAtlasLabels, getAtlasPeriod } from "@/lib/history-atlas-legends";
import { HISTORY_PHOTOS, type HistoryPhoto } from "@/lib/history-photos";

type Tab = "figures" | "maps" | "art" | "cinema";
type OpenVisual = {src:string;title:string;description:string;tip?:string;labels?:{number:number;label:string}[];period?:string};
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
 const labels=getAtlasLabels(item.src);
 const period=getAtlasPeriod(item.src);
 const isMap=item.category==="maps";
 return <article className="overflow-hidden rounded-3xl bg-[#fffcf2] border border-[#d8cbb0] shadow-md hover:shadow-xl transition-shadow">
   <header className="relative flex flex-wrap items-center justify-between gap-3 px-5 md:px-7 py-5 bg-[#213f3b] text-[#fff8e7]">
     <div>
       <p className="text-[11px] font-bold tracking-[0.17em] text-[#e6cea0] uppercase">Історичний атлас · {period} · НМТ</p>
       <h2 className="text-xl md:text-2xl font-black mt-2 tracking-tight">{visible?note.title:"Упізнай історичну картосхему"}</h2>
     </div>
     <span className="rounded-full border border-[#b8a26e] bg-[#34584d] text-[#fce9c8] px-3 py-1.5 text-xs font-bold">{isMap?"КАРТА":item.category==="timeline"?"ХРОНОЛОГІЯ":"СХЕМА"}</span>
   </header>
   <div className="lg:grid lg:grid-cols-[minmax(0,1.65fr)_minmax(285px,1fr)]">
     <div className="relative bg-[#e8e9df] p-3 md:p-5 border-b lg:border-b-0 lg:border-r border-[#d9c9ad]">
       <div className="relative rounded-xl border-2 border-[#9f977e] bg-[#e1ece7] p-2 md:p-4 shadow-inner overflow-hidden">
         <button type="button" onClick={onOpen} aria-label={`Відкрити карту: ${note.title}`} className="group w-full block relative text-left">
           <img src={item.src} alt={note.title} loading="lazy" className="block w-full h-auto object-contain rounded-md sepia-[.08] saturate-[.78] contrast-[1.08] group-hover:scale-[1.015] transition-transform duration-300" />
           <span className="absolute right-2 bottom-2 rounded-xl bg-white/90 px-3 py-2 text-xs font-bold text-[#27443a] shadow flex gap-2 items-center"><Maximize2 size={15}/> Відкрити велику карту</span>
         </button>
         <div aria-hidden="true" className="absolute top-2 right-2 flex flex-col items-center justify-center w-10 h-14 text-[#284b44] pointer-events-none bg-[#f8f4e9]/90 rounded-lg border border-[#c9c3ab]">
           <span className="text-sm font-black leading-none">Пн</span>
           <span className="text-lg leading-none">↑</span>
         </div>
       </div>
       <p className="flex gap-2 items-start text-xs leading-relaxed mt-3 px-1 text-[#626355]"><span aria-hidden="true">◈</span> Географічна основа — сучасний контур України для орієнтування; це не історичний державний кордон. Масштаб умовний.</p>
     </div>
     <div className="flex flex-col p-5 md:p-6 bg-[#fffdf7]">
       {visible?<>
         <h3 className="font-extrabold text-xs tracking-[0.14em] uppercase text-[#94713e] pb-3 border-b-2 border-[#cfb988]">Умовні позначення</h3>
         {labels.length>0?<ol className="my-4 space-y-3">
           {labels.map(({number,label})=><li key={number} className="flex gap-3 items-center">
             <span className="grid shrink-0 size-9 place-items-center rounded-full bg-[#284d44] text-white font-black text-sm shadow-sm">{number}</span>
             <span className="font-semibold text-[#30423d] text-sm md:text-base">{label}</span>
           </li>)}
         </ol>:<p className="mt-4 text-sm text-[#58665c] leading-relaxed">Цифри на цій схемі позначають події або установи. Їх розшифрування наведено у поясненні нижче.</p>}
         {labels.length>0&&labels.length<4&&<p className="text-xs mt-1 text-[#766851]">Підписано лише позначки, що вдалося однозначно звірити із завданнями.</p>}
       </>:<>
         <h3 className="font-extrabold text-xs tracking-[0.14em] uppercase text-[#94713e] pb-3 border-b-2 border-[#cfb988]">Самоперевірка</h3>
         <p className="mt-4 text-sm text-[#4c554c] leading-relaxed">Подивися на цифри й географічні орієнтири. Назви кожне місто або територію, епоху та пов'язану подію.</p>
         <button type="button" onClick={onReveal} className="mt-5 w-fit rounded-xl px-4 py-2.5 bg-[#284d44] text-white font-bold text-sm hover:bg-[#1c3933]">Показати легенду й пояснення</button>
       </>}
       <div className="mt-auto pt-4 border-t border-[#e3dbc8]">
         <p className="flex items-center gap-2 text-xs text-[#847554] font-extrabold uppercase tracking-wide"><BookOpen size={15}/> Як читати карту</p>
         <p className="mt-2 text-sm text-[#43564e] leading-relaxed">{visible?note.description:"Спершу назви позначені об'єкти, а потім поясни їхній зв'язок із темою."}</p>
       </div>
     </div>
   </div>
   {visible&&<footer className="bg-[#f3e6cc] border-t border-[#dbcaac] p-4 md:px-7 text-sm text-[#5b492f] leading-relaxed">
     <strong className="text-[#80612d]">Запам'ятай до НМТ: </strong>{note.tip}
   </footer>}
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
   setZoom(1);setOpened({src:item.src,title:n.title,description:n.description,tip:n.tip,labels:getAtlasLabels(item.src),period:getAtlasPeriod(item.src)});
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
       {opened.period&&<p className="text-amber-200 text-xs font-semibold mb-2">Атлас · {opened.period}</p>}
       {opened.labels&&opened.labels.length>0&&<div className="flex flex-wrap gap-x-4 gap-y-2 pb-2">{opened.labels.map(v=><span key={v.number} className="font-bold text-sm"><span className="text-[#eac984]">{v.number}.</span> {v.label}</span>)}</div>}
       <p>{opened.description}</p>
       {opened.tip&&<p className="text-amber-200 mt-1"><strong>Запам'ятай:</strong> {opened.tip}</p>}
     </div>
   </div>}
 </main>;
}
