import React, { useState, useContext, useEffect } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { AuthContext } from "../../contexts/auth";
import { useNavigate } from "react-router-dom";
import Avatar from "@mui/material/Avatar";
import CssBaseline from "@mui/material/CssBaseline";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Loading from "../../components/Loading";
import { resetpasswordUser } from "../../services/api";


const ResetPassword = () => {
  const { authenticated } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    authenticated && navigate("/");
  }, [authenticated, navigate]);

  const ResetPassword = async (email) => {
    try {
      setLoading(true);
      const response = await resetpasswordUser(email);
      alert("Sua nova senha foi enviada para o seu email.");
      navigate("/login");
    } catch ({ response }) {
      console.log(response.data);
      setError(response.data.error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    ResetPassword(email);
  };

  if (loading) {
    return <Loading />;
  }

  return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h2" variant="h6">
            Digite o seu email para alterar a sua senha.
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              label="Email"
              variant="outlined"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              fullWidth
              margin="normal"
            />
            <span>{error}</span>
            <Button type="submit" fullWidth variant="contained" sx={{ mb: 2 }}>
              Enviar
            </Button>
            <Grid container>
              <Grid item>
                <Link href="/login" variant="body2">
                  Faça login
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
  );
};

export default ResetPassword;
