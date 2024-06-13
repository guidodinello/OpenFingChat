import { Raleway } from "next/font/google";

const logoFont = Raleway({ subsets: ["latin"] });

const Logo = ({
  size = 22,
  color1 = "#ff9800",
  color2 = "#205c9a",
  shadow = false,
}) => {
  return (
    <a
      href="/"
      title="ChatOpenFing"
      className={`${logoFont.className}`}
      style={{
        fontSize: size,
        textDecoration: "none",
        textShadow: shadow ? "2px 2px 8px rgba(0,0,0,0.2)" : "none",
      }}
    >
      <span style={{ color: color1, fontWeight: 400 }}>Chat</span>
      <span style={{ color: color2, fontWeight: 800 }}>OpenFing</span>
    </a>
  );
};

export default Logo;
