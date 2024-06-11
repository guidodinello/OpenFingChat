import { resetChat, setChatLoading } from "@/feature/chat/actions";
import { resetQueryParams, setQueryParams } from "@/feature/query/actions";
import { Paper, Container, Grid, IconButton, TextField } from "@mui/material";
import ReplayIcon from "@mui/icons-material/Replay";
import SendIcon from "@mui/icons-material/Send";
import { useChat } from "@/feature/chat/context";
import { useQuery } from "@/feature/query/context";

const BottomSearch = () => {
  const {
    state: { messages, loading },
    dispatch: dispatchChat,
  } = useChat();
  const { state: query, dispatch: dispatchQuery } = useQuery();

  const onSend = () => {
    dispatchChat(setChatLoading(true));
    dispatchQuery(setQueryParams({ query: "" }));
  };

  return (
    <Paper
      sx={{ position: "fixed", bottom: 0, left: 0, right: 0, py: 2 }}
      elevation={6}
    >
      <Container maxWidth="md">
        <Grid container wrap="nowrap" spacing={2}>
          <Grid item xs={1}>
            <IconButton
              color="default"
              size="large"
              disabled={messages.length === 0}
              onClick={() => {
                dispatchChat(resetChat());
                dispatchQuery(resetQueryParams());
              }}
            >
              <ReplayIcon />
            </IconButton>
          </Grid>
          <Grid item xs={10}>
            <TextField
              variant="outlined"
              required
              multiline
              fullWidth
              maxRows={5}
              placeholder="Envia tu pregunta al chat ..."
              value={query.query}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  onSend();
                }
              }}
              onChange={(e) =>
                dispatchQuery(setQueryParams({ query: e.target.value }))
              }
            />
          </Grid>
          <Grid item xs={1}>
            <IconButton
              color="primary"
              size="large"
              onClick={onSend}
              disabled={loading}
            >
              <SendIcon />
            </IconButton>
          </Grid>
        </Grid>
      </Container>
    </Paper>
  );
};

export default BottomSearch;
