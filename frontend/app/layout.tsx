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
  title: "Asistente Virtual - Alcaldía de Cajicá",
  description: "Consulta transparente sobre el Plan de Desarrollo Municipal 'Cajicá Ideal 2024-2027' - Información oficial de indicadores y servicios municipales",
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
