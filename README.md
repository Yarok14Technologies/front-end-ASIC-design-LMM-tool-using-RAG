# front-end-ASIC-design-Local-Device-LMM-tool-using-RAG
Automated Front-End VLSI Design tool. Uses an LLM-RAG pipeline to transform high-level design specifications into PPA-optimized, synthesizable RTL IP blocks (Verilog/VHDL). Features an iterative verification loop for bug correction and quality assurance.
# 🤖 Automated Front-End VLSI Design AI Tool using LLM RAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository hosts a cutting-edge, end-to-end AI tool that automates the front-end VLSI (Very Large-Scale Integration) design flow. It utilizes a **Retrieval-Augmented Generation (RAG) pipeline** powered by a Large Language Model (LLM) to convert high-level functional specifications into **synthesizable, PPA-optimized Register-Transfer Level (RTL) IP blocks** with a closed-loop verification process.

## ✨ Key Features

* **Spec-to-RTL Generation:** Automatically translates natural language specifications (architecture, functional requirements, protocols) into Verilog/VHDL code, including complex Finite State Machines (FSMs) and Testbenches (TB).
* **PPA Optimization:** The LLM is conditioned to generate RTL focused on achieving the best balance of **Power, Performance, and Area (PPA)** efficiency.
* **Verification-in-the-Loop:** Simulation results (waveforms, coverage logs) are fed back to the LLM to **iteratively correct and refine** the generated RTL until it fully matches the specification.
* **Contextual Accuracy (RAG):** The **RAG engine** grounds the generation by retrieving relevant information from a dedicated **Knowledge Base** (RTL libraries, protocols, reference guides), significantly reducing LLM "hallucinations."
* **Web Interface:** A user-friendly React frontend for file upload, parameter configuration, execution, and output visualization.

***

## 💡 VLSI Design Flow (RAG Pipeline)

The system operates in a continuous, iterative loop to ensure functional correctness and quality standards. 

| Step | Component | Description |
| :--- | :--- | :--- |
| **1. Input & Parsing** | **NLP Parser** (`file_parser.py`) | Upload specification documents and use NLP to extract structured constraints. |
| **2. Retrieval** | **RAG Engine** (`rag_service.py`) | Query the **Knowledge DB** (`vector_db/`) to retrieve relevant golden RTL and reference protocols. |
| **3. Generation** | **LLM Spec-to-RTL** (`rtl_generator.py`) | LLM generates **RTL (Verilog/VHDL)** and **Testbench/VIP** focused on **PPA efficiency**. |
| **4. Verification** | **Post-Processing & Sim** | RTL is checked (Lint, Synthesis Check, STA, CDC) and simulated (UVM, FV). Generates **Waveforms** and **Coverage Logs**. |
| **5. Correction** | **Iterative Loop** | **Verification results are fed back** to the LLM for automated bug correction until spec match is achieved. |
| **6. Final Output** | **Synthesizable IP** | The stable, verified, and PPA-optimized **Synthesizable RTL IP block** is produced. |

***

Markdown

# 🤖 Automated Front-End VLSI Design AI Tool using LLM RAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository hosts a cutting-edge, end-to-end AI tool that automates the front-end VLSI (Very Large-Scale Integration) design flow. It utilizes a **Retrieval-Augmented Generation (RAG) pipeline** powered by a Large Language Model (LLM) to convert high-level functional specifications into **synthesizable, PPA-optimized Register-Transfer Level (RTL) IP blocks** with a closed-loop verification process.

## ✨ Key Features

* **Spec-to-RTL Generation:** Automatically translates natural language specifications (architecture, functional requirements, protocols) into Verilog/VHDL code, including complex Finite State Machines (FSMs) and Testbenches (TB).
* **PPA Optimization:** The LLM is conditioned to generate RTL focused on achieving the best balance of **Power, Performance, and Area (PPA)** efficiency.
* **Verification-in-the-Loop:** Simulation results (waveforms, coverage logs) are fed back to the LLM to **iteratively correct and refine** the generated RTL until it fully matches the specification.
* **Contextual Accuracy (RAG):** The **RAG engine** grounds the generation by retrieving relevant information from a dedicated **Knowledge Base** (RTL libraries, protocols, reference guides), significantly reducing LLM "hallucinations."
* **Web Interface:** A user-friendly React frontend for file upload, parameter configuration, execution, and output visualization.

***

## 💡 VLSI Design Flow (RAG Pipeline)

The system operates in a continuous, iterative loop to ensure functional correctness and quality standards. 

| Step | Component | Description |
| :--- | :--- | :--- |
| **1. Input & Parsing** | **NLP Parser** (`file_parser.py`) | Upload specification documents and use NLP to extract structured constraints. |
| **2. Retrieval** | **RAG Engine** (`rag_service.py`) | Query the **Knowledge DB** (`vector_db/`) to retrieve relevant golden RTL and reference protocols. |
| **3. Generation** | **LLM Spec-to-RTL** (`rtl_generator.py`) | LLM generates **RTL (Verilog/VHDL)** and **Testbench/VIP** focused on **PPA efficiency**. |
| **4. Verification** | **Post-Processing & Sim** | RTL is checked (Lint, Synthesis Check, STA, CDC) and simulated (UVM, FV). Generates **Waveforms** and **Coverage Logs**. |
| **5. Correction** | **Iterative Loop** | **Verification results are fed back** to the LLM for automated bug correction until spec match is achieved. |
| **6. Final Output** | **Synthesizable IP** | The stable, verified, and PPA-optimized **Synthesizable RTL IP block** is produced. |

***

## 📁 Repository Structure

The project is a full-stack application with a Python/FastAPI backend, a dedicated RAG knowledge base, and a React/Vite frontend.

front-end-ASIC-design-LMM-tool-using-RAG

```bash
vlsi-llm-rag/
├── README.md
├── requirements.txt
├── .env.example
├── docker-compose.yml
|
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── services/  (Core LLM/RAG/VLSI Logic)
│   │   │   ├── __init__.py
│   │   │   ├── rag_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── rtl_generator.py
│   │   │   ├── vip_generator.py
│   │   │   └── file_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_parser.py
│   │       └── prompts.py
|
├── knowledge_base/  (Retrieval-Augmented Data)
│   ├── specs/
│   ├── protocols/
│   └── vector_db/
|
├── frontend/ (React/Vite Application)
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── App.css
│       ├── components/ (Reusable UI)
│       │   ├── FileUpload.jsx
│       │   ├── CodeViewer.jsx
│       │   ├── StatusPanel.jsx
│       │   └── RequirementsForm.jsx
│       └── pages/ (Main Views)
│           ├── Home.jsx
│           ├── Upload.jsx
│           ├── Generate.jsx
│           └── Outputs.jsx
|
└── examples/
    ├── axi4_lite/
    │   ├── spec.txt
    │   └── requirements.md
    └── uart/
        ├── spec.txt
        └── requirements.md
```

***

## 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/OWNER/front-end-ASIC-design-Local-Device-LMM-tool-using-RAG.git](https://github.com/OWNER/front-end-ASIC-design-Local-Device-LMM-tool-using-RAG.git)
    cd front-end-ASIC-design-Local-Device-LMM-tool-using-RAG
    ```
2.  **Setup Environment Variables:**
    ```bash
    cp .env.example .env
    # Edit the .env file with your LLM API key (e.g., GEMINI_API_KEY=...)
    ```
3.  **Run with Docker (Recommended):**
    ```bash
    # Build and run the entire stack (backend, frontend, vector db)
    docker-compose up --build
    ```

The application will be accessible at `http://localhost:3000`.

![VLSI RAG Design Flow Diagram](https://github.com/Yarok14Technologies/front-end-ASIC-design-LMM-tool-using-RAG/blob/main/assets/Automated%20%20front%20end%20%20VLSI%20%20design%20AI%20tool%20using%20LLM%20RAG.png)

![VLSI RAG Design Flow Diagram](https://github.com/Yarok14Technologies/front-end-ASIC-design-LMM-tool-using-RAG/blob/main/assets/4%20pages%20model.png)

![VLSI RAG Design Flow Diagram](https://github.com/Yarok14Technologies/front-end-ASIC-design-LMM-tool-using-RAG/blob/main/assets/UI%20UX%20Home%20Page.png)

![VLSI RAG Design Flow Diagram](https://github.com/Yarok14Technologies/front-end-ASIC-design-LMM-tool-using-RAG/blob/main/assets/frontend%20structure%20repo%20structure.png)

## 📁 Repository Structure

The project is a full-stack application with a Python/FastAPI backend, a dedicated RAG knowledge base, and a React/Vite frontend.


## 💻 System Requirements

Running a full-stack RAG system with a local backend, frontend, and vector database requires sufficient local machine resources, primarily due to the performance demands of the Large Language Model (LLM) component and containerization overhead.

### 💾 Hardware Requirements

| Component | Minimum Requirement | Recommended Specification | Notes |
|-----------|------------------|--------------------------|-------|
| RAM (System Memory) | 8 GB | 16 GB or 32 GB | 16 GB is strongly recommended to comfortably run Docker, the vector database, and the Python backend concurrently. |
| CPU | Dual-Core Modern CPU | Quad-Core (4+ Cores) | Necessary for running multiple containers (FastAPI, Vector DB, Frontend) and handling computationally intensive tasks like vector chunking. |
| Storage (Disk Space) | 50 GB Free Space | 100 GB+ SSD | Required for Docker images, cached LLM models (if self-hosted), and the Knowledge Base (`vector_db/`) storage. An SSD is critical for fast vector search and retrieval performance. |
| GPU (Optional) | N/A | NVIDIA GPU (8GB+ VRAM) | Recommended if you plan to host the LLM locally (e.g., using Ollama/vLLM for models like Llama 3) for faster RTL generation times. |

### ⚙️ Software Prerequisites

The entire stack is designed to be launched using Docker Compose for a consistent, isolated environment.

| Component | Requirement | Notes |
|-----------|------------|-------|
| Containerization | Docker Engine (20.10+) | Required to build and run the entire application stack. |
| Orchestration | Docker Compose (v2.0+) | Used to manage the multiple service containers (Backend, Frontend, DB). |
| OS Support | Windows 10/11, macOS, or Linux | Must support Docker Desktop (ensure virtualization is enabled in BIOS). |
| Python | Python 3.8+ | Used for the backend/FastAPI application and RAG logic (primarily for development outside of Docker). |
| Node.js/npm | Node.js 16+ | Used for the frontend/React/Vite development server (primarily for development outside of Docker). |

