"use client";
import React from "react";
import { Box, Container, Grid, Paper } from "@mui/material";
import Logo from "@/components/logo";
import { useChat } from "@/feature/chat/context";

import BottomSearch from "@/components/bottom-search";
import MessagesList from "@/components/messages-list";

const Home = () => {
  const {
    state: { messages, loading },
  } = useChat();

  return (
    <Box height="100%" width="100%">
      {messages.length > 0 && <MessagesList />}

      <Box
        height="100%"
        width="100%"
        paddingBottom={11}
        boxSizing="border-box"
        position="fixed"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <Grid container maxWidth="sm" rowSpacing={6}>
          <Grid item container justifyContent="center">
            <Logo size={30} />
          </Grid>
          {/* <Grid item xs={12}>
            <Paper
              elevation={1}
              sx={{ maxWidth: "sm", py: 2, px: 3, borderRadius: 30 }}
            >
              hola
            </Paper>
          </Grid> */}
        </Grid>
      </Box>

      <BottomSearch />
    </Box>
  );
};

export default Home;
