import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import bcrypt from "bcryptjs";

export async function POST(req: Request) {
  try {
    const { username, password } = await req.json();

    if (!username || !password) {
      return NextResponse.json({ error: "Введіть логін та пароль" }, { status: 400 });
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
    return NextResponse.json({ error: "Помилка сервера" }, { status: 500 });
  }
}
