import json
import requests
from src.config import GEMINI_API_KEY
from src.agents.prompts import INSIGHT_GENERATION_PROMPT

class PortfolioAnalystAgent:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        # Using the standard v1beta REST endpoint for Gemini
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    def generate_portfolio_insights(self, delta_df):
        """
        Compiles structural data sets and coordinates execution loops using the Requests library.
        """
        if not self.api_key:
            return "❌ Insight generation halted: Missing valid GEMINI_API_KEY in configuration."

        # Compute summary parameters for prompt insertion
        summary_stats = delta_df['MOVEMENT_TYPE'].value_counts().to_dict()
        
        # Extract slices of critical momentum events
        top_buys = delta_df[delta_df['MOVEMENT_TYPE'].isin(['New Entry', 'Holdings Increased'])].head(10)[
            ['NAME OF THE INSTRUMENT', 'MOVEMENT_TYPE', 'QTY_DELTA', 'VALUE_DELTA_LAKHS']
        ].to_dict(orient='records')

        top_sells = delta_df[delta_df['MOVEMENT_TYPE'].isin(['Completely Exited', 'Holdings Decreased'])].tail(10)[
            ['NAME OF THE INSTRUMENT', 'MOVEMENT_TYPE', 'QTY_DELTA', 'VALUE_DELTA_LAKHS']
        ].to_dict(orient='records')

        # Structure final payload format string
        formatted_prompt = INSIGHT_GENERATION_PROMPT.format(
            summary_stats=json.dumps(summary_stats, indent=2),
            top_buys=json.dumps(top_buys, indent=2),
            top_sells=json.dumps(top_sells, indent=2)
        )

        # Build payload structure
        payload = {
            "contents": [{
                "parts": [{"text": formatted_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.95,
                "maxOutputTokens": 4096  # Doubled token limit to ensure complete outputs
            }
        }

        try:
            # Send the request with a generous timeout to allow for full generation
            response = requests.post(
                f"{self.endpoint}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=45
            )
            
            if response.status_code != 200:
                return f"❌ API Error Encountered (Status {response.status_code}): {response.text}"
                
            response_data = response.json()
            
            # Safely extract data based on API schema
            candidate = response_data.get('candidates', [{}])[0]
            finish_reason = candidate.get('finishReason', 'UNKNOWN')
            text_out = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')

            # Append warnings if the API explicitly halted generation early
            if finish_reason == 'MAX_TOKENS':
                text_out += "\n\n[⚠️ WARNING: Output truncated. Reached maximum token limit.]"
            elif finish_reason == 'SAFETY':
                text_out += "\n\n[⚠️ WARNING: Output truncated. Tripped API safety filters.]"

            return text_out

        except requests.exceptions.RequestException as e:
            return f"❌ Pipeline exception encountered during network execution loop: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"❌ Failed to parse API response structure: {str(e)}\nRaw Response: {response_data}"