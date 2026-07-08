import pandas as pd
import numpy as np
from src.config import PROCESSED_DATA_DIR

class PortfolioEngine:
    @staticmethod
    def clean_dataframe(file_path):
        """
        Loads a file, bypasses header metadata, strips out footers, and normalizes numeric values.
        """
        # Determine engine based on extension
        if str(file_path).endswith('.csv'):
            df = pd.read_csv(file_path, skiprows=7)
        else:
            df = pd.read_excel(file_path, skiprows=7)

        # Standardize column naming systems
        df.columns = [str(col).strip().upper() for col in df.columns]

        # Critical columns check
        required = ['ISIN', 'NAME OF THE INSTRUMENT', 'QUANTITY', 'MARKET VALUE(RS.IN LAKHS)']
        for col in required:
            if col not in df.columns:
                # Fallback check for slight variance in labeling (e.g. spaces)
                matched = [c for c in df.columns if col[:5] in c]
                if matched:
                    df.rename(columns={matched[0]: col}, inplace=True)

        # Drop rows missing an ISIN code (metadata headers, line breaks, or end notes)
        df = df.dropna(subset=['ISIN'])
        df['ISIN'] = df['ISIN'].astype(str).str.strip()
        
        # Guard clause against non-asset entries trapped in the parsing window
        df = df[df['ISIN'].str.startswith('INE', na=False)]

        # Sanitize numeric metrics by eliminating commas or spacing strings
        for num_col in ['QUANTITY', 'MARKET VALUE(RS.IN LAKHS)']:
            if num_col in df.columns:
                df[num_col] = df[num_col].astype(str).str.replace(',', '', regex=True)
                df[num_col] = pd.to_numeric(df[num_col], errors='coerce').fillna(0)

        return df[['ISIN', 'NAME OF THE INSTRUMENT', 'QUANTITY', 'MARKET VALUE(RS.IN LAKHS)']]

    def compute_deltas(self, previous_month_path, current_month_path, output_name="portfolio_delta.csv"):
        """
        Performs an outer join on ISIN to map precise asset changes month-on-month.
        """
        df_prev = self.clean_dataframe(previous_month_path)
        df_curr = self.clean_dataframe(current_month_path)

        # Merge targets on unique asset identifier
        merged = pd.merge(
            df_prev, df_curr, 
            on='ISIN', 
            how='outer', 
            suffixes=('_PREV', '_CURR')
        )

        # Coalesce descriptive fields post-merge
        merged['NAME OF THE INSTRUMENT'] = merged['NAME OF THE INSTRUMENT_CURR'].fillna(merged['NAME OF THE INSTRUMENT_PREV'])
        merged['QUANTITY_PREV'] = merged['QUANTITY_PREV'].fillna(0)
        merged['QUANTITY_CURR'] = merged['QUANTITY_CURR'].fillna(0)
        merged['MARKET VALUE(RS.IN LAKHS)_PREV'] = merged['MARKET VALUE(RS.IN LAKHS)_PREV'].fillna(0)
        merged['MARKET VALUE(RS.IN LAKHS)_CURR'] = merged['MARKET VALUE(RS.IN LAKHS)_CURR'].fillna(0)

        # Numeric transformations
        merged['QTY_DELTA'] = merged['QUANTITY_CURR'] - merged['QUANTITY_PREV']
        merged['VALUE_DELTA_LAKHS'] = merged['MARKET VALUE(RS.IN LAKHS)_CURR'] - merged['MARKET VALUE(RS.IN LAKHS)_PREV']

        # Core categorical evaluation rules
        conditions = [
            (merged['QUANTITY_PREV'] == 0) & (merged['QUANTITY_CURR'] > 0),
            (merged['QUANTITY_PREV'] > 0) & (merged['QUANTITY_CURR'] == 0),
            (merged['QTY_DELTA'] > 0) & (merged['QUANTITY_PREV'] > 0),
            (merged['QTY_DELTA'] < 0) & (merged['QUANTITY_CURR'] > 0)
        ]
        categories = ['New Entry', 'Completely Exited', 'Holdings Increased', 'Holdings Decreased']
        merged['MOVEMENT_TYPE'] = np.select(conditions, categories, default='No Change')

        # Drop unneeded merge residuals
        final_cols = [
            'ISIN', 'NAME OF THE INSTRUMENT', 'QUANTITY_PREV', 'QUANTITY_CURR', 
            'QTY_DELTA', 'MARKET VALUE(RS.IN LAKHS)_PREV', 'MARKET VALUE(RS.IN LAKHS)_CURR', 
            'VALUE_DELTA_LAKHS', 'MOVEMENT_TYPE'
        ]
        result_df = merged[final_cols].sort_values(by='VALUE_DELTA_LAKHS', ascending=False)
        
        # Persist execution trace
        output_path = PROCESSED_DATA_DIR / output_name
        result_df.to_csv(output_path, index=False)
        return result_df, output_path