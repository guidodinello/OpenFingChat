import type { Metadata } from "next";

import { AppRouterCacheProvider } from "@mui/material-nextjs/v13-appRouter";
import Background from "@/components/background";
import { ThemeProvider } from "@mui/material";
import theme from "@/theme/theme";

import "./globals.css";

import { Open_Sans } from "next/font/google";
const font = Open_Sans({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Fing Chat",
  description: "Chatbot for students using OpenFing platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={font.className}>
        <AppRouterCacheProvider>
          <ThemeProvider theme={theme}>
            <Background />
            {children}
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
