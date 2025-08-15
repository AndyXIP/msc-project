# Setting up a Python Virtual Environment

## 1️⃣ Install Python
Make sure Python 3.11.6+ is installed.  
Check your version:

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

---

## 2️⃣ Create a Virtual Environment
In your project folder:

```bash
python3.11 -m venv .venv
```

This creates a `.venv` directory containing the virtual environment.

---

## 3️⃣ Activate the Virtual Environment

- **macOS / Linux**
```bash
source venv/bin/activate
```

- **Windows (PowerShell)**
```powershell
venv\Scripts\Activate.ps1
```

- **Windows (Command Prompt)**
```cmd
venv\Scripts\activate.bat
```

When activated, you’ll see `(venv)` in your terminal prompt.

---

## 4️⃣ Install Dependencies
With the environment activated:

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Deactivate the Virtual Environment
When you’re done working:

```bash
deactivate
```

---

# Using the code

## 1️⃣ Web scrape data

In the root folder:

```bash
python web-scraping/scrape.py all
```

This goes through data/data_sources.json and scrapes data from their websites.

---

## 2️⃣ Processing data