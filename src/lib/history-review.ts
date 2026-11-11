import type { Prisma } from "@prisma/client";

/**
 * Temporary quarantine: 78 legacy illustrations were hand-drawn for the site
 * and have not been independently matched to original examination sources.
 *
 * IMPORTANT: keep historical user scores and questions in the database.
 * Do not expose or score these 292 image-based questions until an editor
 * verifies EACH image and its corresponding answer against a dated source.
 * Non-image questions and separately sourced NMT materials remain available.
 */
export const HISTORY_LEGACY_IMAGE_PREFIX = "/img/history/";

export function isUnverifiedHistoryQuestion(imageUrl: string | null | undefined) {
  return typeof imageUrl === "string" && imageUrl.startsWith(HISTORY_LEGACY_IMAGE_PREFIX);
}

/** Reuse this filter for quizzes, diagnostics, error review and daily questions. */
export const verifiedQuestionWhere: Prisma.QuestionWhereInput = {
  OR: [
    { imageUrl: null },
    { NOT: { imageUrl: { startsWith: HISTORY_LEGACY_IMAGE_PREFIX } } },
  ],
};

/** Metadata for a verifiable exam source; add an item only after source audit. */
export type VerifiedExamMap = {
  id: string;
  title: string;
  period: string;
  sourceName: string;
  sourceUrl: string;
  imageUrl?: string;
  examYear?: number;
  questionNumber?: number;
  key: string;
  explanation: string;
  /** Legend written from the original map task, never from an invented SVG. */
  legend?: string[];
  sourceType: "official" | "exam_archive";
};
