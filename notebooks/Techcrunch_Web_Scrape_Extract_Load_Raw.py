import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")

if not API_KEY:
    raise ValueError("❌ FIRECRAWL_API_KEY not found in environment variables.")

# Set Firecrawl API headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Step 1: Try scraping full HTML
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers=headers,
    json={"url": "https://techcrunch.com"}
)

data = response.json()
html = data.get("html")

# Step 2: Fallback to extract mode if no HTML is returned
if not html:
    print("⚠️ HTML not returned — retrying with extract mode...")
    response = requests.post(
        "https://api.firecrawl.dev/v1/scrape",
        headers=headers,
        json={
            "url": "https://techcrunch.com",
            "options": {
                "extract": True
            }
        }
    )
    data = response.json()
    html = data.get("html") or data.get("content")

if not html:
    raise ValueError("❌ Neither HTML nor extracted content was returned. Full response:\n" + str(data))

# Step 3: Parse with BeautifulSoup
try:
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("a", class_="post-block__title__link")

    if not articles:
        print("⚠️ No article links found — fallback content may not include HTML structure.")
        raise ValueError("No valid article links found.")

    all_articles = []
    for article in articles:
        title = article.get_text(strip=True)
        link = article.get("href", "")
        all_articles.append({"title": title, "link": link})

    # Step 4: Write to PostgreSQL
    df = pd.DataFrame(all_articles)
    engine = create_engine(
        f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )
    df.to_sql("techcrunch_articles", schema="sql_project", con=engine, if_exists="replace", index=False)
    print("✅ Successfully saved articles to sql_project.techcrunch_articles")

except Exception as e:
    print("❌ Parsing or database write failed:", e)
