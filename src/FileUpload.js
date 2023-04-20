import React from 'react';

const FileUpload = ({ onFileUpload }) => {
  // Function to handle the file input change event
  const handleFileChange = (event) => {
    // Get the first file from the input
    const file = event.target.files[0];
    // Call the parent component's file upload handler with the selected file
    onFileUpload(file);
  };

  return (
    <div>
      <input type="file" accept=".xls,.xlsx" onChange={handleFileChange} />
    </div>
  );
};

export default FileUpload;
