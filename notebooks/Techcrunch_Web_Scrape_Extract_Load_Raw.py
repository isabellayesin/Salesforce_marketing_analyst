import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")

if not API_KEY:
    raise ValueError("❌ FIRECRAWL_API_KEY not found in environment variables.")

# Set Firecrawl API headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Step 1: Call Firecrawl
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers=headers,
    json={"url": "https://techcrunch.com"}
)

if response.status_code == 200:
    try:
        data = response.json()
        print("🔎 Full API response:", data)
        html = data.get("html")
        if not html:
            raise ValueError("❌ HTML content missing from API response.")
        print("✅ HTML content successfully retrieved.")

        # Step 2: Parse HTML from Firecrawl
