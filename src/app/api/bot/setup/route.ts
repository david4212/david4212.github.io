import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

// Відкрий /api/bot/setup один раз у браузері — це зареєструє вебхук у Telegram.
export async function GET(req: Request) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  if (!token) return NextResponse.json({ error: "Немає TELEGRAM_BOT_TOKEN" }, { status: 500 });

  const host = process.env.VERCEL_PROJECT_PRODUCTION_URL || req.headers.get("host");
  const url = `https://${host}/api/bot`;

  const res = await fetch(`https://api.telegram.org/bot${token}/setWebhook`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url,
      allowed_updates: ["message", "callback_query"],
      secret_token: process.env.TELEGRAM_WEBHOOK_SECRET || undefined,
    }),
  });
  return NextResponse.json({ webhook: url, telegram: await res.json() });
}
