"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, ExternalLink, Map, Images, Landmark, Clapperboard, Search, BookOpen, Maximize2 } from "lucide-react";
import { HISTORY_VISUALS, HISTORY_FIGURES, HISTORY_ART, HISTORY_CINEMA } from "@/lib/history-gallery";

type Category = "images" | "maps" | "art" | "cinema";
const tabs: { key: Category; name: string; info: string }[] = [
  { key: "images", name: "Фото й образи", info: "Персоналії, схеми та історичні об'єкти" },
  { key: "maps", name: "Атлас подій", info: "Картосхеми, території та хронологія" },
  { key: "art", name: "Галерея епох", info: "Архітектура, картини, ікони й скульптури" },
  { key: "cinema", name: "Кадри культури", info: "Кіно, театр, режисери та їхні роботи" },
];

function mediaSearch(title: string) {
  return "https://commons.wikimedia.org/w/index.php?search=" + encodeURIComponent(title + " Україна") + "&title=Special:MediaSearch&type=image";
}

export default function HistoryAtlas() {
  const [tab, setTab] = useState<Category>("images");
  const [query, setQuery] = useState("");
  const [opened, setOpened] = useState<string | null>(null);
  const [showHints, setShowHints] = useState(true);
  const q = query.trim().toLocaleLowerCase("uk");
  const assets = useMemo(() => HISTORY_VISUALS.filter(v =>
    (tab === "maps" ? v.category === "maps" || v.category === "timeline" : v.category === "visuals")
    && (v.title + " " + v.description + " " + v.src).toLocaleLowerCase("uk").includes(q)), [tab, q]);
  const knowledge = (tab === "art" ? HISTORY_ART : tab === "cinema" ? HISTORY_CINEMA : HISTORY_FIGURES)
    .filter(v => (v.title + " " + v.group + " " + v.hint).toLocaleLowerCase("uk").includes(q));
  const showAssets = tab === "maps" || tab === "images";
  const galleryTabs = tabs.map(t => ({...t, total: t.key === "maps"
    ? HISTORY_VISUALS.filter(v => v.category !== "visuals").length
    : t.key === "images" ? HISTORY_VISUALS.filter(v => v.category === "visuals").length + HISTORY_FIGURES.length
    : t.key === "art" ? HISTORY_ART.length : HISTORY_CINEMA.length }));

  return (
    <main className="container mx-auto max-w-6xl px-4 py-7 min-h-screen">
      <Link href="/materials" className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-indigo-700 mb-6"><ArrowLeft size={16} /> До матеріалів</Link>
      <div className="rounded-3xl p-6 md:p-9 bg-gradient-to-br from-amber-600 via-orange-600 to-rose-600 text-white shadow-xl overflow-hidden relative">
        <span className="text-xs uppercase font-bold tracking-widest text-amber-100">Історія України · візуальна підготовка</span>
        <h1 className="text-3xl md:text-5xl font-black mt-2">Історія в кадрі</h1>
        <p className="mt-3 max-w-2xl text-white/90">Розпізнавай карти, пам'ятки мистецтва, історичних діячів і творців кіно. Вивчай підписи, потім приховуй підказки й перевіряй себе.</p>
        <p className="text-xs text-amber-100 mt-4">Це навчальна добірка, а не вичерпний офіційний перелік зображень НМТ.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6" role="tablist" aria-label="Візуальні розділи історії">
        {galleryTabs.map((t, i) => {
          const Icon = [Images, Map, Landmark, Clapperboard][i];
          return <button key={t.key} type="button" role="tab" aria-selected={tab===t.key}
            onClick={() => {setTab(t.key); setOpened(null); setQuery("");}}
            className={`rounded-2xl p-4 border text-left transition hover:shadow-md ${tab === t.key ? "bg-amber-50 border-amber-400 shadow-md" : "bg-white border-slate-200"}`}>
            <Icon size={23} className={tab===t.key?"text-orange-600":"text-slate-500"} />
            <span className="font-extrabold text-slate-900 mt-2 block text-sm md:text-base">{t.name}</span>
            <span className="text-xs text-slate-500 block mt-1">{t.total} матеріалів</span>
          </button>;
        })}
      </div>
      <div className="bg-white rounded-2xl border border-slate-200 p-4 my-5 flex flex-wrap items-center gap-4">
        <label className="relative flex-1 min-w-[210px]">
          <Search size={18} className="absolute left-3 top-3 text-slate-400" />
          <input className="w-full rounded-xl bg-slate-50 py-2.5 pl-10 pr-3 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-amber-400"
            value={query} onChange={e=>setQuery(e.target.value)} placeholder="Шукати за назвою або епохою..." />
        </label>
        <label className="flex gap-2 items-center text-sm text-slate-700 cursor-pointer">
          <input type="checkbox" checked={showHints} onChange={e=>setShowHints(e.target.checked)} className="accent-orange-600 w-4 h-4" />
          Показувати підписи
        </label>
      </div>
      <p className="text-slate-500 text-sm mb-4">{tabs.find(t=>t.key===tab)?.info}. Знайдено: {showAssets ? assets.length + (tab === "images" ? knowledge.length : 0) : knowledge.length}.</p>

      {showAssets && <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        {assets.map(item => <article key={item.id} className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-lg transition">
          <button type="button" onClick={()=>setOpened(item.src)} aria-label={`Відкрити зображення: ${item.title}`}
            className="block w-full bg-slate-50 relative group">
            <img src={item.src} alt={item.title} loading="lazy" className="w-full h-48 object-contain p-3" />
            <Maximize2 className="absolute right-3 bottom-3 text-slate-600 opacity-0 group-hover:opacity-100" size={19} />
          </button>
          <div className="p-4">
            <span className="text-[11px] font-extrabold text-orange-700 uppercase">{item.category==="maps"?"Карта":item.category==="timeline"?"Хронологія":"Схема"}</span>
            {showHints ? <><h2 className="font-extrabold mt-1 text-slate-900">{item.title}</h2><p className="text-sm mt-1 text-slate-600">{item.description}</p></>
              : <p className="text-sm mt-2 font-semibold text-slate-600">Спробуй назвати подію, дату або об'єкт самостійно.</p>}
          </div>
        </article>)}
      </section>}

      {(tab!=="maps") && <section>
        {tab==="images" && <h2 className="font-extrabold text-xl text-slate-900 mt-4 mb-4">Впізнай історичну постать</h2>}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {knowledge.map((item,i) => <article key={item.title} className="rounded-2xl bg-white border border-slate-200 p-5">
            <div className="flex gap-3 items-start justify-between">
              <div><span className="text-xs font-bold text-amber-700">{item.group}</span><h3 className="font-extrabold text-slate-900 text-lg mt-1">{showHints ? item.title : `Об'єкт №${i+1}`}</h3></div>
              <BookOpen className="text-orange-500 shrink-0" size={20}/>
            </div>
            {showHints && <p className="text-sm text-slate-600 mt-2">{item.hint}</p>}
            <a href={mediaSearch(item.title)} target="_blank" rel="noopener noreferrer" className="mt-4 inline-flex gap-1.5 items-center text-sm font-bold text-indigo-700 hover:underline">
              Переглянути зображення на Wikimedia Commons <ExternalLink size={13}/>
            </a>
          </article>)}
        </div>
      </section>}

      {showAssets && assets.length===0 && (tab==="maps" || knowledge.length===0) && <p className="p-8 text-center text-slate-500">За цим пошуком нічого не знайдено.</p>}

      <aside className="my-8 rounded-2xl bg-indigo-50 p-5 text-sm text-indigo-900">
        <strong>Як займатися:</strong> спочатку роздивись зображення й прочитай опис. Потім вимкни «Показувати підписи», спробуй назвати епоху, місце й подію та знову увімкни підказки.
        <p className="mt-2">У вкладках із персоналіями й мистецтвом наведено зовнішній пошук зображень на Wikimedia Commons; самі фотокопії цих об'єктів поки не зберігаються на сайті.</p>
      </aside>
      {opened && <div role="dialog" aria-modal="true" aria-label="Збільшене зображення" onClick={()=>setOpened(null)}
        className="fixed inset-0 z-50 bg-slate-950/90 p-4 md:p-10 flex items-center justify-center cursor-zoom-out">
        <button type="button" onClick={()=>setOpened(null)} className="absolute top-4 right-5 text-white text-3xl" aria-label="Закрити">×</button>
        <img src={opened} alt="Збільшена історична ілюстрація" className="max-h-full max-w-full object-contain" />
      </div>}
    </main>
  );
}
