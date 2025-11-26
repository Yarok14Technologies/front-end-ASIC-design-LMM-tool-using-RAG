// src/pages/Upload.jsx
import React, { useState } from 'react';
import FileUpload from '../components/FileUpload.jsx';
import { useNavigate } from "react-router-dom";

function Upload() {
  const navigate = useNavigate();

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

    const uploadPackage = {
      topModule,
      subModules: subModuleNames,
      uploads,
    };

    localStorage.setItem("uploadData", JSON.stringify(uploadPackage));

    setSubmitStatus("Submitted successfully! Redirecting...");
    setTimeout(() => {
      navigate("/codeview");
    }, 1000);
  };

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

      <div>
        <label>Top Module Name: </label>
        <input
          type="text"
          value={topModule}
          onChange={(e) => setTopModule(e.target.value)}
          placeholder="Top module name"
        />
      </div>

      <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
        <h3>Top Module Uploads</h3>
        <FileUpload label="Specification" onUpload={(files) => handleUpload(topModule, 'spec', files)} />
        <FileUpload label="Testbench Requirements" onUpload={(files) => handleUpload(topModule, 'tb', files)} />
        <FileUpload label="Functional Design" onUpload={(files) => handleUpload(topModule, 'func', files)} />
        <FileUpload label="Architecture Design" onUpload={(files) => handleUpload(topModule, 'arch', files)} />
        <FileUpload label="Protocol Working" onUpload={(files) => handleUpload(topModule, 'protocol', files)} />
        <FileUpload label="UVM Files" onUpload={(files) => handleUpload(topModule, 'uvm', files)} />
        <FileUpload label="Formal Verification" onUpload={(files) => handleUpload(topModule, 'fv', files)} />
        <FileUpload label="SVA / Assertions" onUpload={(files) => handleUpload(topModule, 'sva', files)} />
      </div>

      <h3 style={{ marginTop: '20px' }}>Sub-Modules</h3>
      <label>Number of Sub-Modules: </label>
      <input
        type="number"
        value={numSubModules}
        min={1}
        onChange={handleNumSubModulesChange}
        style={{ width: '60px', marginLeft: '10px' }}
      />

      {subModuleNames.map((name, idx) => (
        <div key={idx} style={{ marginTop: '15px', border: '1px solid #888', padding: '10px' }}>
          <input
            type="text"
            placeholder="Sub-module name"
            value={name}
            onChange={(e) => handleSubModuleNameChange(idx, e.target.value)}
          />
          <FileUpload
            label="Communication / Interface Docs"
            onUpload={(files) => handleUpload(name, 'communication', files)}
          />
        </div>
      ))}

      <button onClick={handleSubmit} style={{ marginTop: '20px', padding: '10px 20px', backgroundColor: 'green', color: 'white' }}>
        Submit & View →
      </button>

      {submitStatus && <p>{submitStatus}</p>}
    </div>
  );
}

export default Upload;
