import React, { useState } from 'react';
import * as XLSX from 'xlsx'; // Import the xlsx library for parsing Excel files
import FileUpload from './FileUpload';

const App = () => {
  // Set up state to store the column names
  const [columnNames, setColumnNames] = useState([]);

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

      // Update state with the extracted column names
      setColumnNames(columnNames);
    };

    reader.readAsBinaryString(file);
  };

  return (
    <div>
      <h1>Excel Column Name Demo</h1>
      <p>Upload the LegSheets Excel workbook to convert the "House" sheet into json. The column names will be listed below after a few seconds.</p>
      {/* Pass the handleFileUpload function as a prop */}
      <FileUpload onFileUpload={handleFileUpload} />

      <ul>
        {columnNames.map((columnName, index) => (
          <li key={index}>{columnName}</li>
        ))}
      </ul>

    </div>
  );
};

export default App;
