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
import { operacaoCompra, acoesDisponiveis } from "../../services/api";
import ModalCompra from "../../components/ModalCompra";
import Loading from "../../components/Loading";

const Mercado = () => {
  const [acoes, setAcoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [acao_id, setAcao_id] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const response = await acoesDisponiveis();
        setAcoes(response.data.Ações);
        setLoading(false);
      } catch (error) {
        console.log(error.data);
      }
    })();
  }, [acao_id]);

  const postOperacaoCompra = async (id_acao, quantidade) => {
    try {
      const response = await operacaoCompra(id_acao, quantidade);
      console.log(response);
      setAcao_id(id_acao);
      // setAcoes(acoes.filter((acao) => acao.id !== id_acao)) #;
      alert("Ação comprada com sucesso!");
    } catch ({ response }) {
      alert(response.data.error);
      console.log(response.data.error);
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
          <Typography
            component="h2"
            variant="h3"
            align="center"
            color="text.primary"
            gutterBottom
          >
            Mercado de ações
          </Typography>
          <Typography
            variant="h5"
            align="center"
            color="text.secondary"
            component="p"
          >
            Compre e venda ações quando e como quiser.
          </Typography>
        </Container>
        {/* End hero unit */}
        <Container maxWidth="lg" component="main">
          <Grid container spacing={3} pb={12} alignItems="flex-end">
            {acoes.map((acao) => (
              <Grid item key={acao.id} xs={12} sm={6} md={4}>
                <Card>
                  <CardHeader
                    title={acao.name}
                    subheader={acao.description}
                    titleTypographyProps={{ align: "center" }}
                    action={acao.oferta ? <StarIcon /> : null}
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
                      Estoque {acao.stock}
                    </Typography>

                    <Typography variant="subtitle1" align="center">
                      <ModalCompra
                        handleCompra={postOperacaoCompra}
                        id_acao={acao.id}
                        price_unit={acao.price_unit}
                      ></ModalCompra>
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

export default Mercado;
