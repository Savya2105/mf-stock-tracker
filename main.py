import sys
from pathlib import Path
from src.config import RAW_DATA_DIR
from src.engine import PortfolioEngine
from src.agents.graph import PortfolioAnalystAgent

def run_pipeline():
    print("🚀 Initializing Mutual Fund Portfolio Analysis Engine...")

    # Locate sample assets inside project structure
    csv_files = sorted(list(RAW_DATA_DIR.glob("*.csv")) + list(RAW_DATA_DIR.glob("*.xlsx")))
    
    if len(csv_files) < 2:
        print(f"⚠️ Insufficient files located inside data/raw/ directory to process changes.")
        print(f"Please drop your target spreadsheets into: {RAW_DATA_DIR}")
        sys.exit(1)

    # Automatically map trailing chronological history based on listing sequence
    prev_month_file = csv_files[0]
    curr_month_file = csv_files[1]

    print(f"📊 Baseline Month File: {prev_month_file.name}")
    print(f"📊 Comparison Month File: {curr_month_file.name}")

    # Step 1: Execute mathematical computations
    engine = PortfolioEngine()
    delta_df, output_path = engine.compute_deltas(prev_month_file, curr_month_file)
    print(f"📦 Delta verification matrices constructed successfully. Matrix stored at: {output_path}")

    # Step 2: Feed data payload to the analyst node
    print("🧠 Dispatching state variables to Portfolio Analyst Agent...")
    analyst = PortfolioAnalystAgent()
    insights = analyst.generate_portfolio_insights(delta_df)

    # Step 3: Print final report output
    print("\n================================================================================")
    print("📋 STRATEGIC INVESTMENT INSIGHTS REPORT")
    print("================================================================================")
    print(insights)
    print("================================================================================")

if __name__ == "__main__":
    run_pipeline()