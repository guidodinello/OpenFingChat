import {
  Box,
  Card,
  Paper,
  Stack,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import Avatar from "./avatar";

const Message = ({
  message,
  from = "chat",
}: {
  message: IMessage;
  from?: "chat" | "user";
}) => {
  const { breakpoints } = useTheme();
  const isSmall = useMediaQuery(breakpoints.down("sm"));

  return (
    <Box
      width="100%"
      display="flex"
      justifyContent={from == "user" ? "flex-end" : "flex-start"}
    >
      <Box
        display="flex"
        alignItems={from == "user" && isSmall ? "flex-end" : "flex-start"}
        flexWrap={"nowrap"}
        flexDirection={
          isSmall ? "column" : from == "user" ? "row-reverse" : "row"
        }
        maxWidth={isSmall ? "90%" : "80%"}
        columnGap={2}
        rowGap={1}
      >
        <Avatar type={from} />
        <Box gap={1} display="flex" flexDirection={"column"}>
          <Paper sx={{ py: 1, px: 2, minWidth: 200 }} elevation={2}>
            <Typography
              color="text.secondary"
              textAlign={from == "user" ? "right" : "left"}
            >
              {message.message}
            </Typography>
          </Paper>
          {message.sources.map((s, index) => (
            <Paper
              key={`source_${index}`}
              sx={{ py: 1, px: 2 }}
              elevation={2}
            ></Paper>
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default Message;
