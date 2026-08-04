import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NexusGateway — Infrastructure FinOps Telemetry",
  description: "Enterprise LLM Autopilot, Semantic Cache & Resilience Gateway Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-zinc-950 text-zinc-100 selection:bg-zinc-800 selection:text-zinc-100">
        {children}
      </body>
    </html>
  );
}
