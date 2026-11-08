import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";

export async function GET() {
  try {
    // Перевіряємо, чи вже є теми, щоб не дублювати
    const existingTopics = await prisma.topic.count();
    
    if (existingTopics > 0) {
      return NextResponse.json({ message: "База вже заповнена!" });
    }

    // Створюємо базові теми для Української мови (як приклад)
    await prisma.topic.createMany({
      data: [
        { subject: "UKRAINIAN", title: "Фонетика. Графіка. Орфоепія", order: 1 },
        { subject: "UKRAINIAN", title: "Лексикологія. Фразеологія", order: 2 },
        { subject: "UKRAINIAN", title: "Будова слова. Словотвір", order: 3 },
        { subject: "UKRAINIAN", title: "Морфологія (Іменник, Прикметник)", order: 4 },
        
        { subject: "MATH", title: "Числа і вирази", order: 1 },
        { subject: "MATH", title: "Рівняння, нерівності та їх системи", order: 2 },
        { subject: "MATH", title: "Функції", order: 3 },
        
        { subject: "HISTORY", title: "Вступ до історії України", order: 1 },
        { subject: "HISTORY", title: "Київська держава (Русь-Україна)", order: 2 },
      ]
    });

    return NextResponse.json({ message: "Базу успішно ініціалізовано! Теми додано." });
  } catch (error) {
    console.error("Помилка ініціалізації БД:", error);
    return NextResponse.json({ error: "Помилка сервера" }, { status: 500 });
  }
}
