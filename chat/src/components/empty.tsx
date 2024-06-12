import { Box, Grid } from "@mui/material";
import Logo from "./logo";

const Empty = () => {
  return (
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
      <Grid container maxWidth="md" rowSpacing={6}>
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
  );
};

export default Empty;
