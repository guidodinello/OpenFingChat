"use client";
import React from "react";
import { Container, Paper } from "@mui/material";
import Logo from "@/components/logo";
import { useChat } from "@/feature/chat/context";
import { useQuery } from "@/feature/query/context";

const Home = () => {
  const {
    state: { messages, loading },
  } = useChat();
  const { state: query } = useQuery();

  return (
    <Container maxWidth="md">
      <Logo size={40} />
      <Paper elevation={1} style={{ padding: 20, margin: 20 }}>
        {JSON.stringify({ messages, loading })}
      </Paper>
      <Paper elevation={10} style={{ padding: 20, margin: 20 }}>
        {JSON.stringify(query)}
      </Paper>
    </Container>
  );
};

export default Home;
