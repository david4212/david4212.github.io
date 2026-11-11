// Культура для НМТ: тільки твори, які прямо пов'язані з персоналіями
// та подіями шкільної програми / архівних завдань.
export type CultureWork = {
 title:string;
 category:"Кіно"|"Театр";
 year:string;
 author:string;
 director:string;
 studio?:string;
 script?:string;
 camera?:string;
 cast?:string;
 historicalContext:string;
 nmtHint:string;
 sourceUrl:string;
 examSourceUrl:string;
};
export const NMT_CULTURE_WORKS:CultureWork[]=[
 {
  title:"«Земля»",
  category:"Кіно",year:"1930",
  author:"Олександр Довженко",
  director:"Олександр Довженко",
  camera:"Данило Демуцький",
  historicalContext:"Німий художній фільм доби становлення українського кінематографа. У центрі — зміни селянського життя на тлі колективізації.",
  nmtHint:"Довженко → «Земля» (1930) → український кінематограф 1920–1930-х років. Данило Демуцький — оператор.",
  sourceUrl:"https://esu.com.ua/article-20465",
  examSourceUrl:"https://zno.osvita.ua/ukraine-history/tag-vizualne_vpiznannja/"
 },
 {
  title:"«Тіні забутих предків»",
  category:"Кіно",year:"1964 (зйомки), 1965 (київська прем’єра)",
  author:"Михайло Коцюбинський — автор однойменної повісті",
  director:"Сергій Параджанов",
  studio:"Київська кіностудія імені Олександра Довженка",
  script:"Сергій Параджанов, Іван Чендей",
  camera:"Юрій Іллєнко",
  cast:"Іван Миколайчук (Іван), Лариса Кадочникова (Марічка)",
  historicalContext:"Важливий зразок українського поетичного кіно. На київській прем'єрі 1965 року відбувся публічний протест проти арештів української інтелігенції.",
  nmtHint:"Параджанов → «Тіні забутих предків» → Іван Миколайчук, Лариса Кадочникова; оператор Юрій Іллєнко. Прем'єра 1965 року пов'язана з виступом шістдесятників.",
  sourceUrl:"https://www.kmu.gov.ua/news/248458887",
  examSourceUrl:"https://zno.osvita.ua/ukraine-history/tag-vizualne_vpiznannja/"
 },
 {
  title:"«Вавілон XX»",
  category:"Кіно",year:"1979",
  author:"Василь Земляк — роман «Лебедина зграя»",
  director:"Іван Миколайчук",
  studio:"Кіностудія імені Олександра Довженка",
  script:"Іван Миколайчук, Василь Земляк",
  camera:"Юрій Гармаш",
  cast:"Іван Миколайчук, Любов Поліщук, Борислав Брондуков, Анатолій Хостікоєв та інші",
  historicalContext:"Фільм за мотивами роману Василя Земляка. Важливий для вивчення творчого доробку Івана Миколайчука й українського поетичного кіно.",
  nmtHint:"Іван Миколайчук — не лише актор «Тіней забутих предків», а й режисер «Вавілону XX» (1979).",
  sourceUrl:"https://dovzhenkocentre.org/top-100/vavilon-xx/",
  examSourceUrl:"https://zno.osvita.ua/ukraine-history/tag-vizualne_vpiznannja/"
 },
 {
  title:"Театр «Березіль»",
  category:"Театр",year:"1922 — заснування у Києві; з 1926 — Харків",
  author:"Мистецьке об'єднання Леся Курбаса",
  director:"Лесь Курбас",
  historicalContext:"Експериментальний театр і осередок модернізації українського сценічного мистецтва у 1920-х роках.",
  nmtHint:"Лесь Курбас → «Березіль» → 1922 рік. Не плутай театр «Березіль» з «Молодим театром» доби Української революції.",
  sourceUrl:"https://tsdahou.archives.gov.ua/arhiv-vystavkovyh-proyektiv/vystavkovi-proyekty-czdago-ukrayiny/do-100-richchya-zasnuvannya-teatru-berezil-ta-135-yi-richnyczi-vid-dnya-narodzhennya-lesya-kurbasa/",
  examSourceUrl:"https://zno.osvita.ua/ukraine-history/tag-vizualne_vpiznannja/"
 }
];
