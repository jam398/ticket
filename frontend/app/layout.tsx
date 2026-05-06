import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TriagePilot AI",
  description: "AI-assisted ticket classification, routing, and response suggestions.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
