import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import GlobalStyles from "@mui/material/GlobalStyles";
import Container from "@mui/material/Container";
import NavBar from "../../components/NavBar";
import { useState, useEffect, React, Fragment } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { listOperacoes, deleteOperationUser } from "../../services/api";
import ModalDeleteOperacao from "../../components/ModalDeleteOperacao";
import Title from "../../components/Title";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import { TablePagination } from "@mui/material";
import Loading from "../../components/Loading";

const Operacoes = () => {
  const [operacoes, setOperacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5); // Quantidade de linhas por página

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0); // Volta para a primeira página ao mudar o número de linhas por página
  };

  useEffect(() => {
    (async () => {
      try {
        const response = await listOperacoes();
        const data = response.data;
        setOperacoes(data.Operações);
        setLoading(false);
      } catch ({ response }) {
        console.log(response.data.error);
      }
    })();
  }, []);

  const deleteOperacao = async (id) => {
    try {
      const response = await deleteOperationUser(id);
      setOperacoes(operacoes.filter((operacao) => operacao.id !== id));
      alert("Seu histórico de transação foi deletado com sucesso.");
    } catch ({ response }) {
      alert("Você só pode deletar transações finalizadas.");
      console.log(response.data.error);
    }
  };

  if (loading) {
    return <Loading />;
  }
  return (
    <>
      <GlobalStyles
        styles={{ ul: { margin: 0, padding: 0, listStyle: "none" } }}
      />
      <CssBaseline />
      <NavBar />
      <Box
        component="main"
        sx={{
          backgroundColor: (theme) =>
            theme.palette.mode === "light"
              ? theme.palette.grey[200]
              : theme.palette.grey[900],
          flexGrow: 1,
          height: "100vh",
          overflow: "auto",
        }}
      >
        <Container
          disableGutters
          maxWidth="sm"
          component="main"
          sx={{ pt: 8, pb: 6 }}
        >
          <Typography
            component="h2"
            variant="h3"
            align="center"
            color="text.secondary"
            gutterBottom
          >
            Minhas operações
          </Typography>
        </Container>
        {/* End hero unit */}
        <Container maxWidth="lg" component="main" sx={{ mt: 1, mb: 10 }}>
          <Fragment>
            {/* Recent Orders */}
            <Grid item xs={12}>
              <Typography
                variant="h5"
                sx={{ mb: 2 }}
                color="text.secondary"
                component="p"
              >
                Consulte suas operações de compra e vendas de ações
              </Typography>
              <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
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
                      <TableCell>Deletar</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {operacoes
                      .slice(
                        page * rowsPerPage,
                        page * rowsPerPage + rowsPerPage
                      )
                      .map((row) => (
                        <TableRow key={row.id}>
                          <TableCell>{row.type_operation}</TableCell>
                          <TableCell>{row.status}</TableCell>
                          <TableCell>$ {row.price_unit}</TableCell>
                          <TableCell>{row.quantity}</TableCell>
                          <TableCell>$ {row.price_total}</TableCell>
                          <TableCell>{row.data_operacao}</TableCell>
                          <TableCell>
                            <ModalDeleteOperacao
                              handleRemove={deleteOperacao}
                              id={row.id}
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
                <TablePagination
                  rowsPerPageOptions={[5, 10, 25]} // Opções de quantidades de linhas por página
                  component="div"
                  count={operacoes.length} // Total de registros
                  rowsPerPage={rowsPerPage}
                  page={page}
                  onPageChange={handleChangePage}
                  onRowsPerPageChange={handleChangeRowsPerPage}
                />
              </Paper>
            </Grid>
          </Fragment>
        </Container>
      </Box>
    </>
  );
};

export default Operacoes;
