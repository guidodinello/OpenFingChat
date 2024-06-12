import type { Metadata } from "next";

import { AppRouterCacheProvider } from "@mui/material-nextjs/v13-appRouter";
import Background from "@/components/background";
import { ThemeProvider } from "@mui/material";
import theme from "@/theme/theme";

import "./globals.css";

import { Open_Sans } from "next/font/google";
import { ChatProvider } from "@/features/chat/context";
import { QueryProvider } from "@/features/query/context";
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
        <QueryProvider>
          <ChatProvider>
            <AppRouterCacheProvider>
              <ThemeProvider theme={theme}>
                <Background />
                {children}
              </ThemeProvider>
            </AppRouterCacheProvider>
          </ChatProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
