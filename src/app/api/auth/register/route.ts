import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import bcrypt from "bcryptjs";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const username = String(body?.username ?? "").trim();
    const password = String(body?.password ?? "");

    if (!username || !password) {
      return NextResponse.json({ error: "Введіть логін та пароль" }, { status: 400 });
    }

    if (username.length < 3 || password.length < 6) {
      return NextResponse.json(
        { error: "Логін — мінімум 3 символи, пароль — мінімум 6" },
        { status: 400 }
      );
    }

    // Перевіряємо, чи немає вже такого логіна
    const existingUser = await prisma.user.findUnique({
      where: { username },
    });

    if (existingUser) {
      return NextResponse.json({ error: "Користувач з таким логіном вже існує" }, { status: 400 });
    }

    // Шифруємо пароль
    const hashedPassword = await bcrypt.hash(password, 10);

    // Створюємо користувача в БД
    const user = await prisma.user.create({
      data: {
        username,
        passwordHash: hashedPassword,
      },
    });

    return NextResponse.json({ message: "Користувача створено успішно", userId: user.id }, { status: 201 });
  } catch (error) {
    console.error("Помилка реєстрації:", error);
    return NextResponse.json({ error: "Помилка сервера" }, { status: 500 });
  }
}
