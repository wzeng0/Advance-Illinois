import React, { useState } from 'react';
import FileUpload from './FileUpload';
import { Checkbox, FormGroup, FormControlLabel, Button, CircularProgress } from '@mui/material';
import './App.css';

// Import the Web Worker
// eslint-disable-next-line import/no-webpack-loader-syntax
import Worker from 'worker-loader!./fileProcessor.worker';

const App = () => {
  const [columnNames, setColumnNames] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);
  const [uploadInProgress, setUploadInProgress] = useState(false);

  // Create an instance of the Web Worker
  const fileProcessorWorker = new Worker();

  // Listen for messages from the Web Worker
  fileProcessorWorker.addEventListener('message', (event) => {
    const columnNames = event.data;
    setColumnNames(columnNames);
    setUploadInProgress(false);
  });

  const handleFileUpload = (file) => {
    setUploadInProgress(true);

    // Send the file to the Web Worker for processing
    fileProcessorWorker.postMessage(file);
  };

  const handleCheckboxChange = (event) => {
    if (event.target.checked) {
      setSelectedItems([...selectedItems, event.target.name]);
    } else {
      setSelectedItems(selectedItems.filter((item) => item !== event.target.name));
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Selected Items:', selectedItems);
  };

  return (
    <div>
      <h1>Advance Illinois</h1>
      <p>Upload the LegSheets Excel workbook to convert the "House" sheet into json. The column names will be listed below after a few seconds.</p>
      <FileUpload onFileUpload={handleFileUpload} />

      {uploadInProgress && <CircularProgress/>}

      <form onSubmit={handleSubmit}>
        <FormGroup>
          {columnNames.map((columnName, index) => (
            <FormControlLabel
              key={index}
              control={
                <Checkbox
                  name={columnName}
                  onChange={handleCheckboxChange}
                />
              }
              label={columnName}
            />
          ))}
        </FormGroup>

        <Button type="submit" variant="contained">
          Submit
        </Button>
      </form>
      
    </div>
  );
};

export default App;
