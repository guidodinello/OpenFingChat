"use client";
import { createTheme } from "@mui/material";
import { Open_Sans } from "next/font/google";

const font = Open_Sans({ subsets: ["latin"] });

const theme = createTheme({
  typography: { fontFamily: font.style.fontFamily },
  palette: {
    primary: {
      main: "#205c9a",
      light: "#4d8cbf",
      dark: "#003666",
    },
    secondary: {
      main: "#ff9800",
      light: "#ffd180",
      dark: "#f57c00",
    },
    error: {
      main: "#f44336",
      light: "#ff7961",
      dark: "#ba000d",
    },
    warning: {
      main: "#ff9800",
      light: "#ffd180",
      dark: "#f57c00",
    },
    info: {
      main: "#2196f3",
      light: "#64b5f6",
      dark: "#1976d2",
    },
    success: {
      main: "#4caf50",
      light: "#81c784",
      dark: "#388e3c",
    },
  },
});

export default theme;
