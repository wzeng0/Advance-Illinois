import React, { useState } from "react";
import UploadWizard from "./components/UploadWizard/UploadWizard";
import { Button, Typography } from "@mui/material";
import axios from "axios";
import "./App.css";
import { UploadWizardForm, AppContainer } from "./styles";

const App = () => {
  const [started, setStarted] = useState(false);
  const [sessionUuid, setSessionUuid] = useState(null);

  const start = async () => {
    try {
      const response = await axios.get("http://localhost:8000/new_form");
      setSessionUuid(response.data.uuid);
      setStarted(true);
    } catch (error) {
      console.error("Error fetching UUID:", error);
    }
  };

  return (
    <AppContainer>
      <UploadWizardForm>
        <Typography
          variant="h1"
          sx={{ fontSize: "4rem", paddingTop: "15px", paddingBottom: "15px" }}
        >
          Advance Illinois
        </Typography>
        <Typography
          variant="body1"
          sx={{ textAlign: "center", marginBottom: "30px" }}
        >
          Please follow the steps below to generate PDFs for representatives.
        </Typography>
        {!started && (
          <Button variant="contained" onClick={start} sx={{width: '25%', height: '8%'}}>
            Start
          </Button>
        )}
        {started && (
          <UploadWizard
            sessionUuid={sessionUuid}
            sx={{ display: "flex", flexDirection: "column" }}
          />
        )}
      </UploadWizardForm>
    </AppContainer>
  );
};

export default App;
