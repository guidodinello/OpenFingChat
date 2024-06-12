import { useChat } from "@/features/chat/context";
import {
  Container,
  List,
  ListItem,
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
    <Container maxWidth={"md"} sx={{ px: isSmall ? 0 : 2 }}>
      <List sx={{ px: isSmall ? 0 : 4 }}>
        {messages.map((msg, index) => (
          <ListItem key={index}>
            <Message message={msg} />
          </ListItem>
        ))}
        {loading && <MessageLoading />}
      </List>
    </Container>
  );
};

export default MessagesList;
