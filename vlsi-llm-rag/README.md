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
│   |       └── prompts.py
|   |
│   └── uploads/          # <--- New folder for storing uploaded files
│       ├── TopModuleName/
│       │   ├── spec/
│       │   ├── tb/
│       │   ├── func/
│       │   ├── arch/
│       │   ├── protocol/
│       │   ├── uvm/
│       │   ├── fv/
│       │   └── sva/
│       ├── SubModule1/
│       │   └── communication/
│       ├── SubModule2/
│       │   └── communication/
│       └── ...           # dynamically created per user upload
│  
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



Absolutely! Since your project is a **local front-end VLSI design automation tool using LLM + RAG**, there are several ways to improve the **effectiveness, accuracy, and efficiency** of your system. I’ll break them down by **RAG, LLM, data handling, and integration strategies**.

---

## 1️⃣ RAG (Retrieval-Augmented Generation) Improvements

1. **Knowledge Base Quality**

   * Ensure your KB (`knowledge_base/`) is **well-structured, comprehensive, and clean**.
   * Include **golden RTL examples, verified UVM testbenches, protocol references, PPA-optimized IPs**.
   * Keep document chunks **smaller and semantically coherent** (e.g., per FSM, per module, per protocol section).

2. **Embedding Optimization**

   * Use **domain-specific embeddings** for RTL/VLSI content (not general NLP embeddings).

     * Example: Train embeddings using code-focused models (CodeBERT, StarCoder embeddings) for Verilog/VHDL.
   * Normalize units, comments, and conventions in RTL before embedding to **reduce retrieval mismatches**.

3. **Vector DB Tuning**

   * Use **FAISS or Milvus** with approximate nearest neighbors for fast retrieval.
   * Fine-tune **distance metrics**: e.g., cosine similarity vs inner product for code vectors.
   * Maintain **updated embeddings** if new RTL/IP references are added.

4. **Context Window Management**

   * Include only **relevant top-K retrieved chunks** in each LLM query to reduce hallucinations.
   * For larger specs, summarize or prioritize chunks to stay within model input limits.

5. **Feedback Loop Integration**

   * After verification, **store failed/wrong patterns** in KB for future retrieval.
   * Maintain a **“negative examples” dataset** to guide LLM corrections.

---

## 2️⃣ LLM Improvements

1. **Domain-Specific Fine-Tuning**

   * Fine-tune the LLM on **RTL design examples, UVM testbenches, verification flows**.
   * Include **PPA-optimized code patterns** for better output suggestions.

2. **Prompt Engineering**

   * Use structured prompts with **instruction + context + spec + previous failures**.
   * Include explicit instructions for:

     * Module naming conventions.
     * Signal naming conventions.
     * PPA optimization strategies.
   * Example:

     ```text
     Generate synthesizable Verilog RTL with:
     - FSM design for <module>
     - Testbench skeleton with UVM
     - Power-aware and area-optimized
     - Ensure no combinational loops
     ```

3. **Iterative Generation**

   * Break RTL generation into **smaller steps**:

     1. Top module skeleton
     2. Sub-module interfaces
     3. Functional FSM logic
     4. Testbench & VIP
   * This reduces **errors and improves modularity**.

4. **Verification-Aware LLM**

   * Feed **simulation results, coverage reports, and linting logs** back into the LLM for **automatic bug fixes**.
   * Example:

     ```text
     Simulation failed for SubModule1, signal X stuck at 1. Suggest RTL fix.
     ```

---

## 3️⃣ File & Data Handling Improvements

1. **Structured File Storage**

   * Keep **separate folders per top-module / sub-module / category**.
   * Include **metadata JSON** describing files: module, category, RTL version, last processed date.

2. **Versioning**

   * Store **multiple versions of generated RTL** for rollback and iterative improvement.
   * Include a **hash/checksum** for each file to avoid duplicate embeddings.

3. **Preprocessing**

   * Strip comments and normalize indentation before embedding to **reduce noise in retrieval**.
   * Tokenize RTL carefully to preserve **signal names and syntax**.

---

## 4️⃣ Workflow & Integration Improvements

1. **Pipeline Orchestration**

   * Use a **task queue** (Celery/RQ) for asynchronous RTL generation and verification.
   * Allows **large designs to process in chunks** and reduces frontend blocking.

2. **Automated Testing**

   * Integrate **linting, CDC checks, and synthesis checks** before feeding results to the LLM.
   * Automatic **pass/fail logging** improves iterative learning.

3. **Hybrid Search**

   * Combine **symbolic search (regex, RTL pattern matching)** with vector-based retrieval.
   * Example: Find all instances of `FSM` or `AXI4 interface` for precise grounding.

4. **Caching**

   * Cache **frequently accessed RTL patterns** or LLM outputs to reduce computation.
   * For RAG, **store top-K embeddings for recent modules** in memory.

---

## 5️⃣ Optional Advanced Improvements

* **Self-hosted LLMs**

  * Use **vLLM / Ollama / local LLaMA variants** for **full offline generation**, reducing latency and dependency on APIs.
* **Knowledge Graph Integration**

  * Build a **VLSI module dependency graph** to guide RTL generation.
  * LLM can reason about **sub-module connections and interface consistency**.
* **PPA Metrics Feedback**

  * Integrate synthesis tools output (power, area, timing) as feedback for **optimization-aware prompts**.
* **Code Style Enforcement**

  * Auto-format generated RTL for **consistent coding style**, signal names, and commenting conventions.

---

Yes — absolutely! The **previous project’s Verilog codes, RTL structures, and verification artifacts** can serve as a strong foundation for **next-generation or derivative ASIC projects**, like your hypothetical H100 → B100 → A100 evolution or Snapdragon successors. Here’s a structured explanation and best practices:

---

## 1️⃣ Why Previous RTL & Verification Code is Reusable

1. **Modular Design**

   * If your RTL is **modular**, e.g., separate modules for ALUs, FIFOs, AXI interconnects, or custom IP blocks, these modules can be **directly reused** in newer chips with minimal modification.
   * Interfaces (ports, buses, handshakes) should be **standardized** to ensure plug-and-play reusability.

2. **Verified Blocks**

   * Any **UVM testbenches, assertions, and formal verification properties** already written for prior projects save time.
   * You can **reuse coverage models and regression suites** with minor adaptations for new features.

3. **Parameterized RTL**

   * If modules are **parameterized** (e.g., bit-width, number of cores, FIFO depth), they can be instantiated for **larger or smaller configurations** without rewriting.

4. **Design Patterns**

   * Architectural patterns like **FSMs, pipelines, bus arbitration, caching schemes** are reusable across chips.
   * Optimization strategies (PPA tuning, clock gating, pipelining) are transferable to newer designs.

---

## 2️⃣ How to Structure Reuse Across Projects

You can organize your **RTL / verification / knowledge base** to make future reuse systematic:

```
projects/
├── A100/
│   ├── rtl/
│   ├── tb/
│   └── docs/
├── H100/
│   ├── rtl/
│   ├── tb/
│   └── docs/
├── B100/
│   ├── rtl/
│   ├── tb/
│   └── docs/
└── common_ip/            # Reusable modules for all projects
    ├── alu/
    ├── axi_interconnect/
    ├── fifo/
    └── vip/
```

**Key points:**

* `common_ip/` holds **well-verified reusable modules**.
* Each project can **instantiate modules from common_ip** and add project-specific blocks.
* Keep **separate UVM testbenches** for project-specific functionality but reuse **shared VIP/test utilities**.

---

## 3️⃣ Verification & Regression Reuse

1. **UVM Components**

   * Agents, monitors, scoreboards, sequences written for previous chips can be **parameterized** for new designs.
   * Example: AXI4 agent can handle different bit-widths or configurations by changing parameters.

2. **Coverage & Assertions**

   * Keep **coverage models generic** for modules (e.g., ALU operations, pipeline stalls) — these can be reused for different chips.
   * Assertions for interfaces (handshake correctness, timing, no combinational loops) are **directly reusable**.

3. **Formal Verification**

   * Properties written in SVA or PSL for prior modules can often be **copied and adapted**.
   * Only project-specific properties (new functionality) need additional formal checks.

---

## 4️⃣ Using Previous Project Knowledge in LLM + RAG Pipelines

Your **RAG + LLM tool** can **learn from past projects** to accelerate new chip designs:

1. Store **previous RTL, VIP, protocols, and verification logs** in your **knowledge base**.
2. When generating new RTL:

   * Retrieve **best practices, optimized FSMs, verified testbenches** from older projects.
   * LLM can **adapt existing RTL patterns** instead of generating from scratch.
3. This reduces **errors, hallucinations, and redundant work**, especially when designing **derivative products** like “B100 improved from H100”.

---

## 5️⃣ Tips for Reuse Across Generations

1. **Versioning**

   * Maintain versions: `H100_v1`, `H100_v2`, `B100_v1`.
   * Track changes to **common_ip** modules for regression tracking.

2. **Parameterization & Config Files**

   * Use **parameters/config files** to tweak module width, pipeline depth, or memory sizes between generations.
   * Helps LLM generate “tuned” versions for new projects automatically.

3. **Documentation**

   * Maintain **design rationale and RTL decisions** in markdown or internal wiki.
   * RAG can reference this to inform new generation designs.

4. **Automated Regression**

   * Use CI/CD pipelines to **re-run UVM regression** whenever a module from `common_ip` is reused in a new project.
   * Ensures **reusability does not introduce bugs**.

---

✅ **In short:**
Your previous projects are **not just reusable—they are assets**. With **modular RTL, reusable VIP, parameterized design, and a well-maintained RAG knowledge base**, you can accelerate **next-gen ASIC designs** like H100 → B100 → A100 and beyond while maintaining quality and PPA optimization.

---

Absolutely! Let’s do it. I can draft a **concrete improvement roadmap** for your front-end VLSI design tool, integrating **RAG + LLM + RTL generation + verification**, and showing **folder structure, pipeline, and iterative feedback loops**.

Here’s a detailed roadmap:

---

## **1️⃣ Folder & Knowledge Base Structure**

```
vlsi-llm-rag/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── file_service.py      # Handles uploads & storage
│   │   │   ├── rtl_generator.py     # LLM generates RTL
│   │   │   ├── vip_generator.py     # LLM generates UVM VIP/testbench
│   │   │   ├── rag_service.py       # Embeddings & retrieval
│   │   │   └── llm_service.py       # LLM call wrapper
│   │   └── utils/
│   │       └── file_parser.py       # Parses specs/documents
│   └── uploads/                     # Stores uploaded files & intermediate results
├── knowledge_base/
│   ├── specs/                        # High-level functional specs
│   ├── protocols/                     # Protocol docs (AXI, SPI, I2C, etc.)
│   └── vector_db/                     # Embeddings for RAG
├── projects/
│   ├── common_ip/                     # Verified reusable RTL modules
│   ├── A100/, H100/, B100/            # Versioned chip projects
│   │   ├── rtl/
│   │   ├── tb/
│   │   └── reports/                   # Lint, simulation, STA logs
└── frontend/                           # React/Vite UI
```

**Key Idea:**

* `uploads/` handles incoming user files.
* `knowledge_base/` is the retrieval source for LLM.
* `common_ip/` ensures reuse across generations.
* `projects/` stores each chip iteration with verification logs.

---

## **2️⃣ RAG + LLM Pipeline (High-Level)**

1. **User Upload & Parsing**

   * User uploads specs, architecture docs, protocol files.
   * `file_parser.py` extracts structured info: modules, interfaces, constraints.

2. **Retrieval (RAG)**

   * `rag_service.py` searches `vector_db/` for similar RTL, testbench patterns, verified IP blocks.
   * Returns **top-K relevant chunks** as context for LLM.

3. **Generation (LLM)**

   * `rtl_generator.py`:

     * Generates **synthesizable RTL** (Verilog/VHDL) using RAG context.
     * Focuses on **PPA optimization**.
   * `vip_generator.py`:

     * Generates **UVM testbench / verification VIP** based on retrieved testbench templates.

4. **Verification Loop**

   * Simulate generated RTL using:

     * Linting
     * Synthesis check (area, timing)
     * UVM simulation / coverage
   * Generate logs and waveforms in `projects/<chip>/reports/`.

5. **Feedback Loop**

   * `rtl_generator.py` takes **verification results** (failures, coverage gaps) and iteratively refines RTL.
   * RAG can retrieve similar **previous bug fixes** to guide correction.

6. **Final Output**

   * Verified, PPA-optimized RTL + UVM testbenches + verification reports.
   * Store in project folder for reuse.

---

## **3️⃣ Iterative Improvement Flow**

```
User Upload → Parsing → RAG Retrieval → LLM RTL/VIP Generation → Verification → Feedback → Refined RTL
```

* **Step 1:** Upload spec → parse modules/interfaces.
* **Step 2:** Retrieve previous similar RTL + protocols.
* **Step 3:** Generate new RTL & VIP testbench.
* **Step 4:** Run lint/sim/synthesis → collect errors, coverage.
* **Step 5:** Feed results back → LLM refines RTL.
* **Step 6:** Repeat until coverage & PPA targets met.
* **Step 7:** Save final RTL & TB → update knowledge base.

---

## **4️⃣ Reuse & Scaling Across Chip Generations**

* Store **golden modules and VIP** in `common_ip/`.
* Future chips (e.g., B100 from H100) can **reuse modules and testbenches**.
* Update `vector_db/` embeddings for **each new RTL iteration**.
* LLM can **retrieve previous verified patterns** for faster generation.

---

## **5️⃣ Suggested Enhancements**

1. **Versioned Embeddings**

   * Keep embeddings for each chip generation to track evolution.

2. **Parameterized RTL**

   * Modules in `common_ip/` should be parameterized for widths, depth, cores.

3. **Automated Regression**

   * Trigger CI/CD regression on reused modules to ensure backward compatibility.

4. **Feedback Storage**

   * Save iterative feedback in `uploads/<user>/feedback.json` for LLM learning.

5. **Performance Metrics**

   * Collect PPA metrics per iteration → LLM can optimize next generation designs.

---

✅ **Outcome:**

* Faster RTL generation with **verified, reusable patterns**.
* Reduced hallucination due to **RAG grounding**.
* **Iterative corrections** ensure correctness and optimal PPA.
* Future generations can **leverage past projects** efficiently.

---






