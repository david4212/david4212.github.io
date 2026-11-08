// Запускається після збірки на Vercel: сам реєструє вебхук бота. Помилка тут не ламає деплой.
const token = process.env.TELEGRAM_BOT_TOKEN;
const host = process.env.VERCEL_PROJECT_PRODUCTION_URL;

if (process.env.VERCEL_ENV !== "production" || !token || !host) {
  console.log("[webhook] пропускаю (не production або немає токена/адреси)");
  process.exit(0);
}

try {
  const res = await fetch(`https://api.telegram.org/bot${token}/setWebhook`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: `https://${host}/api/bot`,
      allowed_updates: ["message", "callback_query"],
      secret_token: process.env.TELEGRAM_WEBHOOK_SECRET || undefined,
    }),
  });
  const data = await res.json();
  console.log("[webhook]", data.ok ? "зареєстровано" : "помилка", data.description ?? "");
} catch (e) {
  console.log("[webhook] не вдалось:", e.message);
}
