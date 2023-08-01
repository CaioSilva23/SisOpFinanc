import { React, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardHeader from "@mui/material/CardHeader";
import Grid from "@mui/material/Grid";
import StarIcon from "@mui/icons-material/StarBorder";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import NavBar from "../../components/NavBar";
import { acoesForUser, operacaoVenda } from "../../services/api";
import ModalVenda from "../../components/ModalVenda";
import Loading from "../../components/Loading";

const Acoes = () => {
  const [acoes, setAcoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [acao_id, setAcaoId] = useState("")

  useEffect(() => {
    (async () => {
      try {
        const response = await acoesForUser();
        const data = response.data;
        setAcoes(data.acoes);
        setLoading(false);
      } catch ({ error }) {
        console.log(error.data);
      }
    })();
  }, [acao_id]);

  const postOperacaoVenda = async (id_acao, preco_unit, quantidade) => {
    try {
      const response = await operacaoVenda(id_acao, preco_unit, quantidade);
      console.log(response);
      setAcaoId(id_acao)
      alert("Sua ação foi anunciada com uma oferta.");
    } catch ({ response }) {
      console.log(response.data.error);
      alert(response.data.error);
    }
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <>
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
          <>
            {!acoes.length ? (
              <Typography
                variant="h5"
                align="center"
                color="text.secondary"
                component="p"
              >
                {
                  "Voce não possui ações, realize operações de compra, no mercado de ações."
                }
              </Typography>
            ) : (
              <>
                <Typography
                  component="h2"
                  variant="h3"
                  align="center"
                  color="text.primary"
                  gutterBottom
                >
                  Minhas ações
                </Typography>

                <Typography
                  variant="h5"
                  align="center"
                  color="text.secondary"
                  component="p"
                >
                  Você pode vender as suas ações em forma de oferta, com o preço
                  e as quantidades que desejar.
                </Typography>
              </>
            )}
          </>
        </Container>
        {/* End hero unit */}
        <Container maxWidth="lg" component="main">
          <Grid container spacing={3} pb={12} alignItems="flex-end">
            {acoes.map((acao) => (
              <Grid item key={acao.stock_id} xs={12} sm={6} md={4}>
                <Card>
                  <CardHeader
                    title={acao.name}
                    subheader={acao.description}
                    titleTypographyProps={{ align: "center" }}
                    action={acao.name === "Pro" ? <StarIcon /> : null}
                    subheaderTypographyProps={{
                      align: "center",
                    }}
                    sx={{
                      backgroundColor: (theme) =>
                        theme.palette.mode === "light"
                          ? theme.palette.grey[300]
                          : theme.palette.grey[900],
                    }}
                  />
                  <CardContent>
                    <Box
                      sx={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "baseline",
                        mb: 2,
                      }}
                    >
                      <Typography
                        component="h2"
                        variant="h4"
                        color="text.primary"
                      >
                        R$ {acao.price_unit.toFixed(2)}
                      </Typography>
                    </Box>
                    <Typography variant="subtitle1" align="center">
                      Seu estoque {acao.quantity}
                    </Typography>
                    <Typography variant="subtitle1" align="center">
                      <ModalVenda
                        handleVenda={postOperacaoVenda}
                        id_acao={acao.stock_id}
                      ></ModalVenda>
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
    </>
  );
};

export default Acoes;
