import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Generate from './pages/Generate'
import Outputs from './pages/Outputs'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>🤖 VLSI Design AI Tool</h1>
          <nav>
            <a href="/">Home</a>
            <a href="/upload">Upload</a>
            <a href="/generate">Generate</a>
            <a href="/outputs">Outputs</a>
          </nav>
        </header>
        
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/generate" element={<Generate />} />
            <Route path="/outputs" element={<Outputs />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
