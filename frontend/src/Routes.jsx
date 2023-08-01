import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import Mercado from "./pages/MercadoAcoes/Mercado";
import Operacoes from "./pages/TransacoesUser/Operacoes";
import Acoes from "./pages/TransacoesUser/Acoes";
import Login from "./pages/Auth/Login";
import ResetPassword from "./pages/Auth/ResetPassword";
import Home from "./pages/Home/Home";
import Register from "./pages/Auth/Register";
import { AuthProvider, AuthContext } from "./contexts/auth";
import React, { useContext } from "react";
import Loading from "./components/Loading";
import ChangePassword from "./pages/Auth/ChangePassword";


const RoutesApp = () => {
  const Private = ({ children }) => {
    const { authenticated, loading } = useContext(AuthContext);

    if (loading) {
      return <Loading />;
    }

    if (!authenticated) {
      return <Navigate to={"/login"} />;
    }

    return children;
  };

  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route
            exact
            path="/"
            element={
              <Private>
                <Home />
              </Private>
            }
          />
          <Route
            exact
            path="/acoes"
            element={
              <Private>
                <Mercado />
              </Private>
            }
          />
          <Route
            exact
            path="/operacoes"
            element={
              <Private>
                <Operacoes />
              </Private>
            }
          />
          <Route
            exact
            path="/acoes/user"
            element={
              <Private>
                <Acoes />
              </Private>
            }
          />
          <Route
            exact
            path="change-password"
            element={
              <Private>
                <ChangePassword />
              </Private>
            }
          />
          <Route
            exact
            path="reset-password"
            element={<ResetPassword />}
          ></Route>
          <Route path="/login" element={<Login />} />
          <Route exact path="/register" element={<Register />} />
          <Route path="*" element={<Login />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default RoutesApp;
