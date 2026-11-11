import type { VerifiedExamMap } from "@/lib/history-review";

/**
 * This is a whitelist, NOT a generated map catalog.
 * Add a map only after checking its image, original examination, year,
 * question number and answer together.
 * Images are loaded directly from the archival display source, never copied
 * to this repository. The official UCEQA document is linked for comparison.
 */
export const VERIFIED_EXAM_MAPS: (VerifiedExamMap & {periodKey:string;officialUrl:string;answer:string})[] = [
  {
    id:"nmt-2024-demo-8-sugar",
    title:"Промислові райони українських земель",
    period:"Кінець XIX — початок XX ст.",
    periodKey:"h4",
    sourceName:"НМТ-2024 · демонстраційний варіант · завдання 8",
    sourceType:"official",
    examYear:2024,
    questionNumber:8,
    sourceUrl:"https://zno.osvita.ua/ukraine-history/571/",
    officialUrl:"https://testportal.gov.ua/wp-content/uploads/2024/02/NMT_2024-Ist_Ukr-Demo_sajt.pdf#page=4",
    imageUrl:"https://r2.cdn.miyklas.com.ua/79e266a7-9b2f-406f-a229-7473d6f911a8/%D1%968w800.png",
    key:"Знайди на мапі Правобережжя: Київщина й Поділля, на відміну від нафтової Галичини, промислового Донбасу та степового Півдня.",
    answer:"2",
    explanation:"Позначка 2 — Правобережжя, район товарного виробництва цукру наприкінці XIX — на початку XX століття. 1 — нафтовидобуток у Галичині, 3 — вугільно-металургійний Донбас, 4 — зернове господарство степового Півдня. Розташування та відповідь звірені з демонстраційним тестом УЦОЯО й поясненням архіву ЗНО."
  }
];

export const HISTORY_MAP_SOURCE_COLLECTIONS = [
  {
    title:"Оригінальні карти НМТ — тематична добірка",
    description:"Зразки з реальних варіантів, згруповані за історичними періодами; перед перенесенням кожну карту потрібно звірити з відповіддю.",
    url:"https://osvita.ua/test/training/materialy-instrumenty/97873/"
  },
  {
    title:"Карти (мапи) — тренажер регіонального центру оцінювання",
    description:"Тренувальні картографічні питання з авторськими поясненнями після вибору відповіді.",
    url:"https://lv.testportal.gov.ua/traneeHistory/edusite/maps.html"
  },
  {
    title:"Архів тестів з історії України",
    description:"Реальні завдання попередніх років, за якими можна перевірити джерело, формулювання та правильну відповідь.",
    url:"https://zno.osvita.ua/ukraine-history/"
  }
];
