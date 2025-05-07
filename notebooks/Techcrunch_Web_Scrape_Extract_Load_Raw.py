import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")
print(f"Loaded API Key: {API_KEY}")

# Headers for Firecrawl API
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Step 1: Call Firecrawl
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers=headers,
    json={  # ✅ Only send URL
        "url": "https://techcrunch.com"
    }
)

if response.status_code == 200:
    try:
        data = response.json()
        html = data.get("html")
        print("✅ HTML content successfully retrieved.")
    except Exception as e:
        print("❌ Failed to parse JSON.")
        print("Raw response:", response.text)
        raise e

        # Step 2: Parse with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("a", class_="post-block__title__link")

        if articles:
            all_articles = []
            for article in articles:
                title = article.get_text(strip=True)
                link = article["href"]
                print(f"📰 Title: {title}")
                print(f"🔗 Link: {link}")
                print("-" * 50)
                all_articles.append({"Title": title, "Link": link})

            # Step 3: Save to CSV
            df = pd.DataFrame(all_articles)
            df.to_csv("techcrunch_articles.csv", index=False)
            print("✅ Saved to techcrunch_articles.csv")
        else:
            print("⚠️ No articles found in the HTML.")

