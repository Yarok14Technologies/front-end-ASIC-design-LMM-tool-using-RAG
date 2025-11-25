// src/components/RequirementsForm.jsx
import React, { useState } from 'react';

function RequirementsForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    designName: '',
    interfaceProtocol: 'AXI',
    verificationMethodology: 'UVM',
    clockFrequency: '100 MHz'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      // Pass the collected data up to the parent (Generate.jsx)
      onSubmit(formData);
    }
    console.log('Form Data Submitted:', formData);
    alert('Verification requirements submitted! Check the generated code.');
  };

  return (
    <form onSubmit={handleSubmit} className="requirements-form">
      <h3>Verification Environment Setup</h3>
      
      <label>
        Design Top Module Name:
        <input 
          type="text" 
          name="designName" 
          value={formData.designName} 
          onChange={handleChange} 
          required 
          placeholder="e.g., top_module"
        />
      </label>
      
      <label>
        Interface Protocol:
        <select name="interfaceProtocol" value={formData.interfaceProtocol} onChange={handleChange}>
          <option value="AXI">AXI</option>
          <option value="APB">APB</option>
          <option value="Wishbone">Wishbone</option>
          <option value="Custom">Custom/None</option>
        </select>
      </label>
      
      <label>
        Verification Methodology:
        <select name="verificationMethodology" value={formData.verificationMethodology} onChange={handleChange}>
          <option value="UVM">UVM (Universal Verification Methodology)</option>
          <option value="SV-TB">SystemVerilog Testbench</option>
          <option value="VHDL">VHDL Testbench</option>
        </select>
      </label>
      
      <button type="submit">Generate Environment Code</button>
    </form>
  );
}

export default RequirementsForm;