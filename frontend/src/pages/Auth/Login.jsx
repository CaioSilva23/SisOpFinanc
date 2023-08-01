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

const Login = () => {
  const { authenticated, AuthLogin, error } = useContext(AuthContext);
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    authenticated && navigate("/");
  }, [authenticated, navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    AuthLogin(email, password);
    setEmail("");
    setPassword("");
  };

  return (
    <>
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
          <Typography component="h1" variant="h5">
            Faça login no sistema
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
            <TextField
              label="Senha"
              variant="outlined"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              fullWidth
              margin="normal"
            />
            <span>{error}</span>

            <Button type="submit" fullWidth variant="contained" sx={{ mb: 2 }}>
              Login
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="/reset-password" variant="body2">
                  Esqueceu a senha ?
                </Link>
              </Grid>
              <Grid item>
                <Link href="/register" variant="body2">
                  Cadastre-se
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </>
  );
};

export default Login;
