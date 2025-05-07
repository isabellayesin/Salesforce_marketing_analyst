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

        # Step 2: Parse HTML
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("a", class_="post-block__title__link")

        if not articles:
            print("⚠️ No articles found on the page.")
        else:
            all_articles = []
            for article in articles:
                title = article.get_text(strip=True)
                link = article.get("href", "")
                all_articles.append({"Title": title, "Link": link})

            df = pd.DataFrame(all_articles)
            output_path = os.path.join("data", "techcrunch_articles.csv")
            os.makedirs("data", exist_ok=True)
            df.to_csv(output_path, index=False)
            print(f"✅ Saved {len(df)} articles to {output_path}")
    
    except Exception as e:
        print("❌ An error occurred while processing the response:", e)

else:
    print(f"❌ Request failed with status code {response.status_code}")
    print("Response:", response.text)
