# 📈 Mutual Fund Portfolio Tracker & Analyzer

An automated, hybrid data pipeline that tracks month-on-month portfolio shifts in Indian mutual funds and uses AI to extract strategic investment insights. 

Built with **Python**, **Pandas**, and **Google Gemini**, this tool cleanly separates deterministic mathematical calculations from qualitative AI analysis.

---

## ✨ Features

* **Automated Data Ingestion:** Web scraper built with `requests` and `BeautifulSoup` to automatically discover and download the latest portfolio statutory disclosures.
* **Self-Healing Data Engine:** A dynamic `pandas` engine that automatically detects headers, bypasses shifting metadata/footer rows, and aligns assets accurately using ISIN codes.
* **Deterministic Delta Tracking:** Mathematically calculates precise quantity and market value shifts, categorizing them strictly into:
  * 🟢 *New Entry*
  * 🔴 *Completely Exited*
  * 📈 *Holdings Increased*
  * 📉 *Holdings Decreased*
* **AI Strategy Analyst:** Passes the structured mathematical outputs to a Google Gemini AI agent to analyze sector rotation, conviction bets, and liquidity trends without risking "math hallucinations".

---

## 📂 Project Structure

```text
mf-portfolio-tracker/
├── data/                      
│   ├── raw/                   # Store downloaded Quant Excel/CSV files here
│   └── processed/             # Output directory for calculated delta CSVs
├── src/                       
│   ├── __init__.py
│   ├── config.py              # Environment variables and path configurations
│   ├── scraper.py             # HTTP requests logic to fetch the latest files
│   ├── engine.py              # The Pandas difference engine
│   └── agents/                
│       ├── __init__.py
│       ├── graph.py           # Gemini API integration and agent state
│       └── prompts.py         # System instructions for the LLM analyst
├── .env                       # Store your GEMINI_API_KEY (git-ignored)
├── .env.example               # Safe template for environment variables
├── .gitignore                 # Prevents committing raw data and keys
├── requirements.txt           # Python dependency list
├── setup.sh / setup.bat       # Environment initialization scripts
└── main.py                    # The orchestrator entry point