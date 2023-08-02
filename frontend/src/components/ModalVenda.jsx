import { React, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import Title from "./Title";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "1px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function FormVenda({ handleVenda, id_acao }) {
  const [quantidade, setQuantidade] = useState(0);
  const [preco_unit, setPrecoUnit] = useState(0);
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    handleVenda(id_acao, preco_unit, quantidade);
  };

  return (
    <div>
      <Button onClick={handleOpen} variant="contained" color="success">
        Vender
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} component="form" onSubmit={handleSubmit} noValidate>
          <Typography id="modal-modal-title" component="h6">
            Informe a quantidade que deseja vender.
          </Typography>
          <TextField
            label="Quantidade"
            variant="outlined"
            name="quantidade"
            value={quantidade}
            onChange={(e) => setQuantidade(e.target.value)}
            type="number"
            fullWidth
            margin="normal"
          />
          <TextField
            label="Preço venda (Unitário)"
            variant="outlined"
            name="preco_unit"
            value={preco_unit}
            onChange={(e) => setPrecoUnit(e.target.value)}
            type="number"
            fullWidth
            margin="normal"
          />
          <Title>Total: R$ {(quantidade*preco_unit).toFixed(2)}</Title>

          <Button type="submit" variant="contained" color="success">
            Vender
          </Button>
        </Box>
      </Modal>
    </div>
  );
}
