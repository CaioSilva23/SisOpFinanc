import React, { useState, useContext } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { AuthContext } from "../../contexts/auth";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import NavBar from "../../components/NavBar";
import Toolbar from "@mui/material/Toolbar";

const FormChangePassword = () => {
  const { ChangePassword, error } = useContext(AuthContext);
  const [old_password, setOld_password] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    ChangePassword(old_password, password, password2);
    setOld_password("");
    setPassword("");
    setPassword2("");
  };

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

          <Container component="main" maxWidth="xs">
            <Typography textAlign="center" component="h1" variant="h5">
              Altere a sua senha.
            </Typography>
            <Box
              component="form"
              onSubmit={handleSubmit}
              noValidate
              sx={{ mt: 1 }}
            >
              <TextField
                label="Senha atual"
                variant="outlined"
                name="old_password"
                value={old_password}
                onChange={(e) => setOld_password(e.target.value)}
                type="password"
                fullWidth
                margin="normal"
              />
              <span>
                {error.old_password
                  ? "Senha atual inválida, digite sua senha."
                  : ""}{" "}
              </span>
              <TextField
                label="Nova senha"
                variant="outlined"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                fullWidth
                margin="normal"
              />
              <span>{error.password}</span>

              <TextField
                label="Confirme sua nova senha"
                variant="outlined"
                name="password2"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                type="password"
                fullWidth
                margin="normal"
              />
              <span>{error.error}</span>

              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mb: 2 }}
              >
                Confirmar
              </Button>
            </Box>
          </Container>
        </Box>
      </Box>
      {/* <Container
       component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            
          }}
        >
          
        </Box>
      </Container> */}
    </>
  );
};

export default FormChangePassword;
