import { Raleway } from "next/font/google";

const logoFont = Raleway({ subsets: ["latin"] });

const Logo = ({ size = 22, color1 = "#333333", color2 = "#205c9a" }) => {
  return (
    <a
      href="/"
      title="ChatOpenFing"
      className={`${logoFont.className}`}
      style={{ fontSize: size, textDecoration: "none" }}
    >
      <span style={{ color: color1, fontWeight: 400 }}>Chat</span>
      <span style={{ color: color2, fontWeight: 800 }}>OpenFing</span>
    </a>
  );
};

export default Logo;
