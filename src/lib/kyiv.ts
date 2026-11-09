const fmt = new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Kyiv", year: "numeric", month: "2-digit", day: "2-digit" });

// Календарна дата YYYY-MM-DD за київським часом
export function kyivDate(d: Date = new Date()): string {
  return fmt.format(d);
}

export function prevDate(date: string): string {
  const [y, m, d] = date.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d - 1)).toISOString().slice(0, 10);
}
