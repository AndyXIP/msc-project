# Backend Setup & Usage Guide

This guide walks you through setting up your development environment and using the codebase.

---

## Setting up a Python Virtual Environment

### Install Python
Ensure **Python 3.11.6+** is installed.  
Check your version:

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

---

### Create a Virtual Environment
In your backend folder, run:

```bash
python3.11 -m venv .venv
```

This creates a `.venv` directory containing the virtual environment.

---

### Activate the Virtual Environment

- **macOS / Linux**
  ```bash
  source .venv/bin/activate
  ```

- **Windows (PowerShell)**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt)**
  ```cmd
  .\.venv\Scripts\activate
  ```

When activated, your terminal prompt will show `(venv)`.

---

### Install Dependencies
With the environment activated:

```bash
pip install -r requirements.txt
```

---

### Deactivate the Virtual Environment
When finished working:

```bash
deactivate
```

---

## Using the Code

### Hosting Backend

In the backend folder:

```bash
uvicorn app.main:app
```

This runs the backend locally on http://127.0.0.1:8000.

---