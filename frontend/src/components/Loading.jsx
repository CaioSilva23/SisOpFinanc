import React from "react";
import { CircularProgress, Box } from "@mui/material";

const Loading = () => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height="100vh"
      bgcolor="#f0f0f0" // Cor de fundo
    >
      <CircularProgress color="primary" />
    </Box>
  );
};

export default Loading;
