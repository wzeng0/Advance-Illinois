import React, { useState } from 'react';
import FileUpload from './FileUpload';
import { Checkbox, FormGroup, FormControlLabel, Button, CircularProgress } from '@mui/material';
import axios from 'axios';
import './App.css';

const App = () => {
  const [columnNames, setColumnNames] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);
  const [uploadInProgress, setUploadInProgress] = useState(false);

  const handleFileUpload = async (file) => {
    // File is received as an argument
    const formData = new FormData();
    formData.append('file', file);
    
    setUploadInProgress(true);

    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setColumnNames(response.data.columnNames);
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setUploadInProgress(false);
    }
  };

  const handleCheckboxChange = (event) => {
    if (event.target.checked) {
      // If checked, add the item to the selected items array
      setSelectedItems([...selectedItems, event.target.name]);
    } else {
      // Otherwise, remove the item from the array
      setSelectedItems(selectedItems.filter((item) => item !== event.target.name));
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('http://localhost:8000/selectedColumns', selectedItems);
    } catch (error) {
      console.error('Error submitting selected columns:', error);
    }
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

        {columnNames.length > 0 && (
          <Button type="submit" variant="contained">
            Submit
          </Button>
        )}
      </form>
    </div>
  );
};

export default App;
