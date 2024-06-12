import { Avatar as AvatarComponent, useTheme } from "@mui/material";
import ChatBubbleIcon from "@mui/icons-material/ChatBubble";
import SchoolIcon from "@mui/icons-material/School";

const Avatar = ({ type = "chat" }: { type: "chat" | "user" }) => {
  const { palette } = useTheme();

  return (
    <AvatarComponent
      sx={{
        bgcolor: type == "user" ? palette.secondary.main : palette.primary.main,
        boxShadow: 2,
      }}
    >
      {type == "user" ? (
        <SchoolIcon fontSize="medium" />
      ) : (
        <ChatBubbleIcon fontSize="small" />
      )}
    </AvatarComponent>
  );
};

export default Avatar;
