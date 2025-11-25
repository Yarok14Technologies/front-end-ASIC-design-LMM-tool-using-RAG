// src/pages/Generate.jsx
import React from 'react';
import RequirementsForm from '../components/RequirementsForm.jsx';
import CodeViewer from '../components/CodeViewer.jsx';

function Generate() {
  return (
    <div>
      <h1>Verification/IP Generation</h1>
      <RequirementsForm />
      <CodeViewer />
      {/* Placeholder for the generate button and status */}
    </div>
  );
}

export default Generate;