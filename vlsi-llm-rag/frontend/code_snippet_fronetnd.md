# frontend code file snippet  

```bash
// package.json
{
  "name": "vlsi-llm-rag-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.1"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.6.0",
    "vite": "^5.1.0"
  }
}

---
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  }
})

---
// index.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>VLSI LLM RAG</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>

---
// tailwind.config.cjs
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

---
// postcss.config.cjs
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}

---
// src/index.css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --accent: #0ea5e9;
}

body {
  @apply bg-slate-50 text-slate-800;
}

---
// src/main.jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)

---
// src/config.js
export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

---
// src/App.jsx
import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Generate from './pages/Generate'
import Outputs from './pages/Outputs'

export default function App(){
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="font-bold text-xl text-slate-700">VLSI LLM RAG</Link>
          <div className="space-x-4">
            <Link to="/upload" className="text-slate-600 hover:text-slate-900">Upload</Link>
            <Link to="/generate" className="text-slate-600 hover:text-slate-900">Generate</Link>
            <Link to="/outputs" className="text-slate-600 hover:text-slate-900">Outputs</Link>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/upload" element={<Upload/>} />
          <Route path="/generate" element={<Generate/>} />
          <Route path="/outputs" element={<Outputs/>} />
        </Routes>
      </main>
    </div>
  )
}

---
// src/App.css
/* small helpers if needed */

.code-block {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace;
  font-size: 0.9rem;
}

---
// src/components/FileUpload.jsx
import React, { useState } from 'react'
import axios from 'axios'
import { API_BASE } from '../config'

export default function FileUpload({ onUploaded }){
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const handleChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if(!file) return
    const fd = new FormData()
    fd.append('file', file)
    try{
      setUploading(true)
      const res = await axios.post(`${API_BASE}/upload`, fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (p) => setProgress(Math.round((p.loaded / p.total) * 100))
      })
      onUploaded && onUploaded(res.data)
    }catch(err){
      console.error(err)
      alert('Upload failed')
    }finally{
      setUploading(false)
      setProgress(0)
    }
  }

  return (
    <div className="bg-white p-4 rounded shadow">
      <label className="block text-sm font-medium text-slate-700">Specification / Design File</label>
      <input className="mt-2" type="file" accept=".txt,.md,.json,.sv,.v,.zip" onChange={handleChange} />
      <div className="mt-4 flex items-center gap-2">
        <button onClick={handleUpload} className="px-4 py-2 bg-sky-500 text-white rounded hover:bg-sky-600" disabled={uploading}>
          {uploading ? `Uploading ${progress}%` : 'Upload'}
        </button>
        {file && <span className="text-sm text-slate-500">{file.name}</span>}
      </div>
    </div>
  )
}

---
// src/components/CodeViewer.jsx
import React from 'react'

export default function CodeViewer({ code, language='verilog' }){
  return (
    <div className="bg-white rounded shadow p-4 overflow-auto code-block">
      <pre className="whitespace-pre-wrap"><code>{code || '// no output yet'}</code></pre>
    </div>
  )
}

---
// src/components/StatusPanel.jsx
import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { API_BASE } from '../config'

export default function StatusPanel({ taskId }){
  const [status, setStatus] = useState(null)
  const [progress, setProgress] = useState(0)
  const [logs, setLogs] = useState('')

  useEffect(() => {
    if(!taskId) return
    let mounted = true
    const interval = setInterval(async () => {
      try{
        const res = await axios.get(`${API_BASE}/status/${taskId}`)
        if(!mounted) return
        setStatus(res.data.status)
        setProgress(res.data.progress || 0)
      }catch(e){
        console.error(e)
      }
    }, 1500)

    const logInterval = setInterval(async () => {
      try{
        const r = await axios.get(`${API_BASE}/logs/${taskId}`)
        if(!mounted) return
        setLogs(r.data.logs)
      }catch(e){}
    }, 2000)

    return () => { mounted = false; clearInterval(interval); clearInterval(logInterval) }
  }, [taskId])

  return (
    <div className="bg-white rounded shadow p-4">
      <h4 className="font-medium">Task Status</h4>
      <p className="text-sm text-slate-600">Task ID: <span className="font-mono">{taskId}</span></p>
      <div className="mt-2">
        <div className="w-full bg-slate-100 rounded h-3 overflow-hidden">
          <div className="h-full bg-sky-500" style={{ width: `${progress}%` }} />
        </div>
        <p className="mt-2 text-sm">Status: <strong>{status || 'idle'}</strong></p>
      </div>

      <details className="mt-4">
        <summary className="cursor-pointer text-sm text-slate-600">Logs</summary>
        <pre className="mt-2 max-h-48 overflow-auto bg-slate-50 p-2 rounded text-xs font-mono">{logs || 'No logs yet'}</pre>
      </details>
    </div>
  )
}

---
// src/components/RequirementsForm.jsx
import React, { useState } from 'react'

export default function RequirementsForm({ onChange }){
  const [form, setForm] = useState({ clock: '100MHz', pipeline: 1, reset: 'sync', target: 'area' })

  const handle = (k, v) => {
    const n = { ...form, [k]: v }
    setForm(n)
    onChange && onChange(n)
  }

  return (
    <div className="bg-white p-4 rounded shadow">
      <h4 className="font-medium">Design Requirements</h4>
      <div className="grid grid-cols-2 gap-3 mt-3">
        <label className="text-sm">Clock</label>
        <input className="p-2 border rounded" value={form.clock} onChange={(e) => handle('clock', e.target.value)} />

        <label className="text-sm">Pipeline Stages</label>
        <input type="number" min={0} className="p-2 border rounded" value={form.pipeline} onChange={(e) => handle('pipeline', Number(e.target.value))} />

        <label className="text-sm">Reset Type</label>
        <select className="p-2 border rounded" value={form.reset} onChange={(e) => handle('reset', e.target.value)}>
          <option value="sync">Synchronous</option>
          <option value="async">Asynchronous</option>
        </select>

        <label className="text-sm">Optimization Target</label>
        <select className="p-2 border rounded" value={form.target} onChange={(e) => handle('target', e.target.value)}>
          <option value="area">Area</option>
          <option value="power">Power</option>
          <option value="performance">Performance</option>
        </select>
      </div>
    </div>
  )
}

---
// src/pages/Home.jsx
import React from 'react'
import { Link } from 'react-router-dom'

export default function Home(){
  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold">Automated Front-End VLSI Design (LLM + RAG)</h1>
        <p className="mt-2 text-slate-600">Upload specs, run the RAG pipeline, generate RTL, and iterate with verification-in-the-loop.</p>
        <div className="mt-4 flex gap-3">
          <Link to="/upload" className="px-4 py-2 bg-sky-500 text-white rounded">Upload Spec</Link>
          <Link to="/generate" className="px-4 py-2 border rounded">Generate RTL</Link>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">Quick demo: Upload spec, choose constraints, and run generate.</div>
        <div className="bg-white p-4 rounded shadow">Supports Verilog/VHDL, UVM testbenches, and PPA optimization targets.</div>
        <div className="bg-white p-4 rounded shadow">Outputs: RTL, Testbench, Waveforms, Coverage Reports.</div>
      </div>
    </div>
  )
}

---
// src/pages/Upload.jsx
import React, { useState } from 'react'
import FileUpload from '../components/FileUpload'
import RequirementsForm from '../components/RequirementsForm'

export default function Upload(){
  const [uploaded, setUploaded] = useState(null)
  const [requirements, setRequirements] = useState(null)

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <FileUpload onUploaded={(d) => setUploaded(d)} />
        <RequirementsForm onChange={(r) => setRequirements(r)} />
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h4 className="font-medium">Upload Summary</h4>
        <p className="text-sm mt-2">File: {uploaded?.filename || 'Not uploaded'}</p>
        <pre className="mt-2 text-xs font-mono bg-slate-50 p-2 rounded">{JSON.stringify(requirements, null, 2)}</pre>
      </div>
    </div>
  )
}

---
// src/pages/Generate.jsx
import React, { useState } from 'react'
import axios from 'axios'
import { API_BASE } from '../config'
import StatusPanel from '../components/StatusPanel'

export default function Generate(){
  const [taskId, setTaskId] = useState(null)
  const [prompt, setPrompt] = useState('')

  const startGenerate = async () => {
    try{
      const res = await axios.post(`${API_BASE}/generate`, { prompt })
      setTaskId(res.data.task_id)
    }catch(e){
      console.error(e)
      alert('Failed to start generation')
    }
  }

  return (
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-white p-4 rounded shadow">
        <h4 className="font-medium">Run Generation</h4>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={10} className="w-full mt-2 p-2 border rounded" placeholder="Describe the RTL you want (eg. 32-bit ALU with flags, AXI4-Lite slave)..." />
        <div className="mt-3 flex gap-2">
          <button onClick={startGenerate} className="px-4 py-2 bg-sky-500 text-white rounded">Start</button>
          <button onClick={() => setPrompt('')} className="px-4 py-2 border rounded">Clear</button>
        </div>
      </div>

      <div>
        {taskId ? <StatusPanel taskId={taskId} /> : (
          <div className="bg-white p-4 rounded shadow">No active task. Start a generation to see status.</div>
        )}
      </div>
    </div>
  )
}

---
// src/pages/Outputs.jsx
import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { API_BASE } from '../config'
import CodeViewer from '../components/CodeViewer'

export default function Outputs(){
  const [taskId, setTaskId] = useState('')
  const [output, setOutput] = useState('')

  const fetchOutput = async () => {
    if(!taskId) return alert('Enter a task id')
    try{
      const res = await axios.get(`${API_BASE}/result/${taskId}`)
      setOutput(res.data.output)
    }catch(e){
      console.error(e)
      alert('Failed to fetch output')
    }
  }

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded shadow grid grid-cols-3 gap-2 items-center">
        <input className="col-span-2 p-2 border rounded" placeholder="Enter task id" value={taskId} onChange={(e) => setTaskId(e.target.value)} />
        <button className="px-4 py-2 bg-sky-500 text-white rounded" onClick={fetchOutput}>Fetch</button>
      </div>

      <CodeViewer code={output} />

      {output && (
        <div className="mt-2">
          <a className="px-4 py-2 bg-slate-800 text-white rounded" href={`${API_BASE}/download/${taskId}`} target="_blank" rel="noreferrer">Download Package</a>
        </div>
      )}
    </div>
  )
}

```
