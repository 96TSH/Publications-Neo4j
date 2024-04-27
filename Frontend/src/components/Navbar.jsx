import { Box, Typography } from "@mui/material";
import { Link, Outlet } from "react-router-dom";

const Navbar = () => {
  const styles = {
    link: {
      color: "maroon",
      fontFamily: "Century Gothic",
      padding: 20,
      fontSize: 20,
    },
  };

  return (
    <Box>
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        sx={{ paddingInline: 5, backgroundColor: "lightgray" }}
      >
        <Typography
          align="left"
          variant="h3"
          sx={{ color: "black", fontFamily: "century", px: 2, py: 2 }}
        >
          <b>NEOPUB</b>
        </Typography>
        <nav>
          <Link to="/" style={styles.link}>
            Home
          </Link>
          <Link to="/dashboard" style={styles.link}>
            Dashboard
          </Link>
        </nav>
      </Box>
      <Outlet />
    </Box>
  );
};

export default Navbar;
