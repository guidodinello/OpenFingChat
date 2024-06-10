"use client";
import { createTheme } from "@mui/material";

import palette from "./palette";
import shadows from "./shadows";
import typography from "./typography";

const theme = createTheme({
  typography,
  palette,
  shadows,
});

export default theme;
