# 🚀 IDEAS: Intelligent Design & Execution Scripting Compiler

 ![Deployed Link](https://dslpmbygokukhushi.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg)

**IDEAS** is a custom Domain-Specific Language (DSL) and a full 6-phase compiler built from scratch in Python. It translates simple, human-readable text scripts into mathematically optimized, resource-aware project management schedules. 

Instead of dragging blocks on a heavy calendar app like Jira, project managers can write version-controllable text. The IDEAS compiler analyzes the logic, detects circular dependencies, calculates the **Critical Path**, prevents resource double-booking, and outputs a highly interactive Gantt chart.

## ✨ Core Features

*   **Custom Language Syntax:** A strictly typed grammar designed specifically for project management (`TASK`, `DURATION`, `REQUIRES`, `ASSIGNED`).
*   **Directed Acyclic Graph (DAG) Engine:** Automatically maps task dependencies into a mathematical graph.
*   **Infinite Loop Detection:** Uses Depth-First Search (DFS) to catch logical impossibilities (e.g., Task A needs B, but B needs A) before execution.
*   **Critical Path Method (CPM):** Calculates Early Start/Finish and Late Start/Finish to highlight project bottlenecks (Zero-Slack tasks).
*   **Smart Resource Allocation:** Acts like an OS CPU Scheduler. If an employee is double-booked on parallel tasks, the engine automatically delays one task to prevent a collision.
*   **SaaS Backend:** Built-in SQLite database with password hashing (SHA-256) to allow multiple users to register, log in, and save their project timelines securely.
*   **Interactive Web UI:** Built with Streamlit and Plotly to render the compiled JSON data into beautiful, hoverable Gantt charts.

---

## 🏗️ Compiler Architecture

The engine follows a classic 6-phase compiler pipeline:

1.  **Lexical Analysis (`lexer.py`):** Uses Regex to read raw text and tokenize it into functional keywords (`KEYWORD`, `IDENT`, `NUMBER`, `COMMA`).
2.  **Syntax Analysis (`parser.py`):** Validates the token order against the strict IDEAS grammar rules and builds an Abstract Syntax Tree (AST).
3.  **Semantic Analysis (`semantic.py`):** The logic checker. Verifies that dependencies actually exist and traces the graph via DFS to prevent infinite loops.
4.  **Intermediate Representation (`ir_gen.py`):** Strips away language concepts and builds a pure mathematical blueprint (DAG) of predecessors and successors.
5.  **Code Optimization (`optimizer.py`):** The "Brain." Runs forward and backward passes to calculate parallel execution, slack time, and resource availability calendars.
6.  **Code Generation (`codegen.py`):** Packages the optimized mathematical schedule into a structured JSON file for downstream UI consumption.

---

## 📖 Language Documentation

Writing IDEAS code is incredibly simple. The compiler ignores spaces and tabs, but strictly enforces the keyword order.

### The Syntax
`TASK [Name] DURATION [Days] (Optional: REQUIRES [Deps]) (Optional: ASSIGNED [Person])`

### Example Script
```text
TASK Foundation DURATION 5 ASSIGNED Builder
TASK Walls DURATION 4 REQUIRES Foundation ASSIGNED Builder
TASK Roof DURATION 3 REQUIRES Walls ASSIGNED Builder
TASK Garden DURATION 2 REQUIRES Foundation ASSIGNED Landscaper
TASK Final_Inspection DURATION 1 REQUIRES Roof, Garden ASSIGNED Inspector
Note: The compiler is smart enough to handle multiple requirements separated by commas, and can accept REQUIRES and ASSIGNED in any order.

💻 Installation & Local Setup
Want to run the compiler on your own machine? Follow these steps:

1. Clone the repository

Bash
git clone [https://github.com/yourusername/ideas-compiler.git](https://github.com/yourusername/ideas-compiler.git)
cd ideas-compiler
2. Install dependencies

Bash
pip install -r requirements.txt
3. Initialize the Database
Run the setup script to build the local SQLite database for the SaaS features.

Bash
python setup_db.py
4. Launch the Web Application

Bash
streamlit run app.py
