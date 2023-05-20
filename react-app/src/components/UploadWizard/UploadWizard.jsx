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
import axios from "axios";

const steps = ["Upload Sheets", "Select Columns", "Download"];
const columnNames = [
  "SCHOOL DISTRICT",
  "ENROLLMENT",
  "% OF FULL FUNDING",
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
          uuid: sessionUuid,
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

  return (
    <div>
      <Stepper activeStep={activeStep}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
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
        <Typography variant="h5" align="center">
          Thank you!
        </Typography>
      )}
    </div>
  );
};

export default UploadWizard;
