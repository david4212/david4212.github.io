# НМТ на 200

Next.js 14 + Tailwind + Prisma (PostgreSQL / Neon) + NextAuth + Telegram-бот як адмінка.

- Таблиці в базі й офіційні теми НМТ (`src/lib/curriculum.json`) створюються автоматично під час кожної збірки на Vercel.
- Питання й картки додаються через бота: `/addtest`, `/addcards` (предмет → тема → підрозділ → контент).
- Змінні середовища: `DATABASE_URL`, `NEXTAUTH_SECRET`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_ID`, `TELEGRAM_WEBHOOK_SECRET`.
