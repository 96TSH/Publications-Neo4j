import { Box } from "@mui/material";

const Dashboard = () => {
  const neoDashUrl =
    "http://neodash.graphapp.io/?share&type=database&id=5ce81c80-14a2-4d8f-9017-bd31a960711b&dashboardDatabase=neo4j&credentials=neo4j%2Bs%3A%2F%2Fneo4j%3AteV3BKUHpbDE-OrXCj-5O5SEn1znxzpin_BNubXEGoU%40%3A3038c058.databases.neo4j.io%3A7687&standalone=Yes";

  return (
    <Box
      sx={{
        bgcolor: "#f5f5f5",
        height: "100%",
        width: "100%",
      }}
    >
      <iframe
        src={neoDashUrl}
        style={{ width: "100%", height: "1000px" }}
        title="NeoDash Dashboard"
      />
    </Box>
  );
};

export default Dashboard;
