"use client";
import React from "react";
import { Box } from "@mui/material";
import { useChat } from "@/features/chat/context";

import BottomSearch from "@/components/bottom-search";
import MessagesList from "@/components/messages-list";
import Empty from "@/components/empty";

const Home = () => {
  const {
    state: { messages },
  } = useChat();

  return (
    <Box height="100%" width="100%">
      {messages.length === 0 && <Empty />}
      {messages.length > 0 && <MessagesList />}

      <BottomSearch />
    </Box>
  );
};

export default Home;
