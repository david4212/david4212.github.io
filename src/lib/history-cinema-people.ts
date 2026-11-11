/**
 * Source-led person -> work -> exact role index for NMT history.
 * "основне": frequently appears in NMT/ZNO study materials and exam practice.
 * "контекст": useful associated works, not claimed as mandatory exam items.
 * This is not a copyright reproduction of any exam exercise.
 */
export type CulturePerson = {
 name: string; period:string; field:string; focus:string;
 works:{title:string; year:string; role:string; level:"основне"|"контекст"; fact:string;}[];
 sources:string[];
};
export const NMT_CINEMA_PEOPLE:CulturePerson[] = [
  {
    "name": "Олександр Довженко",
    "period": "1920–1950-ті",
    "field": "Кінорежисер, сценарист, письменник",
    "focus": "Автор трилогії «Звенигора» — «Арсенал» — «Земля». Не називай кіноповість «Україна в огні» знятим за його життя фільмом.",
    "works": [
      {
        "title": "«Звенигора»",
        "year": "1928",
        "role": "Режисер",
        "level": "основне",
        "fact": "Кіноепопея з образами української історії."
      },
      {
        "title": "«Арсенал»",
        "year": "1929",
        "role": "Режисер",
        "level": "основне",
        "fact": "Фільм про революційну добу в Києві."
      },
      {
        "title": "«Земля»",
        "year": "1930",
        "role": "Режисер і сценарист",
        "level": "основне",
        "fact": "Німий фільм; найвідоміша робота режисера."
      },
      {
        "title": "«Україна в огні»",
        "year": "1943",
        "role": "Автор кіноповісті (не готовий фільм)",
        "level": "контекст",
        "fact": "Твір, за який Довженка критикувало сталінське керівництво."
      }
    ],
    "sources": [
      "https://zno.osvita.ua/ukraine-history/all/1525/",
      "https://suspilne.media/culture/142099-100-najkrasih-filmiv-v-istorii-ukrainskogo-kino-rejting-dovzenko-centru/"
    ]
  },
  {
    "name": "Сергій Параджанов",
    "period": "1960-ті",
    "field": "Режисер українського поетичного кіно",
    "focus": "«Тіні забутих предків» — режисер Параджанов, оператор Юрій Іллєнко, головний актор Іван Миколайчук.",
    "works": [
      {
        "title": "«Тіні забутих предків»",
        "year": "1964 (виробництво), 1965 (прем’єра)",
        "role": "Режисер",
        "level": "основне",
        "fact": "Екранізація повісті Михайла Коцюбинського; фільм став символом українського поетичного кіно."
      }
    ],
    "sources": [
      "https://zno.osvita.ua/ukraine-history/all/260/",
      "https://suspilne.media/culture/142099-100-najkrasih-filmiv-v-istorii-ukrainskogo-kino-rejting-dovzenko-centru/"
    ]
  },
  {
    "name": "Іван Миколайчук",
    "period": "1960–1980-ті",
    "field": "Актор, режисер, сценарист",
    "focus": "Особливо запам’ятай різні ролі: «Тіні забутих предків» — грав, «Білий птах...» — грав і писав сценарій, «Вавілон ХХ» — режисер.",
    "works": [
      {
        "title": "«Тіні забутих предків»",
        "year": "1964/1965",
        "role": "Актор: Іван Палійчук",
        "level": "основне",
        "fact": "Головна роль у фільмі Сергія Параджанова."
      },
      {
        "title": "«Сон»",
        "year": "1964",
        "role": "Актор: молодий Тарас Шевченко",
        "level": "контекст",
        "fact": "Режисер Володимир Денисенко."
      },
      {
        "title": "«Білий птах з чорною ознакою»",
        "year": "1970/1971",
        "role": "Співавтор сценарію, актор: Петро Дзвонар",
        "level": "основне",
        "fact": "Режисер — Юрій Іллєнко; роль Ореста виконав Богдан Ступка."
      },
      {
        "title": "«Пропала грамота»",
        "year": "1972",
        "role": "Актор",
        "level": "контекст",
        "fact": "Режисер Борис Івченко."
      },
      {
        "title": "«Вавілон ХХ»",
        "year": "1979",
        "role": "Режисер і актор",
        "level": "основне",
        "fact": "Екранізація за мотивами «Лебединої зграї» Василя Земляка."
      }
    ],
    "sources": [
      "https://vue.gov.ua/%D0%9C%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D0%B9%D1%87%D1%83%D0%BA%2C_I%D0%B2%D0%B0%D0%BD_%D0%92%D0%B0%D1%81%D0%B8%D0%BB%D1%8C%D0%BE%D0%B2%D0%B8%D1%87",
      "https://usfa.gov.ua/movie-catalog/bilyy-ptakh-z-chornoyu-oznakoyu-i9173",
      "https://online.dovzhenkocentre.org/film_collections/ukrayinske-poetychne-kino/"
    ]
  },
  {
    "name": "Юрій Іллєнко",
    "period": "1960–1970-ті",
    "field": "Кінорежисер, кінооператор",
    "focus": "«Тіні забутих предків» — оператор Іллєнко, але режисер Параджанов; «Білий птах...» — режисер Іллєнко.",
    "works": [
      {
        "title": "«Тіні забутих предків»",
        "year": "1964/1965",
        "role": "Оператор-постановник",
        "level": "основне",
        "fact": "Фільм зняв Сергій Параджанов."
      },
      {
        "title": "«Криниця для спраглих»",
        "year": "1965",
        "role": "Режисер",
        "level": "основне",
        "fact": "Стрічка зазнала цензурних обмежень."
      },
      {
        "title": "«Вечір на Івана Купала»",
        "year": "1968",
        "role": "Режисер",
        "level": "контекст",
        "fact": "Приклад українського поетичного кіно."
      },
      {
        "title": "«Білий птах з чорною ознакою»",
        "year": "1970/1971",
        "role": "Режисер, співавтор сценарію",
        "level": "основне",
        "fact": "Співавтор сценарію — Іван Миколайчук, Богдан Ступка зіграв Ореста."
      }
    ],
    "sources": [
      "https://usfa.gov.ua/movie-catalog/bilyy-ptakh-z-chornoyu-oznakoyu-i9173",
      "https://suspilne.media/culture/755027-lapas-imperskij-politici-ta-personalna-koliivsina-pro-so-znimav-urij-illenko/"
    ]
  },
  {
    "name": "Леонід Биков",
    "period": "1970-ті",
    "field": "Актор і режисер",
    "focus": "«У бій ідуть тільки „старі“» (1973) — зняв і зіграв капітана Титаренка («Маестро»). Не віднось цей фільм до поетичного кіно.",
    "works": [
      {
        "title": "«У бій ідуть тільки „старі“»",
        "year": "1973",
        "role": "Режисер і актор: Олексій Титаренко",
        "level": "основне",
        "fact": "Художній фільм про льотчиків Другої світової війни."
      },
      {
        "title": "«Ати-бати, йшли солдати...»",
        "year": "1976",
        "role": "Режисер і актор",
        "level": "основне",
        "fact": "Одна з найвідоміших режисерських робіт Бикова."
      }
    ],
    "sources": [
      "https://vue.gov.ua/%D0%91%D0%B8%D0%BA%D0%BE%D0%B2%2C_%D0%9B%D0%B5%D0%BE%D0%BD%D1%96%D0%B4_%D0%A4%D0%B5%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D1%87",
      "https://zno.osvita.ua/ukraine-history/tag-ukrayina_v_period_zagostrennya_krizi_radyanskoyi_sistemi/"
    ]
  },
  {
    "name": "Леонід Осика",
    "period": "1960–1970-ті",
    "field": "Режисер українського поетичного кіно",
    "focus": "«Камінний хрест» (1968) і «Захар Беркут» (1971) — режисер Осика; «Тіні...» — Параджанов.",
    "works": [
      {
        "title": "«Камінний хрест»",
        "year": "1968",
        "role": "Режисер",
        "level": "основне",
        "fact": "За творами Василя Стефаника."
      },
      {
        "title": "«Захар Беркут»",
        "year": "1971",
        "role": "Режисер",
        "level": "основне",
        "fact": "За однойменною повістю Івана Франка."
      }
    ],
    "sources": [
      "https://online.dovzhenkocentre.org/film_collections/ukrayinske-poetychne-kino/",
      "https://zno.osvita.ua/ukraine-history/all/260/"
    ]
  },
  {
    "name": "Борис Івченко",
    "period": "1960–1970-ті",
    "field": "Кінорежисер",
    "focus": "«Пропала грамота» — режисер Борис Івченко, а не актор Іван Миколайчук.",
    "works": [
      {
        "title": "«Пропала грамота»",
        "year": "1972",
        "role": "Режисер",
        "level": "основне",
        "fact": "Український фільм за мотивами повісті Миколи Гоголя; роль головного козака виконав Іван Миколайчук."
      }
    ],
    "sources": [
      "https://online.dovzhenkocentre.org/film_collections/ukrayinske-poetychne-kino/",
      "https://zno.osvita.ua/ukraine-history/all/260/"
    ]
  },
  {
    "name": "Іван Кавалерідзе",
    "period": "1930-ті",
    "field": "Кінорежисер, скульптор",
    "focus": "Не плутай його історичні фільми з трилогією Довженка.",
    "works": [
      {
        "title": "«Перекоп»",
        "year": "1930",
        "role": "Режисер",
        "level": "контекст",
        "fact": "Історична кінокартина."
      },
      {
        "title": "«Коліївщина»",
        "year": "1933",
        "role": "Режисер",
        "level": "контекст",
        "fact": "Тема гайдамацького повстання."
      },
      {
        "title": "«Прометей»",
        "year": "1936",
        "role": "Режисер",
        "level": "контекст",
        "fact": "Фільм про боротьбу проти соціального гноблення."
      }
    ],
    "sources": [
      "https://zno.osvita.ua/ukraine-history/all/1525/",
      "https://zno.osvita.ua/ukraine-history/all/260/"
    ]
  },
  {
    "name": "Лесь Курбас",
    "period": "1920–1930-ті",
    "field": "Театральний режисер і реформатор",
    "focus": "Заснував театр «Березіль» у Києві 1922 року; це ТЕАТР, не кінофільм.",
    "works": [
      {
        "title": "«Березіль»",
        "year": "1922 (Київ), з 1926 — Харків",
        "role": "Засновник і художній керівник театру",
        "level": "основне",
        "fact": "Модернізація сценічної мови, експериментальний український театр."
      }
    ],
    "sources": [
      "https://tsdahou.archives.gov.ua/arhiv-vystavkovyh-proyektiv/vystavkovi-proyekty-czdago-ukrayiny/do-100-richchya-zasnuvannya-teatru-berezil-ta-135-yi-richnyczi-vid-dnya-narodzhennya-lesya-kurbasa/"
    ]
  }
];
