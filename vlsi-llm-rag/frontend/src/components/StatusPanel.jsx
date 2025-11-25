// src/components/CodeViewer.jsx
import React from 'react';

// Default code content if none is provided
const DEFAULT_CODE = `
// Example Generated SystemVerilog Code

import uvm_pkg::*;
\`include "uvm_macros.svh"

class my_agent extends uvm_agent;
  // Agent implementation...
endclass
`;

function CodeViewer({ code = DEFAULT_CODE, language = 'systemverilog', title = 'Generated Code / Output Log' }) {
  // In a real app, you'd use a library like 'react-syntax-highlighter' 
  // for proper code formatting and coloring.

  return (
    <div className="code-viewer-container">
      <h4>{title}</h4>
      <pre className={`code-block language-${language}`}>
        {/* Simple plaintext rendering */}
        <code>
          {code}
        </code>
      </pre>
      {/* Action buttons */}
      <div className="code-actions">
        <button onClick={() => navigator.clipboard.writeText(code)}>Copy Code</button>
        <button>Download File</button>
      </div>
    </div>
  );
}

export default CodeViewer;
