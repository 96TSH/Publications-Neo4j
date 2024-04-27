import { useState, useEffect, useContext, Fragment } from "react";
import {
  Typography,
  Box,
  List,
  ListItemButton,
  ListItemText,
  CssBaseline,
  ListItem,
  Divider,
  TablePagination,
  TextField,
  Button,
  CircularProgress,
  Backdrop,
  Collapse,
} from "@mui/material";
import FetchContext from "../stores/fetchContext";

const Homepage = () => {
  const { articlesData, fetchArticles, searchArticles, loading } =
    useContext(FetchContext);

  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [open, setOpen] = useState([]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
    fetchArticles(newPage, rowsPerPage);
  };

  const handleChangeRowsPerPage = (event) => {
    const newRowsPerPage = parseInt(event.target.value, 10);
    setRowsPerPage(newRowsPerPage);
    setPage(1);
    fetchArticles(1, newRowsPerPage);
  };

  const handleSearchTermChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchClick = () => {
    searchArticles(searchTerm, page, rowsPerPage);
  };

  const handleResetClick = () => {
    setSearchTerm("");
    fetchArticles(page, rowsPerPage);
  };

  const handleClick = (index) => {
    setOpen((prevOpen) => {
      const newOpen = [...prevOpen];
      newOpen[index] = !newOpen[index];
      return newOpen;
    });
  };

  useEffect(() => {
    fetchArticles(page, rowsPerPage);
  }, []);

  return (
    <Box
      sx={{
        bgcolor: "#f5f5f5",
        height: "100%",
        width: "100%",
        paddingTop: "3%",
        paddingBottom: "3%",
        paddingInline: "6%",
      }}
    >
      <Backdrop open={loading} sx={{ zIndex: 9999, color: "#fff" }}>
        <CircularProgress color="inherit" />
      </Backdrop>
      <TablePagination
        component="div"
        count={
          articlesData && articlesData.total_pages
            ? articlesData.total_pages
            : 100
        }
        page={page}
        onPageChange={handleChangePage}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
      <Box
        sx={{
          display: "flex",
          justifyContent: "right",
          alignItems: "center",
        }}
      >
        <TextField
          id="filled-search"
          label="Search field"
          type="search"
          variant="standard"
          value={searchTerm}
          onChange={handleSearchTermChange}
        />
        <Button
          sx={{ marginInline: "10px" }}
          color="error"
          variant="outlined"
          onClick={handleResetClick}
        >
          Reset
        </Button>
        <Button color="primary" variant="outlined" onClick={handleSearchClick}>
          Search
        </Button>
      </Box>
      <Typography
        variant="h4"
        sx={{ color: "black", fontFamily: "Century", paddingBottom: 2 }}
      >
        Research Publications
      </Typography>
      <CssBaseline />
      <List sx={{ width: "100%", bgcolor: "background.paper" }}>
        {articlesData.articles &&
          articlesData.articles.map((article, index) => (
            <Fragment key={article.pmid}>
              <ListItemButton onClick={() => handleClick(index)}>
                <Box sx={{ width: "100%" }}>
                  <ListItemText
                    primary={article.title}
                    secondary={
                      <Fragment>
                        {`${article.doi}`}
                        <br />
                        <Typography
                          sx={{ display: "inline" }}
                          component="span"
                          variant="body2"
                          color="text.primary"
                        >
                          Journal:{" "}
                          {article.published_by ? article.published_by : ""}
                          <br />
                          Country:{" "}
                          {article.published_in ? article.published_in : ""}
                        </Typography>
                      </Fragment>
                    }
                  />
                  <Collapse in={open[index]} timeout="auto" unmountOnExit>
                    <Typography
                      sx={{ display: "inline" }}
                      component="span"
                      variant="caption"
                      color="text.primary"
                    >
                      Citation Count:{" "}
                      {article.citation_count ? article.citation_count : 0} |{" "}
                      Authors:{" "}
                      {article.authored_by
                        ? article.authored_by.join(", ")
                        : ""}
                    </Typography>
                  </Collapse>
                </Box>
              </ListItemButton>
              <Divider variant="inset" component="li" />
            </Fragment>
          ))}
      </List>
    </Box>
  );
};

export default Homepage;
