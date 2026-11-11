/** Authored historical map collection of the Ukrainian Institute of National Memory.
 * Image URLs link to the original artwork. Educational display, not exam questions.
 * UINP explicitly permits noncommercial distribution of this series with attribution.
 */
export type EducationalMap = {
 id:string; title:string; period:string; periodKey:string; sourceName:string; sourceType:"institution"|"textbook"; imageUrl:string; sourceUrl:string; key:string; explanation:string; legend:string[]; kind:"educational";
};
export const HISTORY_EDUCATIONAL_MAPS: EducationalMap[] = [
  {
    "id": "uinp-map-7",
    "title": "Українське військо в революції 1917–1921 років",
    "period": "1917–1921",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/yd51599054367VGt.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Військові події Української революції",
    "explanation": "Простежуй розташування військових формувань і зміну контролю над територіями.",
    "legend": [
      "Військові події Української революції",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-8",
    "title": "Повернення Криму та Донбасу під український контроль",
    "period": "1918",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/Owd1599054399pLj.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Події весни 1918 року",
    "explanation": "Показано кампанію Армії УНР у Криму та розвиток подій на сході України.",
    "legend": [
      "Події весни 1918 року",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-9",
    "title": "Чортківська офензива УГА",
    "period": "Червень 1919",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/uv21599054422jIT.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Західноукраїнський театр бойових дій",
    "explanation": "Чортківська офензива — наступ Української галицької армії проти польських сил.",
    "legend": [
      "Західноукраїнський театр бойових дій",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-10",
    "title": "Східні кордони польських держав",
    "period": "Міжвоєнний і попередні періоди",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/LvP1599054487lIp.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Кордонні зміни між державами",
    "explanation": "Зіставляй кордони різних епох, звертай увагу на територію Галичини й Волині.",
    "legend": [
      "Кордонні зміни між державами",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-11",
    "title": "Польсько-українська війна",
    "period": "1918–1919",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/SQk1599054515k3L.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Боротьба за Східну Галичину",
    "explanation": "Порівняй райони під контролем ЗУНР і Польщі.",
    "legend": [
      "Боротьба за Східну Галичину",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-12",
    "title": "Польсько-українське протистояння в 1940-х",
    "period": "1940-ті",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/iMK1599054535Iu5.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Прикордонні райони і повоєнне насильство",
    "explanation": "Враховуй контекст Другої світової й післявоєнних переселень населення.",
    "legend": [
      "Прикордонні райони і повоєнне насильство",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-13",
    "title": "Союз УНР і Польщі",
    "period": "1920",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/59F1599054556uSU.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Варшавський договір і спільні воєнні дії",
    "explanation": "Позначено союз і перебіг подій 1920 року.",
    "legend": [
      "Варшавський договір і спільні воєнні дії",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-14",
    "title": "Розселення українців і поляків",
    "period": "XIX–XX ст.",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/ZRI1599054574DE3.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Етнічна географія прикордонних земель",
    "explanation": "Читай етнічну карту окремо від політичних кордонів.",
    "legend": [
      "Етнічна географія прикордонних земель",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-15",
    "title": "Закарпаття після розпаду Австро-Угорщини",
    "period": "1918–1919",
    "periodKey": "rev",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/eMr1599054752sUy.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Державна належність Закарпаття",
    "explanation": "Визначай зміни влади в регіоні після Першої світової війни.",
    "legend": [
      "Державна належність Закарпаття",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-16",
    "title": "Мюнхенська угода та Віденський арбітраж",
    "period": "1938",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/EZF1599054773bL9.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Зміни кордонів Чехословаччини",
    "explanation": "Звертай увагу на відчуження територій та автономію Закарпаття.",
    "legend": [
      "Зміни кордонів Чехословаччини",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-17",
    "title": "Закарпаття у 1938 році",
    "period": "1938",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/yGh1599054815XWZ.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Автономія Підкарпатської Русі",
    "explanation": "Пов'язуй із кризою Чехословаччини 1938 року.",
    "legend": [
      "Автономія Підкарпатської Русі",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-18",
    "title": "Окупація Карпатської України",
    "period": "1939",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/K2o15990548404Zc.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Березневі події 1939 року",
    "explanation": "Окрема карта короткого існування Карпатської України та угорського вторгнення.",
    "legend": [
      "Березневі події 1939 року",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-19",
    "title": "Зміни влади на Закарпатті",
    "period": "1939",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/iMB15990548834pL.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Територіальні зміни 1939 року",
    "explanation": "Не ототожнюй Закарпаття з територіями УРСР того року.",
    "legend": [
      "Територіальні зміни 1939 року",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-20",
    "title": "Битва на Красному полі",
    "period": "Березень 1939",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/kKH1599054899mJ5.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Оборона Карпатської України",
    "explanation": "Місце поблизу Хуста, пов'язане з опором Карпатської Січі.",
    "legend": [
      "Оборона Карпатської України",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-21",
    "title": "Українські землі між світовими війнами",
    "period": "1919–1939",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/16/M7H1599055190Coy.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Поділ українських земель між державами",
    "explanation": "Співвіднось УСРР/УРСР, Польщу, Румунію та Чехословаччину.",
    "legend": [
      "Поділ українських земель між державами",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-22",
    "title": "Розчленування Чехословаччини",
    "period": "1938",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/sAa1599055207cMk.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Мюнхенська криза",
    "explanation": "Розрізняй кордони до та після рішень 1938 року.",
    "legend": [
      "Мюнхенська криза",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-23",
    "title": "Карпатська Україна на карті",
    "period": "Березень 1939",
    "periodKey": "interwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/afM1599055423UMM.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Проголошення незалежності в Хусті",
    "explanation": "Знайди Закарпаття, Хуст і території під угорською окупацією.",
    "legend": [
      "Проголошення незалежності в Хусті",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-24",
    "title": "Пакт Молотова — Ріббентропа: сфери впливу",
    "period": "Серпень 1939",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/fTS1599055441fg8.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Поділ Східної Європи між СРСР і Німеччиною",
    "explanation": "Порівняй сфери впливу, зафіксовані в таємному протоколі.",
    "legend": [
      "Поділ Східної Європи між СРСР і Німеччиною",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-25",
    "title": "Агресія Німеччини та СРСР проти Польщі",
    "period": "Вересень–жовтень 1939",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/Web1599055497nEx.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Початок Другої світової війни",
    "explanation": "Польщу атакували Німеччина 1 вересня і СРСР 17 вересня 1939 року.",
    "legend": [
      "Початок Другої світової війни",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-26",
    "title": "Радянські анексії в Східній Європі",
    "period": "1940",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/Sql15990555197zK.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Приєднання територій до СРСР",
    "explanation": "Звертай увагу на Бессарабію та Північну Буковину в 1940 році.",
    "legend": [
      "Приєднання територій до СРСР",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-27",
    "title": "Німецьке вторгнення й окупація України",
    "period": "Червень 1941 — листопад 1942",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/tCO1599055549X3q.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Початок німецько-радянської війни",
    "explanation": "Стрілки на історичній карті відображають напрямки руху фронтів; зафарбовані території — зміни окупаційного контролю.",
    "legend": [
      "Початок німецько-радянської війни",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-28",
    "title": "Нацистська окупаційна адміністрація України",
    "period": "1941–1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/hBo1599055572T72.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Окупаційні зони і режими",
    "explanation": "Розрізняй Райхскомісаріат «Україна», дистрикт «Галичина», військову адміністрацію та румунську зону.",
    "legend": [
      "Окупаційні зони і режими",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-29",
    "title": "Радянські партизани й підпілля",
    "period": "1941–1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/QwO1599055589yLK.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Рух Опору в окупованій Україні",
    "explanation": "Умовні знаки позначають райони діяльності радянського підпілля й партизанів.",
    "legend": [
      "Рух Опору в окупованій Україні",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-30",
    "title": "Знищені нацистами населені пункти",
    "period": "1941–1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/HDr1599055621PCr.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Нацистські злочини проти цивільного населення",
    "explanation": "Місця на карті пов'язані зі спаленими селами й окупаційним терором.",
    "legend": [
      "Нацистські злочини проти цивільного населення",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-31",
    "title": "Діяльність УПА на українських землях",
    "period": "1943–1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/88X1599055638ZeY.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Райони дій УПА",
    "explanation": "Показано історичні регіони діяльності повстанських формувань у Другій світовій.",
    "legend": [
      "Райони дій УПА",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-32",
    "title": "Зміни фронту після Сталінградської битви",
    "period": "Листопад 1942 — серпень 1943",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/ihw1599055654n57.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Перехід стратегічної ініціативи",
    "explanation": "Порівняй фронтові рубежі та дати вигнання нацистських військ зі сходу України.",
    "legend": [
      "Перехід стратегічної ініціативи",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-33",
    "title": "Наступ радянських фронтів в Україні",
    "period": "Серпень 1943 — листопад 1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/NoF1599055685fVN.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Вигнання нацистських окупантів",
    "explanation": "На карті показано просування фронтів через Лівобережжя, Правобережжя, Крим і західні області.",
    "legend": [
      "Вигнання нацистських окупантів",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-34",
    "title": "Українці на фронтах Другої світової війни",
    "period": "1939–1945",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/QVG1599055715YZu.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Участь українців у різних арміях",
    "explanation": "Географія воєнних дій не обмежувалася територією України.",
    "legend": [
      "Участь українців у різних арміях",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-35",
    "title": "Закордонні рейди УПА",
    "period": "Повоєнні 1940-ві",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/BNt1599055741qf4.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Рейди українського підпілля",
    "explanation": "Розглядай карту в контексті збройного протистояння та повоєнної еміграції.",
    "legend": [
      "Рейди українського підпілля",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-36",
    "title": "Повоєнний поділ Європи",
    "period": "1945–1949",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/1un1599055759SvJ.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Європа після війни",
    "explanation": "Зіставляй зміни кордонів і політичні сфери впливу.",
    "legend": [
      "Європа після війни",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-37",
    "title": "Табори переміщених осіб у Європі",
    "period": "Після 1945",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/s2b1599055783KFO.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "ДіПі — переміщені особи",
    "explanation": "Знайди насамперед табори в окупаційних зонах Німеччини й Австрії.",
    "legend": [
      "ДіПі — переміщені особи",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-38",
    "title": "Українська еміграція після Другої світової",
    "period": "1945–1950-ті",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/TXx1599055802QHI.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Напрями переселення українців",
    "explanation": "Розрізняй вимушені повоєнні міграції й давніші хвилі еміграції.",
    "legend": [
      "Напрями переселення українців",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-39",
    "title": "Похідні групи ОУН",
    "period": "1941",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/iLN1599055999dyJ.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Діяльність українського націоналістичного руху",
    "explanation": "Позначено маршрути пересування похідних груп у контексті німецького вторгнення.",
    "legend": [
      "Діяльність українського націоналістичного руху",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-40",
    "title": "Українське підпілля у 1943–1944 роках",
    "period": "1943–1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/bnC1599056021yI7.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Опір і збройне протистояння",
    "explanation": "Порівнюй райони дій УПА з лініями фронту та окупаційними зонами.",
    "legend": [
      "Опір і збройне протистояння",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-41",
    "title": "Доля членів ОУН у нацистських таборах",
    "period": "1940-ві",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/A7b1599056038RZb.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Нацистські репресії проти членів ОУН",
    "explanation": "Зображені місця ув'язнення — це не карта основних фронтових операцій.",
    "legend": [
      "Нацистські репресії проти членів ОУН",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-42",
    "title": "Райони діяльності УПА",
    "period": "1944",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/U0A1599056149YlM.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Перехід від воєнних дій до протидії радянській владі",
    "explanation": "Враховуй зміну контролю над українськими землями в 1944 році.",
    "legend": [
      "Перехід від воєнних дій до протидії радянській владі",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-43",
    "title": "Райони діяльності УПА в повоєнний час",
    "period": "1945",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/foM1599056171eHu.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Підпільний рух після завершення війни в Європі",
    "explanation": "На карті показано географію продовження протистояння після травня 1945 року.",
    "legend": [
      "Підпільний рух після завершення війни в Європі",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-44",
    "title": "Закордонні рейди УПА",
    "period": "1944–1945",
    "periodKey": "ww2",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/Kr11599056192pkF.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Перехідні воєнні й повоєнні події",
    "explanation": "Зіставляй маршрути з тодішніми державними кордонами.",
    "legend": [
      "Перехідні воєнні й повоєнні події",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-45",
    "title": "Закерзоння після війни",
    "period": "1945–1947",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/GHs1599056293dBf.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Українські етнічні території західніше лінії Керзона",
    "explanation": "Порівнюй державні кордони з районами проживання українців.",
    "legend": [
      "Українські етнічні території західніше лінії Керзона",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-46",
    "title": "Українські етнічні землі Закерзоння",
    "period": "Перша половина XX ст.",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/gXA1599056588N32.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Лемківщина, Надсяння, Холмщина, Підляшшя",
    "explanation": "Території нині переважно в Польщі; не плутай етнічний ареал із державними кордонами.",
    "legend": [
      "Лемківщина, Надсяння, Холмщина, Підляшшя",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-47",
    "title": "Депортації та обміни населенням",
    "period": "1944–1951",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/Eg51599056610Rqf.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Переміщення українців і поляків",
    "explanation": "Післявоєнні переселення та операція «Вісла» (1947) — різні історичні процеси.",
    "legend": [
      "Переміщення українців і поляків",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-48",
    "title": "Європа наприкінці холодної війни",
    "period": "1988",
    "periodKey": "postwar",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/OZO1599056671Kje.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Соціалістичні держави Європи",
    "explanation": "Порівняй кордони політичних блоків напередодні 1989–1991 років.",
    "legend": [
      "Соціалістичні держави Європи",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-60",
    "title": "Окупація Криму Росією",
    "period": "Лютий–березень 2014",
    "periodKey": "independence",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/gnL1599058159xeM.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Початок російсько-української війни",
    "explanation": "Мапа місць і подій захоплення Кримського півострова.",
    "legend": [
      "Початок російсько-української війни",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-61",
    "title": "Відновлення українського контролю над містами Донеччини",
    "period": "2014",
    "periodKey": "independence",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/Gqk1599058178hPy.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Бойові дії на сході України 2014 року",
    "explanation": "Історична карта стосується ситуації 2014 року, а не нинішньої лінії зіткнення.",
    "legend": [
      "Бойові дії на сході України 2014 року",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  },
  {
    "id": "uinp-map-62",
    "title": "Зона Операції об'єднаних сил",
    "period": "2019",
    "periodKey": "independence",
    "sourceName": "УІНП · навчальна історична карта",
    "sourceType": "institution",
    "imageUrl": "https://uinp.gov.ua/storage/app/public/uploads/2020-09-02/17/OaK1599058194mmv.jpeg",
    "sourceUrl": "https://uinp.gov.ua/elektronni-vydannya/kartografichnyy-dorobok-ukrayinskogo-instytutu-nacionalnoyi-pamyati-2015-2020",
    "key": "Розмежування на Донбасі 2019 року",
    "explanation": "Це історична карта до повномасштабного вторгнення 2022 року, не актуальна схема фронту.",
    "legend": [
      "Розмежування на Донбасі 2019 року",
      "Умовні позначення, кольори та кордони звіряй із легендою на оригінальному зображенні.",
      "Це навчальна карта, а не скан конкретного завдання НМТ."
    ],
    "kind": "educational"
  }
];
