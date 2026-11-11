/* eslint-disable react/no-unescaped-entities, @next/next/no-img-element */
"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, ExternalLink, Map as MapIcon, Images, Landmark, Clapperboard, Search, Maximize2, Eye, EyeOff, X, CheckCircle2 } from "lucide-react";
import { VERIFIED_EXAM_MAPS } from "@/lib/verified-exam-maps";
import { NMT_CINEMA_PEOPLE } from "@/lib/history-cinema-people";
import VerifiedMapsPanel from "@/components/materials/VerifiedMapsPanel";
import CultureWorksPanel from "@/components/materials/CultureWorksPanel";
import { HISTORY_PHOTOS, type HistoryPhoto } from "@/lib/history-photos";
import { HISTORY_ARCHITECTURE } from "@/lib/history-architecture";
import { HISTORY_ARCHAEOLOGY } from "@/lib/history-archaeology";
import { HISTORY_ENTRY_DETAILS } from "@/lib/history-entry-details";

type Tab = "figures" | "maps" | "art" | "cinema";
type OpenVisual = {src:string;title:string;description:string;tip?:string;labels?:{number:number;label:string}[];period?:string;photo?:boolean;source?:string;category?:HistoryPhoto["category"];group?:string;recognition?:string;views?:string[];catalogNumber?:number};
const TABS: {id:Tab;title:string;subtitle:string;icon:typeof Images}[] = [
  {id:"figures",title:"Обличчя історії",subtitle:"Фото й портрети",icon:Images},
  {id:"maps",title:"Атлас подій",subtitle:"Карти, схеми, дати",icon:MapIcon},
  {id:"art",title:"Галерея епох",subtitle:"Архітектура й мистецтво",icon:Landmark},
  {id:"cinema",title:"Кіно й театр",subtitle:"Хто зняв, написав або зіграв",icon:Clapperboard}
];
function ImageWithFallback({src,title,large=false,fallbacks=[]}:{src:string;title:string;large?:boolean;fallbacks?:string[]}) {
 const [failedIndex,setFailedIndex]=useState(0);
 const candidates=[...new Set([src,...fallbacks])];
 if(failedIndex>=candidates.length)return <div role="img" aria-label={title} className="w-full min-h-48 p-6 flex flex-col items-center justify-center gap-2 bg-slate-100 text-center text-slate-600">
  <Images size={26} className="text-slate-400"/><strong className="text-sm">Зображення недоступне</strong>
  <span className="text-xs">Усі ракурси із джерела тимчасово не завантажуються. Назва й опис доступні нижче.</span>
 </div>;
 return <img src={candidates[failedIndex]} alt={title} loading={large?"eager":"lazy"} onError={()=>setFailedIndex(i=>i+1)}
  className={large?"max-h-[72vh] w-full object-contain":"w-full h-56 object-contain p-3 transition-transform duration-300 group-hover:scale-[1.03]"} />;
}
function PhotoCard({item,index,quiz,revealed,onReveal,onOpen}:{item:HistoryPhoto;index:number;quiz:boolean;revealed:boolean;onReveal:()=>void;onOpen:()=>void}){
 const isVisible=!quiz||revealed;
 return <article className="rounded-3xl bg-white border border-slate-200 shadow-sm overflow-hidden hover:shadow-lg transition-shadow flex flex-col">
   <button type="button" onClick={onOpen} aria-label={`Збільшити фото: ${item.title}`} className="group relative w-full bg-gradient-to-br from-slate-50 to-amber-50/40 min-h-56 grid place-items-center">
     <ImageWithFallback src={item.src} title={item.title} fallbacks={item.views}/>
     <span className="absolute right-3 bottom-3 rounded-full bg-white/90 px-3 py-1.5 shadow text-xs font-bold text-slate-600 flex items-center gap-1"><Maximize2 size={13}/> Збільшити</span>
   </button>
   <div className="p-4 sm:p-5 flex-1 flex flex-col">
     <span className="uppercase tracking-wide text-[11px] font-extrabold text-amber-700">{item.catalogNumber?`№${item.catalogNumber} · `:""}{item.group}</span>
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
export default function HistoryAtlas(){
 const [tab,setTab]=useState<Tab>("figures");
 const [query,setQuery]=useState("");
 const [artGroup,setArtGroup]=useState("all");
 const [quiz,setQuiz]=useState(false);
 const [revealed,setRevealed]=useState<string[]>([]);
 const [opened,setOpened]=useState<OpenVisual|null>(null);
 const q=query.toLocaleLowerCase("uk").trim();
 const photoItems=useMemo(()=>[
   ...(tab==="art"?[...HISTORY_ARCHAEOLOGY,...HISTORY_ARCHITECTURE]:[]),
   ...HISTORY_PHOTOS.filter(item=>tab==="figures"?item.category==="figures":tab==="art"?item.category==="art":item.category==="cinema"),
 ].filter(item=>(tab!=="art"||artGroup==="all"||(artGroup==="art"?item.category==="art":item.group===artGroup))&&(`${item.title} ${item.group} ${item.description} ${item.recognition||""}`).toLocaleLowerCase("uk").includes(q)),[tab,q,artGroup]);
 const currentCount=tab==="maps"?VERIFIED_EXAM_MAPS.filter(item=>(item.title+" "+item.period+" "+item.explanation).toLocaleLowerCase("uk").includes(q)).length:photoItems.length+(tab==="cinema"?NMT_CINEMA_PEOPLE.filter(person=>(person.name+" "+person.field+" "+person.focus+" "+person.works.map(w=>w.title+" "+w.role).join(" ")).toLocaleLowerCase("uk").includes(q)).length:0);
 const openPhoto=(item:HistoryPhoto)=>{setOpened({src:item.src,title:item.title,description:item.description,photo:true,source:item.source,category:item.category,group:item.group,recognition:item.recognition,views:item.views,catalogNumber:item.catalogNumber});};
 const countFor=(key:Tab)=>key==="maps"?VERIFIED_EXAM_MAPS.length:
   key==="art"?HISTORY_PHOTOS.filter(item=>item.category==="art").length+HISTORY_ARCHAEOLOGY.length+HISTORY_ARCHITECTURE.length:HISTORY_PHOTOS.filter(item=>key==="figures"?item.category==="figures":item.category==="cinema").length+(key==="cinema"?NMT_CINEMA_PEOPLE.length:0);
 return <main className="container mx-auto max-w-6xl px-4 py-6 min-h-screen">
   <Link href="/materials" className="inline-flex gap-2 items-center text-sm text-slate-500 hover:text-indigo-700 mb-5"><ArrowLeft size={16}/> Назад до матеріалів</Link>
   <header className="bg-gradient-to-br from-amber-600 via-orange-600 to-rose-600 rounded-3xl p-6 md:p-9 text-white shadow-xl overflow-hidden">
     <span className="uppercase tracking-widest text-xs font-bold text-amber-100">Візуальна підготовка до НМТ</span>
     <h1 className="font-black text-3xl md:text-5xl mt-2">Історія в кадрі</h1>
     <p className="text-sm md:text-base text-white/95 max-w-3xl mt-3 leading-relaxed">Фото та репродукції з <a className="font-extrabold underline underline-offset-2" href="https://osvita.ua/test/training/materialy-instrumenty/93357/" target="_blank" rel="noopener noreferrer">добірок Освіта.ua для НМТ</a>, а також підтверджені картосхеми з реальних НМТ/ЗНО. Саморобні карти та неперевірені схеми знято з показу. Розпізнавай об'єкти одразу на сторінці, не переходячи за пошуковими посиланнями.</p>
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
     {tab==="art"&&<select value={artGroup} onChange={e=>setArtGroup(e.target.value)} aria-label="Вид архітектури чи мистецтва"
       className="rounded-xl border border-slate-200 bg-slate-50 py-2.5 px-3 text-sm text-slate-700 max-w-full">
       <option value="all">Усі пам'ятки й мистецтво</option>
       <option value="Археологічні пам’ятки">Археологія · 6</option>
       <option value="Культові споруди">Культові споруди · 26</option>
       <option value="Фортифікаційні споруди">Фортифікації · 8</option>
       <option value="Світські споруди та містобудування">Світські будівлі · 10</option>
       <option value="art">Картини й графіка</option>
     </select>}
     <button type="button" onClick={()=>{setQuiz(v=>!v);setRevealed([]);}} aria-pressed={quiz}
       className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-bold ${quiz?"bg-orange-500 text-white":"bg-slate-100 text-slate-800 hover:bg-slate-200"}`}>
       {quiz?<Eye size={16}/>:<EyeOff size={16}/>} {quiz?"Режим перевірки: увімк.":"Приховати відповіді"}
     </button>
   </div>
   {tab==="art"&&<p className="text-sm text-slate-600 mt-4 leading-relaxed">6 археологічних пам’яток (зокрема скіфська пектораль і гребінь) та 44 архітектурні пам’ятки за списками Освіта.ua — 26 культових, 8 фортифікаційних та 10 світських. У картках доступний 91 ракурс із поясненнями, як упізнавати об’єкти. Окремо додані твори мистецтва. Для археологічних об’єктів є доба, місце знахідки й ознаки впізнавання.</p>}
   <div className="my-5 flex items-center justify-between text-sm text-slate-600">
     <span>Знайдено: <b className="text-slate-900">{currentCount}</b></span>
     <span className="text-slate-400 hidden sm:inline">Натисни на зображення, щоб збільшити</span>
   </div>
   {tab==="maps"?<VerifiedMapsPanel query={query} quiz={quiz}/>:<>
     {tab==="cinema"&&<CultureWorksPanel query={query}/>}
     <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
       {photoItems.map((item,i)=><PhotoCard key={item.src} item={item} index={i} quiz={quiz} revealed={revealed.includes(item.src)} onReveal={()=>setRevealed(r=>[...r,item.src])} onOpen={()=>openPhoto(item)}/>)}
     </section>
   </>}
   {currentCount===0&&<p className="text-center text-slate-500 py-14 bg-white rounded-2xl border border-slate-200">За цим запитом нічого не знайдено. Спробуй інше слово або період.</p>}
   <aside className="my-8 bg-indigo-50 rounded-2xl p-5 text-indigo-900 text-sm leading-relaxed">
     <div className="flex items-center gap-2 font-bold mb-2"><CheckCircle2 size={19}/> Як підготуватися</div>
     Спочатку впізнай зображення, а тоді поясни, <strong>хто / що це, коли й де відбувалася подія та з чим її пов'язують</strong>.
     Увімкни режим перевірки, щоб приховати підписи та згадати відповідь самостійно. У розділі карт залишено лише ілюстрації з підтвердженим екзаменаційним джерелом і перевіреною відповіддю.
   </aside>
   {opened?.photo&&<div role="dialog" aria-modal="true" aria-label={opened.title} className="fixed inset-0 z-[90] bg-slate-950/85 backdrop-blur-sm p-3 sm:p-6 flex items-center justify-center" onClick={()=>setOpened(null)}>
     <section className="bg-white rounded-3xl w-full max-w-6xl max-h-full overflow-hidden flex flex-col shadow-2xl" onClick={e=>e.stopPropagation()}>
       <header className="px-5 py-4 border-b border-slate-200 flex items-center justify-between gap-3">
         <div className="min-w-0"><p className="text-[11px] uppercase font-extrabold tracking-widest text-amber-700">{opened.group||"Візуальний довідник НМТ"}</p>
         <h2 className="text-xl sm:text-2xl font-black text-slate-900 truncate mt-1">{opened.title}</h2></div>
         <button type="button" onClick={()=>setOpened(null)} aria-label="Закрити картку" className="rounded-xl bg-slate-100 p-2.5 hover:bg-slate-200 text-slate-700 shrink-0"><X size={22}/></button>
       </header>
       <div className="overflow-y-auto min-h-0 grid grid-cols-1 md:grid-cols-2">
         <div className="bg-gradient-to-br from-[#e7e9e2] to-[#e6ddcd] p-5 sm:p-8 flex flex-col items-center justify-center min-h-[260px] md:min-h-[450px]">
           <div className="w-full max-w-lg rounded-2xl bg-white/70 p-3 sm:p-5 border border-[#cdbfa4] shadow-lg">
             <ImageWithFallback key={opened.src} src={opened.src} title={opened.title} large fallbacks={opened.views}/>
           </div>
           {opened.views&&opened.views.length>1&&<div className="mt-4 flex flex-wrap justify-center gap-2">
             {opened.views.map((src,i)=><button key={src} type="button" onClick={()=>setOpened(current=>current?{...current,src}:current)}
               className={`rounded-lg px-3 py-2 text-xs font-bold border transition ${opened.src===src?"bg-[#284d44] text-white border-[#284d44]":"bg-white text-[#425148] border-[#d8ccb6] hover:border-[#907e5c]"}`}>
               Ракурс {i+1}
             </button>)}
           </div>}
           <p className="text-xs text-[#636659] text-center mt-4">Оглянь портрет або пам'ятку. Порівняй із характерними ознаками справа.</p>
         </div>
         <div className="p-5 md:p-8 flex flex-col gap-5">
           <div><span className="text-xs font-extrabold tracking-widest uppercase text-orange-700">{opened.category==="figures"||opened.category==="cinema"?"Коротка біографія":opened.category==="architecture"?"Про пам'ятку":"Про твір мистецтва"}</span>
             <p className="text-slate-800 leading-relaxed text-sm sm:text-base mt-2">{HISTORY_ENTRY_DETAILS[opened.title]?.bio||opened.description}</p>
           </div>
           <div className="border-l-4 border-amber-500 bg-amber-50 rounded-r-2xl px-5 py-4">
             <p className="text-xs uppercase tracking-widest font-black text-amber-800">{opened.category==="architecture"||opened.category==="art"?"Як упізнати на фото":"Асоціації для НМТ"}</p>
             <p className="text-sm sm:text-base leading-relaxed text-slate-800 mt-2">{opened.recognition||HISTORY_ENTRY_DETAILS[opened.title]?.recognition||(opened.category==="figures"||opened.category==="cinema"?"Запам'ятай обличчя та пов'яжи його з ключовими датами і подіями. "+opened.description:"Звертай увагу на форму, силует, оздоблення й епоху. "+opened.description)}</p>
           </div>
           <div className="rounded-2xl bg-slate-50 border border-slate-100 p-4">
             <p className="text-sm font-bold text-slate-800">Перевір себе</p>
             <p className="text-sm text-slate-600 mt-1">Закрий підказки й назви, кого або що зображено, до якої епохи належить об'єкт і з якою подією пов'язаний.</p>
           </div>
           {opened.source&&<a href={opened.source} rel="noopener noreferrer" target="_blank" className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-700 hover:underline w-fit mt-auto">
             Джерело зображення та добірки <ExternalLink size={15}/>
           </a>}
         </div>
       </div>
     </section>
   </div>}
 </main>;
}
