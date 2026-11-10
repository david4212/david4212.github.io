import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import AuthProvider from "@/components/shared/AuthProvider";
import UserBar from "@/components/shared/UserBar";
import PresenceTracker from "@/components/shared/PresenceTracker";

const inter = Inter({ subsets: ["latin", "cyrillic"] });

export const metadata: Metadata = {
  title: "НМТ на 200 | Підготовка",
  description: "Твій найкращий помічник для підготовки до НМТ. Трекер прогресу та флеш-картки.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="uk">
      <body className={`${inter.className} antialiased`}>
        <AuthProvider>
          <UserBar />
          <PresenceTracker />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
