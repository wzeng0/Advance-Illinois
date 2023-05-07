import React from 'react';

const FileUpload = ({ onFileUpload }) => {
  // When a change is made to the uploaded file, get the first file from the input
  // and call the parent component's file upload handler with the selected file
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    onFileUpload(file);
  };

  return (
    <div>
      <input type="file" accept=".xls,.xlsx" onChange={handleFileChange} />
    </div>
  );
};

export default FileUpload;
