import { Card, Skeleton, Stack } from "@mui/material";

const MessageLoading = () => {
  return (
    <Card sx={{ p: 1 }} variant="outlined">
      <Stack>
        <Skeleton animation="wave" width={"100%"} />
        <Skeleton animation="wave" width={"90%"} />
        <Skeleton animation="wave" width={"60%"} />
      </Stack>
    </Card>
  );
};

export default MessageLoading;
