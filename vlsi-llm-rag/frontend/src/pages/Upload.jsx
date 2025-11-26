// src/pages/Upload.jsx
import React, { useState } from 'react';
import FileUpload from '../components/FileUpload.jsx';

function Upload() {
  const [topModule, setTopModule] = useState('');
  const [numSubModules, setNumSubModules] = useState(1);
  const [subModuleNames, setSubModuleNames] = useState(['']);
  const [uploads, setUploads] = useState({});
  const [submitStatus, setSubmitStatus] = useState('');

  const handleSubModuleNameChange = (idx, value) => {
    setSubModuleNames((prev) => {
      const newNames = [...prev];
      newNames[idx] = value;
      return newNames;
    });
  };

  const handleUpload = (module, category, files) => {
    setUploads((prev) => ({
      ...prev,
      [module]: { ...(prev[module] || {}), [category]: files },
    }));
  };

  const handleSubmit = async () => {
    if (!topModule.trim()) { 
      alert('Enter top module name'); 
      return; 
    }
    if (subModuleNames.some(name => !name.trim())) { 
      alert('Enter all sub-module names'); 
      return; 
    }

    setSubmitStatus('Submitting...');
    try {
      await new Promise((r) => setTimeout(r, 1500));
      console.log('Top Module:', topModule);
      console.log('Uploads:', uploads);
      setSubmitStatus('Submitted successfully!');
    } catch (err) {
      setSubmitStatus(`Submission failed: ${err.message}`);
    }
  };

  // Adjust sub-module names array if number changes
  const handleNumSubModulesChange = (e) => {
    const count = Math.max(1, parseInt(e.target.value) || 1);
    setNumSubModules(count);
    setSubModuleNames(prev => {
      const newArr = [...prev];
      while (newArr.length < count) newArr.push('');
      while (newArr.length > count) newArr.pop();
      return newArr;
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Upload Design Files</h1>

      {/* Top Module */}
      <div>
        <label>Top Module Name: </label>
        <input 
          type="text" 
          value={topModule} 
          onChange={(e) => setTopModule(e.target.value)} 
          placeholder="Top module name" 
          style={{ marginLeft: '10px' }} 
        />
      </div>

      {/* Top Module Uploads */}
      <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px', borderRadius: '5px' }}>
        <h3>Top Module Uploads</h3>
        <FileUpload label="Specification Documents" onUpload={(files) => handleUpload(topModule, 'spec', files)} />
        <FileUpload label="Testbench Requirements" onUpload={(files) => handleUpload(topModule, 'tbRequirements', files)} />
        <FileUpload label="Functional Design" onUpload={(files) => handleUpload(topModule, 'functionalDesign', files)} />
        <FileUpload label="Architecture Design" onUpload={(files) => handleUpload(topModule, 'architectureDesign', files)} />
        <FileUpload label="Protocol Working" onUpload={(files) => handleUpload(topModule, 'protocol', files)} />
        {/* New UVM/FV/SVA uploads */}
        <FileUpload label="UVM Testbench Files" onUpload={(files) => handleUpload(topModule, 'uvm', files)} />
        <FileUpload label="Formal Verification (FV) Files" onUpload={(files) => handleUpload(topModule, 'fv', files)} />
        <FileUpload label="SVA/Assertion Files" onUpload={(files) => handleUpload(topModule, 'sva', files)} />
      </div>

      {/* Sub-Modules */}
      <div style={{ marginTop: '20px' }}>
        <h3>Sub-Modules</h3>
        <label>Number of Sub-Modules: </label>
        <input 
          type="number" 
          value={numSubModules} 
          min={1} 
          onChange={handleNumSubModulesChange} 
          style={{ width: '60px', marginLeft: '10px' }} 
        />

        {subModuleNames.map((name, idx) => (
          <div key={idx} style={{ marginTop: '15px', padding: '10px', border: '1px solid #aaa', borderRadius: '5px' }}>
            <input 
              type="text" 
              placeholder="Sub-module name" 
              value={name} 
              onChange={(e) => handleSubModuleNameChange(idx, e.target.value)} 
              style={{ marginBottom: '10px' }} 
            />
            <FileUpload 
              label="Other Module Communication Files and Connection Details" 
              onUpload={(files) => handleUpload(name, 'communication', files)} 
            />
          </div>
        ))}
      </div>

      {/* Submit Button */}
      <div style={{ marginTop: '20px' }}>
        <button 
          onClick={handleSubmit} 
          style={{ padding: '10px 20px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '5px' }}
        >
          Submit All
        </button>
        {submitStatus && <p>{submitStatus}</p>}
      </div>

      {/* Summary */}
      <div style={{ marginTop: '20px' }}>
        <h3>Uploads Summary</h3>
        <pre>{JSON.stringify({ topModule, uploads }, null, 2)}</pre>
      </div>
    </div>
  );
}

export default Upload;
