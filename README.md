# НМТ на 200

Next.js 14 + Tailwind + Prisma (PostgreSQL) + NextAuth.

## Запуск локально
1. `npm install`
2. Скопіюй `.env.example` у `.env` і заповни `DATABASE_URL`, `NEXTAUTH_SECRET`
3. `npx prisma db push`
4. `npm run dev`
5. Один раз відкрий `/api/init-db`, щоб додати теми

## Деплой
Хостити на Vercel (GitHub Pages не підходить — тут є бекенд).
