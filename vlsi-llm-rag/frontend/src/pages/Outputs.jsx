import React from 'react'
import { Download, Share2 } from 'lucide-react'

const Outputs = () => {
  // This would typically load from state/context/API
  const generatedOutputs = JSON.parse(localStorage.getItem('generationResult') || '{}')

  const downloadFile = (content, filename, contentType = 'text/plain') => {
    const blob = new Blob([content], { type: contentType })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  if (!generatedOutputs.code) {
    return (
      <div className="card">
        <h2>No Generated Outputs</h2>
        <p>Generate some RTL code first to see the outputs here.</p>
        <button 
          className="btn" 
          onClick={() => window.location.href = '/generate'}
        >
          Go to Generate
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <h2>Generated Outputs</h2>
        <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>
          Download your generated RTL files and documentation.
        </p>

        <div className="grid grid-2">
          <div className="card">
            <h3>RTL Files</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <button 
                className="btn"
                onClick={() => downloadFile(
                  generatedOutputs.code, 
                  `${generatedOutputs.module_name}.v`,
                  'text/plain'
                )}
              >
                <Download size={16} style={{ marginRight: '0.5rem' }} />
                Download Verilog
              </button>
              
              {generatedOutputs.testbench_code && (
                <button 
                  className="btn btn-secondary"
                  onClick={() => downloadFile(
                    generatedOutputs.testbench_code, 
                    `tb_${generatedOutputs.module_name}.sv`,
                    'text/plain'
                  )}
                >
                  <Download size={16} style={{ marginRight: '0.5rem' }} />
                  Download Testbench
                </button>
              )}
            </div>
          </div>

          <div className="card">
            <h3>Documentation</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <button className="btn btn-secondary">
                <Share2 size={16} style={{ marginRight: '0.5rem' }} />
                Generate Report
              </button>
              <button className="btn btn-secondary">
                <Download size={16} style={{ marginRight: '0.5rem' }} />
                Design Documentation
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3>Project Summary</h3>
        <div className="grid grid-2">
          <div>
            <h4>Design Information</h4>
            <ul style={{ color: '#cbd5e1' }}>
              <li><strong>Module:</strong> {generatedOutputs.module_name}</li>
              <li><strong>Generated:</strong> {new Date().toLocaleDateString()}</li>
              <li><strong>Status:</strong> Generated</li>
            </ul>
          </div>
          
          <div>
            <h4>Next Steps</h4>
            <ul style={{ color: '#cbd5e1' }}>
              <li>Run simulation with testbench</li>
              <li>Perform synthesis for PPA analysis</li>
              <li>Verify timing constraints</li>
              <li>Run formal verification</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Outputs
