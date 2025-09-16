import "@livekit/components-styles";
import "./globals.css";
import { Public_Sans } from "next/font/google";
import type { Metadata } from "next";

const publicSans = Public_Sans({
  weight: ["400", "500", "600", "700"],
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Gober - Santander Territorio inteligente",
  description: "Consulta transparente sobre objetivos estratégicos y avances institucionales de Santander Territorio inteligente",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`h-full ${publicSans.className}`}>
      <body className="h-full bg-background text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
