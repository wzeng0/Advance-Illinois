// theme.js
import { styled } from "@mui/material/styles";
import { Paper } from "@mui/material";

export const AppContainer = styled("div")({
  backgroundColor: "#282828",
  height: "100vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
});

export const UploadWizardForm = styled(Paper)(() => ({
  backgroundColor: "#404040",
  color: "white",
  width: "50%",
  height: "75%",
  padding: "20px",
  justifyContent: "center",
  alignItems: "center",
}));
