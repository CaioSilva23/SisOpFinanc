import {React, useState} from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
  

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

export default function ModalDelete({handleRemove, id}) {
  const [operacao, setOperacao] = useState(id)
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    handleRemove(id);
  };


  return (
    <div>
      <Button onClick={handleOpen} size="small" variant="contained" color="error">
        <DeleteForeverIcon/>
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}
        component="form"
        onSubmit={handleSubmit}
           noValidate>
          <Typography id="modal-modal-title" component="h6">
            Tem certeza que deseja deletar esta transação ?
          </Typography>
          <input 
          type="hidden" 
          name="operacao" 
          value={operacao} 
          onChange={(e) => setOperacao(e.target.value)}
          />
          <Button type='submit'  variant="contained" color="success">
            Sim
          </Button>
        </Box>
      </Modal>
    </div>
  );
}
