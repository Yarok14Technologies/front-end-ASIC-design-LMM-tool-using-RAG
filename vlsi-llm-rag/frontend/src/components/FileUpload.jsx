// src/components/FileUpload.jsx
import React, { useState } from 'react';

function FileUpload({ label = 'Select Files', multiple = true, onUpload, accept = '*' }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState('');

  // Handle file selection
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
    setUploadStatus('');
    if (onUpload) onUpload(files); // Immediately update parent with selected files
  };

  // Optional upload simulation
  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      alert('Please select files to upload.');
      return;
    }

    setUploadStatus('Uploading...');
    try {
      // Simulate async upload
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log('Files uploaded:', selectedFiles.map(f => f.name));
      setUploadStatus(`Uploaded ${selectedFiles.length} file(s) successfully.`);
      // Optional: clear selection after upload
      // setSelectedFiles([]);
      // if (onUpload) onUpload([]);
    } catch (err) {
      setUploadStatus(`Upload failed: ${err.message}`);
    }
  };

  return (
    <div style={{ marginBottom: '15px' }}>
      <label style={{ fontWeight: 'bold' }}>{label}</label>
      <input
        type="file"
        multiple={multiple}
        accept={accept}
        onChange={handleFileChange}
        style={{ display: 'block', margin: '5px 0' }}
      />

      {selectedFiles.length > 0 && (
        <div>
          <ul>
            {selectedFiles.map((file, index) => (
              <li key={index}>
                {file.name} ({Math.round(file.size / 1024)} KB)
              </li>
            ))}
          </ul>
          <button
            onClick={handleUpload}
            disabled={uploadStatus === 'Uploading...'}
            style={{
              padding: '6px 12px',
              backgroundColor: '#007BFF',
              color: 'white',
              border: 'none',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            {uploadStatus === 'Uploading...' ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}

      {uploadStatus && <p style={{ marginTop: '5px' }}>{uploadStatus}</p>}
    </div>
  );
}

export default FileUpload;
