import Search from "@/components/search";
import React from "react";
import { Container, Grid, Typography } from "@mui/material";

const Home = () => {
  const messages: string[] = [];

  return (
    <Container maxWidth="lg">
      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={6}>
          <Typography>1</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>2</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>3</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>4</Typography>
        </Grid>
      </Grid>
      Press Enter to start editing
    </Container>
  );
};

export default Home;
