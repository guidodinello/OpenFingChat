import { Paper } from "@mui/material";

const Message = ({ message }: { message: IMessage }) => {
  return (
    <Paper sx={{ p: 2 }} elevation={4}>
      {message.message}
    </Paper>
  );
};

export default Message;
