import { React, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function FormCompra({ handleCompra, id_acao }) {
  const [quantidade, setQuantidade] = useState(0);
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    handleCompra(id_acao, quantidade);
    handleClose(false)
  };

  return (
    <div>
      <Button onClick={handleOpen} variant="contained" color="success">
        Comprar
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} component="form" onSubmit={handleSubmit} noValidate>
          <Typography id="modal-modal-title" component="h6">
            Informe a quantidade que deseja comprar.
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
          <Button type="submit" variant="contained" color="success">
            Comprar
          </Button>
        </Box>
      </Modal>
    </div>
  );
}
