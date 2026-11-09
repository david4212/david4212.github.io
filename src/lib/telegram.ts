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

// Завантажує фото з Telegram (токен бота НІКОЛИ не потрапляє в базу чи на сайт)
export async function downloadFile(fileId: string): Promise<{ data: Buffer; mime: string } | null> {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  try {
    const info = await fetch(`https://api.telegram.org/bot${token}/getFile?file_id=${encodeURIComponent(fileId)}`).then((r) => r.json());
    const path: string | undefined = info?.result?.file_path;
    if (!path) return null;

    const res = await fetch(`https://api.telegram.org/file/bot${token}/${path}`);
    if (!res.ok) return null;
    const data = Buffer.from(await res.arrayBuffer());
    if (data.length > 5 * 1024 * 1024) return null;

    const ext = path.split(".").pop()?.toLowerCase();
    const mime = ext === "png" ? "image/png" : ext === "webp" ? "image/webp" : ext === "gif" ? "image/gif" : "image/jpeg";
    return { data, mime };
  } catch (e) {
    console.error("downloadFile error:", e);
    return null;
  }
}
