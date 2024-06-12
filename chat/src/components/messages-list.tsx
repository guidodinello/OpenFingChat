import { useChat } from "@/features/chat/context";
import {
  List,
  ListItem,
  Container,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import Message from "./message";
import MessageLoading from "./message-loading";

const MessagesList = () => {
  const {
    state: { messages, loading },
  } = useChat();
  const { breakpoints } = useTheme();
  const isSmall = useMediaQuery(breakpoints.down("sm"));

  return (
    <Container
      maxWidth="md"
      sx={{
        pb: isSmall ? 10 : 12,
        pt: isSmall ? 6 : 8,
        px: isSmall ? 0 : 2,
        overflow: "auto",
      }}
    >
      <List sx={{ px: isSmall ? 2 : 7 }}>
        {messages.map((msg, index) => (
          <ListItem key={index} sx={{ px: 0 }}>
            <Message message={msg} from={index % 2 == 0 ? "user" : "chat"} />
          </ListItem>
        ))}
        {loading && (
          <ListItem key={-1} sx={{ px: 0 }}>
            <MessageLoading />
          </ListItem>
        )}
      </List>
    </Container>
  );
};

export default MessagesList;
