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

Make sure you have a web driver installed, in this case, a chrome driver from https://sites.google.com/chromium.org/driver/ was installed.

In the root folder:

```bash
python web-scraping/scrape.py all
```

This goes through data/data_sources.json and scrapes data from their websites.

---

## 2️⃣ Processing data

In the root folder:

```bash
python ./processing/process_all.py all
```

This goes through the processed scraped data and downloads, crops, captions, tags and creates descriptions for each image.

---

## 3️⃣ Fine tuning the model

In the root folder:

```bash
python ./training/prepare_dataset.py

python ./training/fine_tune.py
```

---

## 4️⃣ Scrape and process trendy hoodies

In the root folder:

```bash
python web-scraping/scrape.py top10
python ./processing/process_all.py top10
python ./processing/trendy_captions_cleaner.py
```

---

## 5️⃣ Generate images

In the root folder:

```bash
python ./generation/generate_hoodie.py
```

---