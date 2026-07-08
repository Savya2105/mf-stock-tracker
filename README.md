# Mutual Fund Portfolio Tracker & Analyzer

A basic tool that tracks month-on-month portfolio shifts in Indian mutual funds and uses AI to extract strategic investment insights.

---

## Features

* **Deterministic Delta Tracking:** Mathematically calculates precise quantity and market value shifts, categorizing them into:
  * 🟢 *New Entry*
  * 🔴 *Completely Exited*
  * 📈 *Holdings Increased*
  * 📉 *Holdings Decreased*
* **AI Strategy Analyst:** Passes the structured mathematical outputs to an AI agent to analyze sector rotation, conviction bets, and liquidity trends without risking "math hallucinations".

---

## To Do

* Make scraper work
* Add fuctionality to analyse across mfs and give insights

---

## Project Structure

```text
mf-portfolio-tracker/
├── data/                      
│   ├── raw/                   # Store downloaded Quant Excel/CSV files here
│   └── processed/             # Output directory for calculated delta CSVs
├── src/                       
│   ├── config.py              # Environment variables and path configurations
│   ├── scraper.py             # HTTP requests logic to fetch the latest files
│   ├── engine.py              # The Pandas difference engine
│   └── agents/                
│       ├── graph.py           # Gemini API integration and agent state
│       └── prompts.py         # System instructions for the LLM analyst
├── .env                       # Store your GEMINI_API_KEY (git-ignored)
├── .env.example               # Safe template for environment variables
├── .gitignore                 # Prevents committing raw data and keys
├── requirements.txt           # Python dependency list
└── main.py                    # The orchestrator entry point