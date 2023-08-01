import { React, useEffect, useState } from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import GraficoOperacoes from "../../components/GraficoOperacoes";
import SaldoCard from "../../components/SaldoCard";
import NavBar from "../../components/NavBar";
import { getUserDetail, listOperacoes } from "../../services/api";
import Typography from "@mui/material/Typography";
import Loading from "../../components/Loading";
import TableOperacoes from "../../components/TableOperacoes";

const Home = () => {
  const [user, setUser] = useState({});
  const [loading, setLoading] = useState(true);
  const [operacoes, setOperacoes] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const response = await getUserDetail();
        console.log(response.data);
        setUser(response.data);
      } catch ({ error }) {
        console.log(error.data);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const response = await listOperacoes();
        const data = response.data;
        setOperacoes(data.Operações);
      } catch ({ response }) {
        console.log(response.data.error);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return <Loading />;
  }

  return (
    <>
      <NavBar />
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
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
          <Toolbar />
          <Container maxWidth="lg" sx={{ mt: 1, mb: 10 }}>
            <Typography
              variant="h5"
              sx={{ mb: 2 }}
              color="text.secondary"
              component="p"
            >
              Bem vindo {user.name}, analise seus investimentos.
            </Typography>
            <Grid container spacing={3}>
              {/* Chart */}
              <Grid item xs={12} md={8} lg={9}>
                <Paper
                  sx={{
                    p: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: 240,
                  }}
                >
                  <GraficoOperacoes data={operacoes} />
                </Paper>
              </Grid>
              {/* Recent Deposits */}
              <Grid item xs={12} md={4} lg={3}>
                <Paper
                  sx={{
                    p: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: 240,
                  }}
                >
                  <SaldoCard user={user} />
                </Paper>
              </Grid>
              {/* Recent Orders */}
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
                  <TableOperacoes data={operacoes} />
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Box>
    </>
  );
};

export default Home;
