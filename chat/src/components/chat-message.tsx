import "katex/dist/katex.min.css";
import Latex from "react-latex-next";

const ChatMessage = ({ children }: { children: string }) => {
  const format = (str: string) => {
    let res = str;
    res = res.replace(/\n\n/g, "<br/><br/>");
    res = res.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

    return res;
  };

  return <Latex macros={{ "\\f": "#1f(#2)" }}>{format(children)}</Latex>;
};

export default ChatMessage;
