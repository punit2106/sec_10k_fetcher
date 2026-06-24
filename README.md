## Quick Start (Dev Container)

1. Open the project in VS Code
2. Click **"Reopen in Container"** when prompted
3. Run:

```bash
python main.py
```

# SEC 10-K Report Fetcher

Fetches the latest 10-K annual reports from SEC EDGAR for major companies and saves them as PDFs.

**Companies covered:** Apple, Meta, Alphabet, Amazon, Netflix, Goldman Sachs

---

## Quick Start (Dev Container)

1. Open the project in VS Code
2. Click **"Reopen in Container"** when prompted
3. Run:
```bash
python main.py
```

---

## Manual Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Install Playwright's Chromium browser**
```bash
playwright install --with-deps chromium
```

**3. Run**
```bash
python main.py
```

---

PDFs will be saved in the `output/` folder.

## Project Structure
sec_10k_fetcher/

├── .devcontainer/

│   └── devcontainer.json  # Dev Container config

├── config.py              # Company CIK mapping

├── main.py                # Orchestrator

├── sec_client.py          # SEC EDGAR API logic

├── pdf_converter.py       # HTML download + Playwright PDF export

├── requirements.txt

├── AI_PROMPT_LOG.md       # AI usage log

└── output/                # PDFs saved here

## How it works

1. `sec_client.py` queries the SEC EDGAR submissions API using each company's CIK number to find the latest 10-K filing URL
2. `pdf_converter.py` downloads the filing HTML via `requests`, then renders it locally in a headless Chromium browser via Playwright and exports it as a PDF
3. A single browser instance is reused across all companies for efficiency

## Adding companies

Add a new entry to `config.py`:
```python
COMPANIES = {
    "Apple": "0000320193",
    "New Company": "0001234567",  # look up CIK at sec.gov
}
```