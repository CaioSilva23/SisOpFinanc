import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
 
  },
});

export const createSession = (email, password) => {
  return api.post("/login", { email, password });
};

export const registerUser = (name, email, password, password2) => {
  return api.post("/register", { name, email, password, password2 });
};

export const changepasswordUser = (old_password, new_password, new_password2) => {
  return api.patch("/change-password", { old_password, new_password, new_password2 });
};

export const resetpasswordUser = (email) => {
  return api.patch("/reset-password", {email });
};

export const getUserDetail = () => {
  return api.get("/user");
};

export const acoesDisponiveis = () => {
  return api.get("/actions");
};

export const operacaoCompra = (acao_id, quantity) => {
  return api.post("/operations", {acao_id, quantity});
};

export const operacaoVenda = (stock_action, valor_unit, quantity) => {
  return api.post("/actions/user", {stock_action, valor_unit, quantity});
};

export const listOperacoes = () => {
  return api.get("/operations");
};

export const acoesForUser = () => {
  return api.get("/actions/user");
};

export const deleteOperationUser = (id) => {
  return api.delete(`operation/${id}`)
}