import React, { useState } from 'react';
import axios from 'axios';
import { CircularProgress, Typography } from '@mui/material';
import { Check, Warning } from '@mui/icons-material';

const FileUpload = ({ onUploadSuccess, onFileUpload, sessionUuid, endpoint }) => {
  const [uploadInProgress, setUploadInProgress] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [uploadFailure, setUploadFailure] = useState(false);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('sessionUuid', sessionUuid)
    
    setUploadInProgress(true);

    try {
      const response = await axios.post('http://localhost:8000/' + endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });

      onFileUpload(response.data); // Pass the response data back up to the parent
      if (response.data.status === 'success') {
        setUploadSuccess(true);
        onUploadSuccess(true); // Notify the parent of upload success
        setUploadFailure(false);
      } else {
        console.error('Error uploading file:', response.data);
        onUploadSuccess(false); // Notify the parent of upload failure
        setUploadFailure(true);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      onUploadSuccess(false); // Notify the parent of upload failure
      setUploadFailure(true);
    } finally {
      setUploadInProgress(false);
    }
  };

  return (
    <div>
      {!uploadSuccess && <input type="file" accept=".xls,.xlsx" onChange={handleFileChange} />}
      {uploadInProgress && <CircularProgress />}
      {uploadSuccess && (
        <>
          <Check/>
          <Typography variant="subtitle1">Upload successful!</Typography>
        </>
      )}
      {uploadFailure && <Warning />}
    </div>
  );
};

export default FileUpload;
