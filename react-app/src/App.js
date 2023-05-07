import React, { useState } from 'react';
import * as XLSX from 'xlsx'; // Import the xlsx library for parsing Excel files
import FileUpload from './FileUpload';
import { Checkbox, FormGroup, FormControlLabel, Button } from '@mui/material';

const App = () => {
  // Set up state to store the column names
  const [columnNames, setColumnNames] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);

  // Function to handle file uploads from the FileUpload component
  const handleFileUpload = (file) => {
    const reader = new FileReader();

    reader.onload = (event) => {
      // Get the binary string representation of the file's contents
      // and parse it into an XLSX workbook object
      const binaryString = event.target.result;
      const workBook = XLSX.read(binaryString, { type: 'binary' });

      // Retrieve the required sheet from the workbook
      const sheetName = "House"
      const sheet = workBook.Sheets[sheetName];

      // Convert the sheet data into an array of JSON objects and get the first row as column names
      const columnNames = XLSX.utils.sheet_to_json(sheet, { header: 1 })[0];
      //const csvData = XLSX.utils.sheet_to_csv(sheet);


      // Update state with the extracted column names
      setColumnNames(columnNames);
    };

    reader.readAsBinaryString(file);
  };

  // Function to handle checkbox changes
  const handleCheckboxChange = (event) => {
    if (event.target.checked) {
      setSelectedItems([...selectedItems, event.target.name]);
    } else {
      setSelectedItems(selectedItems.filter((item) => item !== event.target.name));
    }
  };

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Selected Items:', selectedItems);
  };

  return (
    <div>
      <h1>Excel Column Name Demo</h1>
      <p>Upload the LegSheets Excel workbook to convert the "House" sheet into json. The column names will be listed below after a few seconds.</p>
      {/* Pass the handleFileUpload function as a prop */}
      <FileUpload onFileUpload={handleFileUpload} />

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
