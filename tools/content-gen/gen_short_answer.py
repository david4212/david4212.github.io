#!/usr/bin/env python3
"""Generate short_answer questions for math and history topics."""

import json
import os

MATH_QUESTIONS = {
    "01_chysla_gen.json": [
        {"text": "Знайдіть значення виразу: 3⁴ − 2⁵", "metadata": {"answer": 49}, "explanation": "3⁴ = 81, 2⁵ = 32, тож 81 − 32 = 49.", "testLevel": 1},
        {"text": "Яке найменше спільне кратне чисел 12 та 18?", "metadata": {"answer": 36}, "explanation": "НСК(12, 18): 12 = 2²·3, 18 = 2·3², НСК = 2²·3² = 36.", "testLevel": 2},
        {"text": "Знайдіть найбільший спільний дільник чисел 84 та 126.", "metadata": {"answer": 42}, "explanation": "84 = 2²·3·7, 126 = 2·3²·7, НСД = 2·3·7 = 42.", "testLevel": 2},
        {"text": "Скільки простих чисел серед чисел від 1 до 20?", "metadata": {"answer": 8}, "explanation": "Прості: 2, 3, 5, 7, 11, 13, 17, 19 — усього 8.", "testLevel": 1},
        {"text": "Обчисліть: |−7| + |3 − 10| − |−2|", "metadata": {"answer": 12}, "explanation": "|−7| = 7, |3−10| = 7, |−2| = 2, тож 7 + 7 − 2 = 12.", "testLevel": 2},
    ],
    "02_alhebra_gen.json": [
        {"text": "Розв'яжіть рівняння: 2x + 5 = 17. Чому дорівнює x?", "metadata": {"answer": 6}, "explanation": "2x = 12, x = 6.", "testLevel": 1},
        {"text": "Спростіть вираз (a³)² · a⁴ і вкажіть показник степеня a.", "metadata": {"answer": 10}, "explanation": "(a³)² = a⁶, a⁶ · a⁴ = a¹⁰.", "testLevel": 2},
        {"text": "Знайдіть значення виразу a² − b² при a = 7, b = 3.", "metadata": {"answer": 40}, "explanation": "a² − b² = 49 − 9 = 40, або (a−b)(a+b) = 4·10 = 40.", "testLevel": 1},
        {"text": "Яке значення виразу log₂(64)?", "metadata": {"answer": 6}, "explanation": "2⁶ = 64, тому log₂(64) = 6.", "testLevel": 3},
        {"text": "Знайдіть дискримінант рівняння x² − 6x + 5 = 0.", "metadata": {"answer": 16}, "explanation": "D = b² − 4ac = 36 − 20 = 16.", "testLevel": 2},
    ],
    "03_rivnyannya_gen.json": [
        {"text": "Скільки розв'язків має рівняння x² + 4 = 0 у множині дійсних чисел?", "metadata": {"answer": 0}, "explanation": "x² = −4 не має дійсних розв'язків, бо квадрат числа невід'ємний.", "testLevel": 1},
        {"text": "Знайдіть суму коренів рівняння x² − 5x + 6 = 0.", "metadata": {"answer": 5}, "explanation": "За теоремою Вієта: x₁ + x₂ = 5.", "testLevel": 2},
        {"text": "Знайдіть добуток коренів рівняння x² + 3x − 10 = 0.", "metadata": {"answer": -10}, "explanation": "За теоремою Вієта: x₁ · x₂ = c/a = −10.", "testLevel": 2},
        {"text": "Скільки цілих розв'язків має нерівність |x| < 5?", "metadata": {"answer": 9}, "explanation": "−5 < x < 5, цілі: −4, −3, −2, −1, 0, 1, 2, 3, 4 — 9 чисел.", "testLevel": 2},
        {"text": "Розв'яжіть систему: x + y = 10, x − y = 4. Чому дорівнює x?", "metadata": {"answer": 7}, "explanation": "Додаємо: 2x = 14, x = 7.", "testLevel": 1},
    ],
    "04_funktsiyi_gen.json": [
        {"text": "Знайдіть f(3), якщо f(x) = 2x² − x + 1.", "metadata": {"answer": 16}, "explanation": "f(3) = 2·9 − 3 + 1 = 18 − 3 + 1 = 16.", "testLevel": 1},
        {"text": "Функція f(x) = x² − 4x + 3 досягає мінімуму при x = ?", "metadata": {"answer": 2}, "explanation": "x_мін = −b/(2a) = 4/2 = 2.", "testLevel": 2},
        {"text": "Скільки нулів має функція f(x) = x³ − x?", "metadata": {"answer": 3}, "explanation": "x³ − x = x(x²−1) = x(x−1)(x+1), нулі: 0, 1, −1.", "testLevel": 2},
        {"text": "Знайдіть область визначення: f(x) = √(x − 3). Яке мінімальне значення x?", "metadata": {"answer": 3}, "explanation": "x − 3 ≥ 0, тобто x ≥ 3.", "testLevel": 1},
    ],
    "05_pokhidna_gen.json": [
        {"text": "Знайдіть f'(2), якщо f(x) = x³.", "metadata": {"answer": 12}, "explanation": "f'(x) = 3x², f'(2) = 3·4 = 12.", "testLevel": 2},
        {"text": "Знайдіть похідну f(x) = 5x⁴ при x = 1.", "metadata": {"answer": 20}, "explanation": "f'(x) = 20x³, f'(1) = 20.", "testLevel": 2},
        {"text": "Знайдіть ∫₀² 3x² dx.", "metadata": {"answer": 8}, "explanation": "∫3x² dx = x³, від 0 до 2: 8 − 0 = 8.", "testLevel": 3},
        {"text": "У якій точці функція f(x) = x² − 6x + 10 має мінімум?", "metadata": {"answer": 3}, "explanation": "f'(x) = 2x − 6 = 0, x = 3. f''(3) = 2 > 0 — мінімум.", "testLevel": 2},
    ],
    "06_kombinatoryka_imovirnist_gen.json": [
        {"text": "Скільки способів вибрати 2 книги з 5? (C₅²)", "metadata": {"answer": 10}, "explanation": "C(5,2) = 5!/(2!·3!) = 10.", "testLevel": 1},
        {"text": "Скільки тризначних чисел можна скласти з цифр 1, 2, 3 без повторень?", "metadata": {"answer": 6}, "explanation": "P(3) = 3! = 6.", "testLevel": 1},
        {"text": "Обчисліть: 6! / 4!", "metadata": {"answer": 30}, "explanation": "6!/4! = 6·5 = 30.", "testLevel": 2},
        {"text": "В урні 3 білих та 7 чорних кульок. Яка ймовірність витягти білу? (відповідь у %)", "metadata": {"answer": 30}, "explanation": "P = 3/10 = 0.3 = 30%.", "testLevel": 2},
    ],
    "07_planimetriya_gen.json": [
        {"text": "Знайдіть площу трикутника з основою 10 та висотою 6.", "metadata": {"answer": 30}, "explanation": "S = ½ · a · h = ½ · 10 · 6 = 30.", "testLevel": 1},
        {"text": "Знайдіть гіпотенузу прямокутного трикутника з катетами 3 та 4.", "metadata": {"answer": 5}, "explanation": "c = √(9 + 16) = √25 = 5.", "testLevel": 1},
        {"text": "Знайдіть площу кола з радіусом 7 (відповідь округліть до цілого).", "metadata": {"answer": 154, "tolerance": 1}, "explanation": "S = πr² = π·49 ≈ 153.94 ≈ 154.", "testLevel": 2},
        {"text": "У рівносторонньому трикутнику зі стороною 6 знайдіть висоту (округліть до десятих).", "metadata": {"answer": 5.2, "tolerance": 0.1}, "explanation": "h = a√3/2 = 6·√3/2 = 3√3 ≈ 5.196 ≈ 5.2.", "testLevel": 3},
    ],
    "08_stereometriya_gen.json": [
        {"text": "Знайдіть об'єм куба з ребром 5.", "metadata": {"answer": 125}, "explanation": "V = a³ = 5³ = 125.", "testLevel": 1},
        {"text": "Знайдіть площу поверхні куба з ребром 3.", "metadata": {"answer": 54}, "explanation": "S = 6a² = 6·9 = 54.", "testLevel": 1},
        {"text": "Знайдіть об'єм циліндра з радіусом 3 та висотою 7 (округліть до цілого).", "metadata": {"answer": 198, "tolerance": 1}, "explanation": "V = πr²h = π·9·7 = 63π ≈ 197.92 ≈ 198.", "testLevel": 2},
        {"text": "Знайдіть довжину діагоналі прямокутного паралелепіпеда зі сторонами 3, 4 та 12.", "metadata": {"answer": 13}, "explanation": "d = √(9 + 16 + 144) = √169 = 13.", "testLevel": 3},
    ],
}

HISTORY_QUESTIONS = {
    "01_davnya_istoriya_kyivska_rus.json": [
        {"text": "У якому році відбулося хрещення Русі?", "metadata": {"answer": 988}, "explanation": "Хрещення Русі відбулося у 988 році за князя Володимира Великого.", "testLevel": 1},
        {"text": "Скільки років тривало правління Ярослава Мудрого (1019–1054)?", "metadata": {"answer": 35}, "explanation": "1054 − 1019 = 35 років.", "testLevel": 2},
        {"text": "У якому столітті було засновано Київ (згідно з літописною традицією)?", "metadata": {"answer": "V", "tolerance": 0}, "explanation": "За літописною традицією Київ засновано у V столітті.", "testLevel": 2},
    ],
    "02_halytsko_volynska_lytovska_doba.json": [
        {"text": "У якому році відбулася битва під Берестечком?", "metadata": {"answer": 1651}, "explanation": "Битва під Берестечком — 1651 рік, одна з найбільших битв козацької доби.", "testLevel": 2},
        {"text": "У якому році Данило Галицький отримав королівський титул?", "metadata": {"answer": 1253}, "explanation": "Данило отримав корону від папського легата у 1253 році.", "testLevel": 3},
    ],
    "03_kozatska_doba_hetmanshchyna.json": [
        {"text": "У якому році розпочалося повстання Богдана Хмельницького?", "metadata": {"answer": 1648}, "explanation": "Національно-визвольна війна під проводом Б. Хмельницького почалася у 1648 р.", "testLevel": 1},
        {"text": "У якому році було підписано Зборівський мир?", "metadata": {"answer": 1649}, "explanation": "Зборівський мирний договір підписано 18 серпня 1649 року.", "testLevel": 2},
        {"text": "Скільки років формально існувала Гетьманщина (1648–1764)?", "metadata": {"answer": 116}, "explanation": "1764 − 1648 = 116 років.", "testLevel": 3},
    ],
    "04_ukraina_v_skladi_imperiy.json": [
        {"text": "У якому році було скасовано кріпацтво в Російській імперії?", "metadata": {"answer": 1861}, "explanation": "Маніфест про скасування кріпацтва — 19 лютого 1861 року.", "testLevel": 1},
        {"text": "У якому році Кирило-Мефодіївське братство було розгромлено?", "metadata": {"answer": 1847}, "explanation": "Братство було викрито і розгромлено у 1847 р.", "testLevel": 2},
    ],
    "05_ukrainska_revolyutsiya.json": [
        {"text": "У якому році було проголошено I Універсал Центральної Ради?", "metadata": {"answer": 1917}, "explanation": "I Універсал проголошено 23 червня 1917 року.", "testLevel": 1},
        {"text": "У якому році було створено Західноукраїнську Народну Республіку (ЗУНР)?", "metadata": {"answer": 1918}, "explanation": "ЗУНР проголошено 1 листопада 1918 року.", "testLevel": 2},
        {"text": "У якому році відбувся Акт Злуки УНР і ЗУНР?", "metadata": {"answer": 1919}, "explanation": "Акт Злуки — 22 січня 1919 року.", "testLevel": 2},
    ],
    "06_ukraina_mizhvoyennyi_dsv.json": [
        {"text": "У якому році розпочався Голодомор в Україні?", "metadata": {"answer": 1932}, "explanation": "Голодомор 1932–1933 років — геноцид українського народу.", "testLevel": 1},
        {"text": "Скільки мільйонів людей (мінімальна оцінка) загинуло під час Голодомору?", "metadata": {"answer": "3.5", "tolerance": 0.5}, "explanation": "За різними оцінками, від 3.5 до 7 мільйонів людей загинули.", "testLevel": 3},
    ],
    "07_ukraina_druha_polovyna_xx.json": [
        {"text": "У якому році сталася Чорнобильська катастрофа?", "metadata": {"answer": 1986}, "explanation": "Аварія на ЧАЕС сталася 26 квітня 1986 року.", "testLevel": 1},
        {"text": "У якому році Україна проголосила незалежність?", "metadata": {"answer": 1991}, "explanation": "Акт проголошення незалежності — 24 серпня 1991 р.", "testLevel": 1},
    ],
    "08_suchasna_ukraina.json": [
        {"text": "У якому році відбулася Помаранчева революція?", "metadata": {"answer": 2004}, "explanation": "Помаранчева революція — листопад–грудень 2004 року.", "testLevel": 1},
        {"text": "У якому році розпочалася Революція Гідності (Євромайдан)?", "metadata": {"answer": 2013}, "explanation": "Євромайдан розпочався 21 листопада 2013 року.", "testLevel": 2},
        {"text": "У якому році Росія анексувала Крим?", "metadata": {"answer": 2014}, "explanation": "Анексія Криму відбулася у лютому–березні 2014 року.", "testLevel": 1},
    ],
}

def add_short_answers(folder, questions_dict):
    for fname, new_qs in questions_dict.items():
        path = os.path.join(folder, fname)
        if not os.path.exists(path):
            # Try _gen version
            gen_name = fname.replace('.json', '').split('_')
            # Find matching gen file
            for f in os.listdir(folder):
                if f.startswith(fname[:2]) and f.endswith('_gen.json'):
                    path = os.path.join(folder, f)
                    break

        if not os.path.exists(path):
            print(f"SKIP: {fname} not found")
            continue

        with open(path) as f:
            data = json.load(f)

        existing_texts = {q['text'] for q in data.get('questions', [])}
        added = 0
        for q in new_qs:
            if q['text'] in existing_texts:
                continue
            data['questions'].append({
                "text": q['text'],
                "options": [],
                "correctIndex": 0,
                "explanation": q['explanation'],
                "testLevel": q['testLevel'],
                "questionType": "short_answer",
                "metadata": q['metadata'],
            })
            added += 1

        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"{os.path.basename(path)}: +{added} short_answer questions")


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("=== MATH ===")
    add_short_answers(os.path.join(base, "content", "math"), MATH_QUESTIONS)

    print("\n=== HISTORY ===")
    add_short_answers(os.path.join(base, "content", "history"), HISTORY_QUESTIONS)
