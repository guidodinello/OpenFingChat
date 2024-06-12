import { resetChat, sendMessage } from "@/features/chat/actions";
import { resetQueryParams, setQueryParams } from "@/features/query/actions";
import {
  Paper,
  Container,
  IconButton,
  TextField,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import ReplayIcon from "@mui/icons-material/Replay";
import SendIcon from "@mui/icons-material/Send";
import { useChat } from "@/features/chat/context";
import { useQuery } from "@/features/query/context";

const BottomSearch = () => {
  const { breakpoints } = useTheme();
  const isSmall = useMediaQuery(breakpoints.down("sm"));

  const {
    state: { messages, loading },
    dispatch: dispatchChat,
  } = useChat();
  const { state: query, dispatch: dispatchQuery } = useQuery();

  const onSend = () => {
    if (query.query?.length === 0) return;

    sendMessage(query, dispatchChat);
    dispatchQuery(setQueryParams({ query: "" }));
  };

  const onReset = () => {
    dispatchChat(resetChat());
    dispatchQuery(resetQueryParams());
  };

  const onEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const onChangeQuery = (e: React.ChangeEvent<HTMLInputElement>) =>
    dispatchQuery(setQueryParams({ query: e.target.value }));

  return (
    <Paper
      sx={{ position: "fixed", bottom: 0, left: 0, right: 0, py: 2 }}
      elevation={6}
    >
      <Container
        maxWidth="md"
        sx={{
          display: "flex",
          justifyContent: "space-between",
          gap: 0.5,
        }}
      >
        <IconButton
          color="default"
          size={isSmall ? "small" : "large"}
          disabled={messages.length === 0}
          onClick={onReset}
        >
          <ReplayIcon />
        </IconButton>
        <TextField
          variant="outlined"
          required
          multiline
          fullWidth
          size={isSmall ? "small" : "medium"}
          maxRows={5}
          placeholder="Envia tu pregunta al chat ..."
          value={query.query}
          onKeyDown={onEnter}
          onChange={onChangeQuery}
        />
        <IconButton
          color="primary"
          onClick={onSend}
          disabled={loading || query.query?.length === 0}
          size={isSmall ? "small" : "large"}
        >
          <SendIcon />
        </IconButton>
      </Container>
    </Paper>
  );
};

export default BottomSearch;
