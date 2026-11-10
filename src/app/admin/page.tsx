import { redirect } from "next/navigation";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import prisma from "@/lib/prisma";

export const dynamic = "force-dynamic";

const subjectNames: Record<string, string> = {
  UKRAINIAN: "Українська мова",
  MATH: "Математика",
  HISTORY: "Історія",
  ENGLISH: "Англійська мова",
};

function Stat({ label, value, hint }: { label: string; value: string | number; hint?: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900">{value}</p>
      {hint ? <p className="mt-1 text-xs text-slate-400">{hint}</p> : null}
    </div>
  );
}

export default async function AdminPage() {
  const session = await getServerSession(authOptions);
  if (!session?.user) redirect("/login");
  if (!session.user.isAdmin) redirect("/");

  const now = new Date();
  const dayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  const onlineSince = new Date(now.getTime() - 2 * 60 * 1000);

  const [
    userCount,
    onlineUsers,
    todayUsers,
    weekUsers,
    monthUsers,
    testsToday,
    testsWeek,
    testsMonth,
    average,
    latestResults,
    topicGroups,
    userGroups,
  ] = await Promise.all([
    prisma.user.count(),
    prisma.user.findMany({
      where: { lastSeenAt: { gte: onlineSince } },
      select: { id: true, username: true, lastSeenAt: true },
      orderBy: { lastSeenAt: "desc" },
    }),
    prisma.user.count({ where: { createdAt: { gte: dayAgo } } }),
    prisma.user.count({ where: { createdAt: { gte: weekAgo } } }),
    prisma.user.count({ where: { createdAt: { gte: monthAgo } } }),
    prisma.testResult.count({ where: { createdAt: { gte: dayAgo } } }),
    prisma.testResult.count({ where: { createdAt: { gte: weekAgo } } }),
    prisma.testResult.count({ where: { createdAt: { gte: monthAgo } } }),
    prisma.testResult.aggregate({ _avg: { percent: true } }),
    prisma.testResult.findMany({
      take: 12,
      orderBy: { createdAt: "desc" },
      include: {
        user: { select: { username: true } },
        topic: { select: { title: true, subject: true } },
      },
    }),
    prisma.testResult.groupBy({
      by: ["topicId"],
      _avg: { percent: true },
      _count: { _all: true },
      orderBy: { _avg: { percent: "asc" } },
      take: 8,
    }),
    prisma.testResult.groupBy({
      by: ["userId"],
      _avg: { percent: true },
      _count: { _all: true },
      orderBy: { _count: { userId: "desc" } },
      take: 10,
    }),
  ]);

  const topicIds = topicGroups.map((item) => item.topicId);
  const userIds = userGroups.map((item) => item.userId);
  const [topics, users] = await Promise.all([
    prisma.topic.findMany({ where: { id: { in: topicIds } }, select: { id: true, title: true, subject: true } }),
    prisma.user.findMany({ where: { id: { in: userIds } }, select: { id: true, username: true } }),
  ]);
  const topicMap = new Map(topics.map((item) => [item.id, item]));
  const userMap = new Map(users.map((item) => [item.id, item]));

  return (
    <main className="container mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">НМТ на 200</p>
          <h1 className="mt-1 text-3xl font-bold text-slate-900">Панель адміністратора</h1>
          <p className="mt-2 text-sm text-slate-500">Вітаю, {session.user.name}. Статистика оновлюється під час перезавантаження сторінки.</p>
        </div>
        <div className="rounded-xl bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
          {onlineUsers.length} користувачів онлайн
        </div>
      </div>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Усього акаунтів" value={userCount} />
        <Stat label="Зараз онлайн" value={onlineUsers.length} hint="Активність за останні 2 хвилини" />
        <Stat label="Середній результат" value={average._avg.percent == null ? "—" : `${Math.round(average._avg.percent)}%`} />
        <Stat label="Тестів за 24 години" value={testsToday} />
      </section>

      <section className="mt-8 grid gap-4 sm:grid-cols-3">
        <Stat label="Нові акаунти за 24 год" value={todayUsers} />
        <Stat label="Нові акаунти за 7 днів" value={weekUsers} />
        <Stat label="Нові акаунти за 30 днів" value={monthUsers} />
        <Stat label="Тестів за 7 днів" value={testsWeek} />
        <Stat label="Тестів за 30 днів" value={testsMonth} />
        <Stat label="Тестів усього" value={await prisma.testResult.count()} />
      </section>

      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900">Хто зараз на сайті</h2>
          <p className="mb-4 mt-1 text-xs text-slate-500">Показуються авторизовані користувачі з активністю за останні 2 хвилини.</p>
          {onlineUsers.length ? (
            <div className="divide-y divide-slate-100">
              {onlineUsers.map((user) => (
                <div key={user.id} className="flex items-center justify-between py-3 text-sm">
                  <span className="font-medium text-slate-800">{user.username}</span>
                  <span className="text-slate-400">{user.lastSeenAt?.toLocaleTimeString("uk-UA", { hour: "2-digit", minute: "2-digit" })}</span>
                </div>
              ))}
            </div>
          ) : <p className="py-5 text-sm text-slate-400">Зараз немає активних авторизованих користувачів.</p>}
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900">Теми з найнижчим середнім балом</h2>
          <p className="mb-4 mt-1 text-xs text-slate-500">За збереженими результатами тестів.</p>
          <div className="divide-y divide-slate-100">
            {topicGroups.map((item) => {
              const topic = topicMap.get(item.topicId);
              return (
                <div key={item.topicId} className="flex items-center justify-between gap-3 py-3 text-sm">
                  <div>
                    <p className="font-medium text-slate-800">{topic?.title ?? "Тему видалено"}</p>
                    <p className="text-xs text-slate-400">{topic ? subjectNames[topic.subject] : ""} · {item._count._all} тестів</p>
                  </div>
                  <span className="font-semibold text-slate-700">{Math.round(item._avg.percent ?? 0)}%</span>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900">Найактивніші користувачі</h2>
          <div className="mt-3 divide-y divide-slate-100">
            {userGroups.map((item) => (
              <div key={item.userId} className="flex items-center justify-between gap-3 py-3 text-sm">
                <span className="font-medium text-slate-800">{userMap.get(item.userId)?.username ?? "Акаунт видалено"}</span>
                <span className="text-slate-500">{item._count._all} тестів · {Math.round(item._avg.percent ?? 0)}% у середньому</span>
              </div>
            ))}
            {!userGroups.length ? <p className="py-4 text-sm text-slate-400">Поки немає результатів.</p> : null}
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900">Останні результати</h2>
          <div className="mt-3 divide-y divide-slate-100">
            {latestResults.map((result) => (
              <div key={result.id} className="py-3 text-sm">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-medium text-slate-800">{result.user.username}</span>
                  <span className="font-semibold text-slate-700">{result.percent}% ({result.correct}/{result.total})</span>
                </div>
                <p className="mt-1 text-xs text-slate-500">{subjectNames[result.topic.subject]} · {result.topic.title} · {result.createdAt.toLocaleString("uk-UA")}</p>
              </div>
            ))}
            {!latestResults.length ? <p className="py-4 text-sm text-slate-400">Поки немає результатів.</p> : null}
          </div>
        </div>
      </section>

      <p className="mt-8 text-xs leading-relaxed text-slate-400">
        Онлайн-статус рахується лише для користувачів, які увійшли в акаунт. Дані показують активність на сайті та результати тестів, а не дії поза сайтом.
      </p>
    </main>
  );
}
