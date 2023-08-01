import { React, useContext, useState } from "react";
import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import { AuthContext } from "../contexts/auth";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

const NavBar = () => {
  const { logout } = useContext(AuthContext);

  const handleLogout = () => {
    logout();
  };

  const [anchorElUser, setAnchorElUser] = useState(null);

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    <>
      <AppBar
        position="static"
        color="default"
        elevation={0}
        sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}
      >
        <Toolbar sx={{ flexWrap: "wrap" }}>
          <Typography variant="h5" color="inherit" noWrap sx={{ flexGrow: 1 }}>
            <Link href="/" color="text.primary">
              SisOp Financ
            </Link>
          </Typography>
          <nav>
            <Link
              variant="button"
              color="text.primary"
              href="/"
              sx={{ my: 1, mx: 1.5 }}
            >
              Home
            </Link>
            <Link
              variant="button"
              color="text.primary"
              href="/acoes"
              sx={{ my: 1, mx: 1.5 }}
            >
              Compra Ações
            </Link>

            <Link
              variant="button"
              color="text.primary"
              href="/operacoes"
              sx={{ my: 1, mx: 1.5 }}
            >
              SUAS OPERAÇÕES
            </Link>
            <Link
              variant="button"
              color="text.primary"
              href="/acoes/user"
              sx={{ my: 1, mx: 1.5 }}
            >
              SUAS AÇÕES
            </Link>
          </nav>
          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 1 }}>
                <AccountCircleIcon sx={{ width: 40, height: 40 }}/>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: "45px" }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              <MenuItem >
                <Button href="/">Dasboard</Button>
              </MenuItem>
              <MenuItem>
                <Button href="/change-password">Alterar senha</Button>
              </MenuItem>
              <MenuItem>
                <Button onClick={handleLogout}>Logout</Button>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
    </>
  );
};
export default NavBar;
