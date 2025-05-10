import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import markdown as md
import re
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")


# Validate environment
if not API_KEY:
    raise ValueError("❌ FIRECRAWL_API_KEY not found in environment variables.")

# Firecrawl headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Extract date from TechCrunch URL
def extract_date_from_url(url):
    match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url)
    if match:
        try:
            return datetime.strptime(match.group(0).strip('/'), "%Y/%m/%d")
        except ValueError:
            return None
    return None

# Step 1: Scrape TechCrunch homepage
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers=headers,
    json={"url": "https://techcrunch.com"}
)

if response.status_code == 200:
    try:
        data = response.json()
        markdown_content = data.get("data", {}).get("markdown")
        if not markdown_content:
            raise ValueError("❌ Markdown content missing from API response.")

        html = md.markdown(markdown_content)
        soup = BeautifulSoup(html, "html.parser")

        # Step 2: Extract articles using <a> tags
        articles = soup.find_all("a")
        print(f"🧪 Found {len(articles)} <a> tags")

        all_articles = []
        for a in articles:
            title = a.get_text(strip=True)
            link = a.get("href", "")

            if title and link and len(title.split()) > 5 and link.startswith("http"):
                inferred_date = extract_date_from_url(link)
                all_articles.append({
                    "title": title,
                    "link": link,
                    "author": None,  # Placeholder for future use
                    "published_at": inferred_date,
                    "source": "TechCrunch"
                })

        if not all_articles:
            raise ValueError("❌ No valid article links found in <a> tags.")

        # Step 3: Clean data
        df = pd.DataFrame(all_articles)
        df["title"] = df["title"].str.strip()
        df["link"] = df["link"].str.strip()
        df = df.drop_duplicates(subset=["title", "link"])

        # Optional: drop author column if it's always null
        # df = df.drop(columns=["author"])

        # Step 4: Load to PostgreSQL
        engine = create_engine(
            f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
        )
        df.to_sql("techcrunch_articles", schema="sql_project", con=engine, if_exists="replace", index=False)

        print("✅ Articles successfully written to sql_project.techcrunch_articles")

    except Exception as e:
        print("❌ An error occurred while processing the response:", e)

else:
    print(f"❌ Request failed with status code {response.status_code}")
    print("Response:", response.text)
