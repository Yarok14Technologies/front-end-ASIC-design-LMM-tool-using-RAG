// src/App.jsx
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css'; // Assuming this contains your main layout styles

// Import the page components
import Home from './pages/Home.jsx';
import Upload from './pages/Upload.jsx';
import Generate from './pages/Generate.jsx';
import Outputs from './pages/Outputs.jsx';

function App() {
  return (
    <div className="app-container">
      {/* 1. Global Navigation Bar */}
      <nav className="nav-bar">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/upload">Upload</Link></li>
          <li><Link to="/generate">Generate (Verification/IP/VIP)</Link></li>
          <li><Link to="/outputs">Outputs (Waveforms/Logs)</Link></li>
        </ul>
      </nav>

      {/* 2. Routing Logic */}
      <main className="main-content">
        <Routes>
          {/* Matches the root path and renders the Home component */}
          <Route path="/" element={<Home />} />
          
          {/* Matches the /upload path */}
          <Route path="/upload" element={<Upload />} />
          
          {/* Matches the /generate path (Verification/IP/VIP generation) */}
          <Route path="/generate" element={<Generate />} />
          
          {/* Matches the /outputs path (Waveforms, Logs, Reports) */}
          <Route path="/outputs" element={<Outputs />} />
          
          {/* 404 Catch-all Route */}
          <Route path="*" element={<h2>404 - Page Not Found</h2>} />
        </Routes>
      </main>
    </div>
  );
}

export default App;