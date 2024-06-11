import { useChat } from "@/feature/chat/context";
import { Container, List, ListItem } from "@mui/material";
import Message from "./message";
import MessageLoading from "./message-loading";

const MessagesList = () => {
  const {
    state: { messages, loading },
  } = useChat();

  return (
    <Container maxWidth="sm">
      <List>
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
