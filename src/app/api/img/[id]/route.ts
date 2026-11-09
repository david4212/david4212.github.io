import prisma from "@/lib/prisma";

export const dynamic = "force-dynamic";

// Віддає фото, завантажене через бота
export async function GET(_req: Request, { params }: { params: { id: string } }) {
  const img = await prisma.image.findUnique({ where: { id: params.id } });
  if (!img) return new Response("Not found", { status: 404 });
  return new Response(new Uint8Array(img.data), {
    headers: {
      "Content-Type": img.mime,
      "Cache-Control": "public, max-age=31536000, immutable",
    },
  });
}
