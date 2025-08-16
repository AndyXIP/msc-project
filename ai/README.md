# Project Setup & Usage Guide

This guide walks you through setting up your development environment and using the codebase.

---

## ⚙️ Setting up a Python Virtual Environment

### 1️⃣ Install Python
Ensure **Python 3.11.6+** is installed.  
Check your version:

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

---

### 2️⃣ Create a Virtual Environment
In your project folder, run:

```bash
python3.11 -m venv .venv
```

This creates a `.venv` directory containing the virtual environment.

---

### 3️⃣ Activate the Virtual Environment

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

### 4️⃣ Install Dependencies
With the environment activated:

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Deactivate the Virtual Environment
When finished working:

```bash
deactivate
```

---

## 🛠️ Using the Code

### 1️⃣ Web Scrape Data
Make sure you have a **Chrome WebDriver** installed. Download from: [chromedriver](https://sites.google.com/chromium.org/driver/).

In the ai folder:

```bash
python web-scraping/scrape.py all
```

This goes through `data/data_sources.json` and scrapes data from their websites.

---

### 2️⃣ Process Data
In the ai folder:

```bash
python processing/process_all.py all
```

This processes the scraped data: downloads, crops, captions, tags, and generates descriptions for each image.

---

### 3️⃣ Fine-Tune the Model
In the ai folder:

```bash
python training/prepare_dataset.py
python training/fine_tune.py
```

---

### 4️⃣ Scrape & Process Trendy Hoodies
In the ai folder:

```bash
python web-scraping/scrape.py top10
python processing/process_all.py top10
python processing/trendy_captions_cleaner.py
```

---

### 5️⃣ Generate Images
In the ai folder:

```bash
python generation/generate_hoodie.py
```

This process generates 30 hoodies from the top 10 hoodies of each website.

---