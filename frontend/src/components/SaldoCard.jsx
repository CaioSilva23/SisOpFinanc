import * as React from "react";
import Typography from "@mui/material/Typography";
import Title from "./Title";

export default function SaldoCard({ user }) {
  const data = new Date();
  return (
    <React.Fragment>
      <Title>Seu saldo</Title>
      <Typography component="p" variant="h4">
        R$ {user.money ? user.money.toFixed(2) : 0}
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        {data.toLocaleString()}
      </Typography>
    </React.Fragment>
  );
}
