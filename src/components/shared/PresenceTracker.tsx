"use client";

import { useEffect } from "react";
import { useSession } from "next-auth/react";

export default function PresenceTracker() {
  const { status } = useSession();

  useEffect(() => {
    if (status !== "authenticated") return;

    const ping = () => {
      fetch("/api/presence", { method: "POST", keepalive: true }).catch(() => {});
    };

    ping();
    const timer = window.setInterval(ping, 30_000);
    return () => window.clearInterval(timer);
  }, [status]);

  return null;
}
