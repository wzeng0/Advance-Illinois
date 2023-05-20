import React, { useState } from 'react';
import UploadWizard from './components/UploadWizard/UploadWizard';
import { Button } from '@mui/material';
import axios from 'axios';
import './App.css';

const App = () => {
  const [started, setStarted] = useState(false);
  const [sessionUuid, setSessionUuid] = useState(null);

  const start = async () => {
    try {
      const response = await axios.get('http://localhost:8000/new_form');
      setSessionUuid(response.data.uuid);
      setStarted(true);
    } catch (error) {
      console.error('Error fetching UUID:', error);
    }
  };

  return (
    <div>
      <h1>Advance Illinois</h1>
      <p>Upload the LegSheets Excel workbook to convert the "House" sheet into json. The column names will be listed below after a few seconds.</p>
      {!started && <Button variant="contained" onClick={start}>Start</Button>}
      {started && <UploadWizard sessionUuid={sessionUuid} />}
    </div>
  );
};

export default App;
