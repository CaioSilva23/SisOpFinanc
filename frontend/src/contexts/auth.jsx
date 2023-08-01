import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  api,
  createSession,
  registerUser,
  changepasswordUser,
} from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const recoveredUser = localStorage.getItem("user");
    const token = localStorage.getItem("token");

    if (recoveredUser && token) {
      setUser(JSON.parse(recoveredUser));
      api.defaults.headers.Authorization = `Bearer ${token}`;
    }

    setLoading(false);
  }, []);

  const AuthLogin = async (email, password) => {
    try {
      const { data } = await createSession(email, password);
      const token = data.token;
      const loggerUser = { email };

      console.log(data);

      localStorage.setItem("user", JSON.stringify(loggerUser));
      localStorage.setItem("token", token);

      api.defaults.headers.Authorization = `Bearer ${token}`;

      setUser(loggerUser);
      navigate("/");
      setError("");
    } catch ({ response }) {
      console.log(response.data);
      setError(response.data.error);
    }
  };

  const AuthRegister = async (name, email, password, password2) => {
    try {
      const response = await registerUser(name, email, password, password2);
      console.log(response.data);
      alert("Cadastro realizado com sucesso!");
      setError("");
      navigate("/");
    } catch ({ response }) {
      console.log(response.data.email);

      setError({
        error: response.data.error,
        email: response.data.email,
        password: response.data.password,
      });
    }
  };

  const ChangePassword = async (old_password, new_password, new_password2) => {
    try {
      const response = await changepasswordUser(
        old_password,
        new_password,
        new_password2
      );
      console.log(response.data);
      setError("");
      alert("Senha alterada com sucesso!");
      navigate("/");
    } catch ({ response }) {
      console.log(response.data);
      setError({
        error: response.data.error,
        password: response.data.password,
        old_password: response.data.old_password,
      });
    }
  };

  const logout = () => {
    console.log("logout");
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  };
  return (
    <AuthContext.Provider
      value={{
        authenticated: !!user,
        user,
        error,
        loading,
        AuthLogin,
        AuthRegister,
        ChangePassword,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
