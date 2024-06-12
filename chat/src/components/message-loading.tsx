import {
  Box,
  Card,
  Skeleton,
  Stack,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import Avatar from "./avatar";

const MessageLoading = () => {
  const { breakpoints } = useTheme();
  const isSmall = useMediaQuery(breakpoints.down("sm"));

  return (
    <Box
      width="100%"
      display="flex"
      alignItems="flex-start"
      justifyContent="space-between"
      maxWidth={isSmall ? "90%" : "80%"}
      flexDirection={isSmall ? "column" : "row"}
      rowGap={1}
      columnGap={2}
    >
      <Avatar type="chat" />
      <Card sx={{ p: 1, width: "100%" }} elevation={2}>
        <Stack>
          <Skeleton animation="wave" width={"100%"} />
          <Skeleton animation="wave" width={"90%"} />
          <Skeleton animation="wave" width={"65%"} />
        </Stack>
      </Card>
    </Box>
  );
};

export default MessageLoading;
