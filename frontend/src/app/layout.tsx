import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Toaster } from "react-hot-toast";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
});

export const metadata: Metadata = {
  title: "OmniFlow.AI | The Universal Multi-Tool Agent Platform",
  description: "Production-grade ReAct agent platform with tools, reasoning, and multi-agent orchestration.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased bg-background text-foreground min-h-screen flex flex-col selection:bg-accent selection:text-white`}>
        {children}
        <Toaster 
          position="top-right" 
          toastOptions={{
            className: 'dark:bg-card dark:text-foreground border dark:border-border glass',
            style: {
              background: 'var(--card)',
              color: 'var(--foreground)',
              border: '1px solid var(--border)',
              backdropFilter: 'blur(10px)',
            }
          }} 
        />
      </body>
    </html>
  );
}
