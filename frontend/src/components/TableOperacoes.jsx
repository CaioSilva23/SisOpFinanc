import { React, Fragment } from "react";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Title from "./Title";

export default function TableOperacoes({ data }) {
  return (
    <Fragment>
      <Title>Transações recentes</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Transação</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Valor unitário</TableCell>
            <TableCell>Quantidade</TableCell>
            <TableCell>Valor total</TableCell>
            <TableCell>Data</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.slice(0, 5).map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.type_operation}</TableCell>
              <TableCell>{row.status}</TableCell>
              <TableCell>R$ {row.price_unit.toFixed(2)}</TableCell>
              <TableCell>{row.quantity}</TableCell>
              <TableCell>R$ {row.price_total.toFixed(2)}</TableCell>
              <TableCell>{row.data_operacao}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Link color="primary" href="/operacoes" sx={{ mt: 3 }}>
        Acesse todo histórico de transações
      </Link>
    </Fragment>
  );
}
