import React, { useState } from "react";
import FileUpload from "../FileUpload/FileUpload";
import {
  Checkbox,
  FormGroup,
  FormControlLabel,
  Button,
  Typography,
  Stepper,
  Step,
  StepLabel,
} from "@mui/material";
import { ColorlibConnector, ColorlibStepIcon } from "./styles";
import axios from "axios";
import { SaveAs } from "@mui/icons-material";

const steps = ["Upload Sheets", "Select Columns", "Download"];
const columnNames = [
  "ENROLLMENT",
  "TOTAL GAP TO FULL FUNDING",
  "PER PUPIL GAP TO FULL FUNDING",
];

const UploadWizard = ({ sessionUuid }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedItems, setSelectedItems] = useState([]);
  const [uploadSuccessLeg, setUploadSuccessLeg] = useState(false);
  const [uploadSuccessGa, setUploadSuccessGa] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleFileUpload = async (data, endpoint) => {
    if (endpoint === "upload_leg") {
      setUploadSuccessLeg(true);
    } else if (endpoint === "upload_ga") {
      setUploadSuccessGa(true);
    }
  };

  const handleCheckboxChange = (event) => {
    if (event.target.checked) {
      setSelectedItems([...selectedItems, event.target.name]);
    } else {
      setSelectedItems(
        selectedItems.filter((item) => item !== event.target.name)
      );
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post(
        "http://localhost:8000/process",
        {
          columns: selectedItems,
          sessionUuid: sessionUuid,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setActiveStep(2); // Move to step 3 after data processing
    } catch (error) {
      console.error("Error submitting user selection", error);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/download/${sessionUuid}`,
        { responseType: "blob" }
      );
      const blob = new Blob([response.data], { type: "application/zip" });
      console.log("blob received")
      SaveAs(blob, `${sessionUuid}.zip`);
      console.log("Download successful")
    } catch (error) {
      console.error("Error downloading file", error);
    }
  };

  return (
    <div>
      <Stepper activeStep={activeStep} connector={<ColorlibConnector />}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel
              StepIconComponent={ColorlibStepIcon}
              sx={{
                "& .MuiStepLabel-label": { color: "#fff" },
              }}
            >
              {label}
            </StepLabel>
          </Step>
        ))}
      </Stepper>

      {activeStep === 0 && (
        <>
          <h2>LegSheet</h2>
          <FileUpload
            onFileUpload={(data) => handleFileUpload(data, "upload_leg")}
            onUploadSuccess={setUploadSuccess}
            sessionUuid={sessionUuid}
            endpoint="upload_leg"
          />
          <h2>GA Sheet</h2>
          <FileUpload
            onFileUpload={(data) => handleFileUpload(data, "upload_ga")}
            onUploadSuccess={setUploadSuccess}
            sessionUuid={sessionUuid}
            endpoint="upload_ga"
          />
          <Button
            variant="contained"
            disabled={!uploadSuccessLeg || !uploadSuccessGa}
            onClick={() => setActiveStep(1)} // Move to step 2 after BOTH uploads
          >
            Next
          </Button>
        </>
      )}

      {activeStep === 1 && (
        <form onSubmit={handleSubmit}>
          <FormGroup>
            {columnNames.map((columnName, index) => (
              <FormControlLabel
                key={index}
                control={
                  <Checkbox name={columnName} onChange={handleCheckboxChange} />
                }
                label={columnName}
              />
            ))}
          </FormGroup>

          {columnNames.length > 0 && (
            <Button type="submit" variant="contained" disabled={!uploadSuccess}>
              Submit
            </Button>
          )}
        </form>
      )}

      {activeStep === 2 && (
        <>
          <Typography variant="h5" align="center" sx={{marginTop: "2rem", marginBottom: "2rem"}}>
            Thank you! Click below to begin your download.
          </Typography>
          <Button variant="contained" onClick={handleDownload} sx={{marginLeft: "auto", marginRight: "auto"}}>
            Download File
          </Button>
        </>
      )}
    </div>
  );
};

export default UploadWizard;
