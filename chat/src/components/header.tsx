import { Box, Container, Paper, useMediaQuery, useTheme } from "@mui/material";
import Logo from "./logo";

const Header = () => {
  const { breakpoints } = useTheme();
  const isSmall = useMediaQuery(breakpoints.down("sm"));

  return (
    <Paper
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 2,
        py: isSmall ? 1.25 : 2,
      }}
      elevation={2}
    >
      <Container maxWidth="md">
        <Box px={isSmall ? 0 : 7}>
          <Logo />
        </Box>
      </Container>
    </Paper>
  );
};

export default Header;
