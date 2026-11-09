"use client";

import { useEffect, useState } from "react";
import { X } from "lucide-react";

// Картинка, яка збільшується по кліку (lightbox)
export default function ZoomImage({ src, alt = "", className = "" }: { src: string; alt?: string; className?: string }) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={src}
        alt={alt}
        onClick={(e) => {
          e.stopPropagation();
          setOpen(true);
        }}
        className={`cursor-zoom-in rounded-2xl object-contain ${className}`}
      />
      {open && (
        <div className="fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4" onClick={(e) => { e.stopPropagation(); setOpen(false); }}>
          <button className="absolute top-4 right-4 p-2 rounded-full bg-white/20 text-white hover:bg-white/30 transition" aria-label="Закрити">
            <X className="w-6 h-6" />
          </button>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={src} alt={alt} className="max-h-full max-w-full rounded-xl" onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </>
  );
}
