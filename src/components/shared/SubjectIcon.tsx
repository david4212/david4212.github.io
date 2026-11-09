import { BookOpen, Landmark, Languages, Sigma, type LucideIcon } from "lucide-react";
import type { Subject } from "@/types";

const ICONS: Record<Subject, LucideIcon> = {
  UKRAINIAN: BookOpen,
  HISTORY: Landmark,
  MATH: Sigma,
  ENGLISH: Languages,
};

export default function SubjectIcon({ subject, className = "" }: { subject: Subject; className?: string }) {
  const Icon = ICONS[subject];
  return <Icon className={className} />;
}
