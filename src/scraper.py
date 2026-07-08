import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.config import QUANT_DISCLOSURES_URL, REQUEST_HEADERS, RAW_DATA_DIR

class PortfolioScraper:
    def __init__(self):
        self.url = QUANT_DISCLOSURES_URL
        self.headers = REQUEST_HEADERS

    def discover_monthly_portfolio_links(self):
        """
        Scrapes the target page to locate links to portfolio files (.xlsx, .xls, .csv).
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Failed to reach statutory disclosures page: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            text = anchor.get_text().lower()
            
            # Target links that contain portfolio terms and are spreadsheets
            if 'portfolio' in href.lower() or 'portfolio' in text:
                if href.endswith(('.xlsx', '.xls', '.csv', '.zip')):
                    full_url = urljoin(self.url, href)
                    if full_url not in links:
                        links.append(full_url)
        return links

    def download_file(self, file_url, custom_filename=None):
        """
        Downloads a specific file asset into the raw data workspace.
        """
        filename = custom_filename if custom_filename else file_url.split('/')[-1]
        destination = RAW_DATA_DIR / filename

        try:
            print(f"📥 Downloading: {filename}...")
            response = requests.get(file_url, headers=self.headers, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"✅ Saved successfully to {destination}")
            return destination
        except requests.RequestException as e:
            print(f"❌ Failed to download asset {file_url}: {e}")
            return None