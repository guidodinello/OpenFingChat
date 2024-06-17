import {
  Box,
  Card,
  Link,
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
  const { breakpoints, palette } = useTheme();
  const isSmall = useMediaQuery(breakpoints.down("sm"));
  console.log(message.error);

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
          <Paper
            sx={{
              py: 1,
              px: 2,
              minWidth: 200,
              bgcolor: message.error
                ? palette.error.light
                : palette.background.paper,
            }}
            elevation={2}
          >
            <Typography
              color={message.error ? "error.dark" : "text.secondary"}
              textAlign={from == "user" ? "right" : "left"}
            >
              {message.message}
            </Typography>
          </Paper>

          {message.sources.length > 0 && (
            <Typography variant="caption">
              Referencias:{" "}
              {message.sources.map((s, index, array) => (
                <>
                  <Link href={`${s.url}?t=${s.start}`} target="_blank">
                    {s.lessonName}
                  </Link>
                  {index === array.length - 1 ? "." : ", "}
                </>
              ))}
            </Typography>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default Message;
