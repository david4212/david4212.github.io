export type InlineKeyboard = { text: string; callback_data: string }[][];

async function call(method: string, body: unknown) {
  const res = await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) console.error("Telegram API error:", method, res.status, await res.text());
  return res;
}

export function sendMessage(chatId: number | string, text: string, keyboard?: InlineKeyboard) {
  return call("sendMessage", {
    chat_id: chatId,
    text: text.slice(0, 4000),
    ...(keyboard ? { reply_markup: { inline_keyboard: keyboard } } : {}),
  });
}

export function answerCallback(callbackId: string) {
  return call("answerCallbackQuery", { callback_query_id: callbackId });
}
