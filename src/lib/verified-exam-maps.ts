import type { VerifiedExamMap } from "@/lib/history-review";

/**
 * 8 original images from published 2025 NMT tasks, with answer key and legends
 * copied as facts after cross-checking the archive explanations.
 * URLs are direct image references from the archived exercises.
 */
export const VERIFIED_EXAM_MAPS: (VerifiedExamMap & {periodKey:string;officialUrl:string;answer:string})[] = [
  {
    "id": "nmt-2025-demo-10-sugar",
    "title": "Цукробуряковий район Наддніпрянщини",
    "period": "Кінець XIX — початок XX ст.",
    "periodKey": "h4",
    "sourceName": "НМТ-2025 · демоваріант · завдання 10",
    "sourceType": "official",
    "examYear": 2025,
    "questionNumber": 10,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/628/",
    "officialUrl": "https://osvita.ua/doc/files/news/937/93721/NMT_2025_Istoriya_demo_sajt_1.pdf",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/321/32148/history-demo-2025-10.png",
    "key": "На карті треба впізнати район товарного виробництва цукру: це Правобережна Україна, особливо Київщина й Поділля.",
    "answer": "Б — цифра 2",
    "explanation": "Згідно з оприлюдненим розбором демоваріанта №10, цифра 2 — Правобережжя, регіон цукробурякового господарства; на зображенні потрібно визначити саме його, не плутати з нафтовою Галичиною (1), Донбасом (3) або зерновим Півднем (4).",
    "legend": [
      "1 — нафтовидобуток і озокерит у Передкарпатті",
      "2 — цукрова промисловість Правобережжя",
      "3 — вугілля і металургія Донбасу",
      "4 — товарне зернове господарство Півдня"
    ]
  },
  {
    "id": "nmt-2025-session1-3-roman",
    "title": "Галицько-Волинська держава за Романа Мстиславовича",
    "period": "1199 — початок XIII ст.",
    "periodKey": "early",
    "sourceName": "НМТ-2025 · 1-ша сесія · завдання 3",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 3,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/669/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/669/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34313/history-nmt-25-1-sessiya-03.png",
    "key": "Крім Галичини й Волині, на картосхемі позначені залежні Київське та Переяславське князівства: це підказка до правління Романа Мстиславовича.",
    "answer": "Б — Роман Мстиславович",
    "explanation": "1199 року Роман Мстиславович об’єднав Галицьке та Волинське князівства; його влада згодом поширилася на Київ та Переяслав. Лев Данилович і Юрій II Болеслав не контролювали цих земель у показаному обсязі.",
    "legend": [
      "Позначено Галицько-Волинську державу",
      "Київське й Переяславське князівства — залежні території",
      "Ключова дата об’єднання Галичини та Волині — 1199 рік"
    ]
  },
  {
    "id": "nmt-2025-session1-11-economy",
    "title": "Два аграрні райони українських земель",
    "period": "XIX століття",
    "periodKey": "h4",
    "sourceName": "НМТ-2025 · 1-ша сесія · завдання 11",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 11,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/669/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/669/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34321/history-nmt-25-1-sessiya-11.png",
    "key": "Знайди два райони інтенсивних аграрних змін XIX ст.: Правобережжя (цукрові буряки) і Південь (товарне зерно).",
    "answer": "Б — 2 і 4",
    "explanation": "Правобережжя розвивало буряківництво й цукроваріння (2), Південь — торговельне зернове господарство та експорт через чорноморські порти (4). Інші позначення стосуються насамперед нафтовидобутку й важкої промисловості.",
    "legend": [
      "2 — Правобережжя: товарне вирощування цукрового буряку",
      "4 — Південь: товарне зернове господарство",
      "1 і 3 — промислові спеціалізації, не відповідь"
    ]
  },
  {
    "id": "nmt-2025-session2-2-monomakh",
    "title": "Походи князів проти половців",
    "period": "Початок XII ст., зокрема 1103–1111 рр.",
    "periodKey": "early",
    "sourceName": "НМТ-2025 · 2-га сесія · завдання 2",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 2,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34342/history-nmt-25-2-sessiya-02.png",
    "key": "Стрілки спрямовані із руських князівств до половецького степу. Це об’єднані походи проти половців, організовані за участі Володимира Мономаха.",
    "answer": "Б — Володимир Мономах",
    "explanation": "На картосхемі показано походи руських військ проти половців. Володимир Мономах був ініціатором і учасником успішних походів 1103–1111 рр.; не плутай ці кампанії з подіями XII–XIII ст. у Галичині.",
    "legend": [
      "Стрілки — напрямки походів руських князів у степ",
      "Половецький степ — території кочовиків",
      "1103–1111 рр. — успішні антиполовецькі походи"
    ]
  },
  {
    "id": "nmt-2025-session2-25-zboriv",
    "title": "Зборівський договір: землі Гетьманщини",
    "period": "1649 рік",
    "periodKey": "h3",
    "sourceName": "НМТ-2025 · 2-га сесія · завдання 25 · карта А",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 25,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34365/ansa_34365.png",
    "key": "Карта А — територія Гетьманщини після Зборівського договору 1649 року, що охоплювала три воєводства: Київське, Чернігівське й Брацлавське.",
    "answer": "А — 1-ша за хронологією",
    "explanation": "Послідовність чотирьох карт у тесті: А (Зборів 1649) → Г (Біла Церква 1651) → В (Гадяч 1658) → Б (володіння Мазепи до 1704). Підпис А означає варіант картосхеми, а не правильну відповідь на одиничне питання.",
    "legend": [
      "1649 р. — Зборівська угода",
      "Київське, Чернігівське та Брацлавське воєводства",
      "Перший етап у завданні на хронологію"
    ]
  },
  {
    "id": "nmt-2025-session2-25-bilatserkva",
    "title": "Білоцерківський договір: скорочення Гетьманщини",
    "period": "1651 рік",
    "periodKey": "h3",
    "sourceName": "НМТ-2025 · 2-га сесія · завдання 25 · карта Г",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 25,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34365/ansd_34365.png",
    "key": "Карта Г — територію Гетьманщини обмежено переважно Київським воєводством за Білоцерківською угодою 1651 року.",
    "answer": "Г — 2-га за хронологією",
    "explanation": "Після поразки в Берестецькій битві 1651 року Білоцерківський договір звузив контрольовану Гетьманщиною територію до Київського воєводства. У початковій задачі вона є другою картосхемою.",
    "legend": [
      "1651 р. — Білоцерківський договір",
      "Гетьманщина обмежена Київським воєводством",
      "Другий етап у послідовності А → Г → В → Б"
    ]
  },
  {
    "id": "nmt-2025-session2-25-hadiach",
    "title": "Гадяцька угода: проєкт Великого князівства Руського",
    "period": "1658 рік",
    "periodKey": "h3",
    "sourceName": "НМТ-2025 · 2-га сесія · завдання 25 · карта В",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 25,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34365/ansc_34365.png",
    "key": "Карта В — проєкт Великого князівства Руського за Гадяцькою угодою 1658 року в межах трьох українських воєводств.",
    "answer": "В — 3-тя за хронологією",
    "explanation": "Гадяцька угода 1658 року передбачала Велике князівство Руське в складі Речі Посполитої як третій суб’єкт федерації; проєкт не був реалізований повністю. Це третя схема в послідовності.",
    "legend": [
      "1658 р. — Гадяцька угода",
      "Проєкт Великого князівства Руського",
      "Київське, Чернігівське, Брацлавське воєводства"
    ]
  },
  {
    "id": "nmt-2025-session2-25-mazepa",
    "title": "Землі під владою Івана Мазепи до 1704 року",
    "period": "Кінець XVII — початок XVIII ст.",
    "periodKey": "h3",
    "sourceName": "НМТ-2025 · 2-га сесія · завдання 25 · карта Б",
    "sourceType": "exam_archive",
    "examYear": 2025,
    "questionNumber": 25,
    "sourceUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "officialUrl": "https://zno.osvita.ua/ukraine-history/670/",
    "imageUrl": "https://zno.osvita.ua/doc/images/znotest/343/34365/ansb_34365.png",
    "key": "Карта Б — території влади гетьмана Івана Мазепи до 1704 р.: Лівобережна Україна та Київ.",
    "answer": "Б — 4-та за хронологією",
    "explanation": "Картосхема показує Гетьманщину наприкінці XVII — на початку XVIII ст. У завданні 25 вона остання, після 1649, 1651 та 1658 років.",
    "legend": [
      "Лівобережна Гетьманщина та Київ",
      "До 1704 року (до поширення влади Мазепи на частину Правобережжя)",
      "Четвертий етап у завданні А → Г → В → Б"
    ]
  }
];

export const HISTORY_MAP_SOURCE_COLLECTIONS = [
 {title:"Опубліковані завдання НМТ-2025: демоваріант",description:"Офіційний тест і правильні відповіді до завдань з картами.",url:"https://zno.osvita.ua/ukraine-history/628/"},
 {title:"Опубліковані завдання НМТ-2025: перша сесія",description:"Завдання з Галицько-Волинською державою й економічними регіонами.",url:"https://zno.osvita.ua/ukraine-history/669/"},
 {title:"Опубліковані завдання НМТ-2025: друга сесія",description:"Походи проти половців та чотири картосхеми території Гетьманщини.",url:"https://zno.osvita.ua/ukraine-history/670/"}
];
