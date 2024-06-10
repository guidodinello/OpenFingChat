import { TypographyOptions } from "@mui/material/styles/createTypography";
import { Open_Sans } from "next/font/google";
const font = Open_Sans({ subsets: ["latin"] });

const typography: TypographyOptions = {
  fontFamily: font.style.fontFamily,
};

export default typography;
