// src/pages/Outputs.jsx
import React from 'react';
import StatusPanel from '../components/StatusPanel.jsx';
import CodeViewer from '../components/CodeViewer.jsx';

function Outputs() {
  return (
    <div>
      <h1>Simulation Results and Outputs</h1>
      <StatusPanel />
      <CodeViewer title="Simulation Log" />
      {/* Placeholder for displaying waveforms and reports */}
    </div>
  );
}

export default Outputs;