// src/components/FileUpload.jsx
import React, { useState } from 'react';

function FileUpload() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    // Convert FileList object to an array for easy mapping
    setSelectedFiles(Array.from(event.target.files));
    setUploadStatus('');
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      alert('Please select files to upload.');
      return;
    }

    setUploadStatus('Uploading...');
    
    // **NOTE:** In a real application, you would use FormData 
    // and an API call (e.g., Axios or fetch) here.
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      console.log('Files submitted:', selectedFiles.map(f => f.name));
      setUploadStatus(`Successfully uploaded ${selectedFiles.length} files.`);
      // Optionally clear files: setSelectedFiles([]);
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
    }
  };

  return (
    <div className="file-upload-container">
      <h3>Select Design and Verification Files</h3>
      <input 
        type="file" 
        multiple 
        onChange={handleFileChange} 
        accept=".v,.sv,.vhd,.vhdl,.sva" // Common EDA file extensions
        style={{ marginBottom: '10px' }}
      />
      
      {selectedFiles.length > 0 && (
        <div style={{ margin: '15px 0' }}>
          <h4>Files Selected:</h4>
          <ul>
            {selectedFiles.map((file, index) => (
              <li key={index}>{file.name} ({Math.round(file.size / 1024)} KB)</li>
            ))}
          </ul>
          <button 
            onClick={handleUpload} 
            disabled={uploadStatus === 'Uploading...'}
          >
            {uploadStatus === 'Uploading...' ? 'Processing...' : 'Start Upload'}
          </button>
        </div>
      )}
      
      {uploadStatus && <p style={{ marginTop: '10px' }}>**Status:** {uploadStatus}</p>}
    </div>
  );
}

export default FileUpload;
