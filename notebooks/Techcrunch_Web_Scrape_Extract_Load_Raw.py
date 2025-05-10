import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import markdown as md  # For converting markdown to HTML

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

# Step 1: Call Firecrawl API
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers=headers,
    json={"url": "https://techcrunch.com"}
)

if response.status_code == 200:
    try:
        data = response.json()
        print("🔥 Raw API response:", data)

        # Get markdown and convert to HTML
        markdown_content = data.get("data", {}).get("markdown")
        if not markdown_content:
            raise ValueError("❌ Markdown content missing from API response.")
        print("✅ Markdown content successfully retrieved.")

        html = md.markdown(markdown_content)

        # Step 2: Parse HTML
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("a")

        if not articles:
            print("⚠️ No articles found in parsed HTML.")
        else:
            all_articles = []
            for article in articles:
                title = article.get_text(strip=True)
                link = article.get("href", "")

                # Filter out short or irrelevant text
                if title and link and len(title.split()) > 5 and link.startswith("http"):
                    all_articles.append({
                        "title": title,
                        "link": link
                    })

            df = pd.DataFrame(all_articles)

            # Clean: remove duplicates and unnecessary whitespace
            df["title"] = df["title"].str.strip()
            df["link"] = df["link"].str.strip()
            df = df.drop_duplicates()

            # Step 3: Insert into PostgreSQL
            engine = create_engine(
                f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
            )
            df.to_sql("techcrunch_articles", schema="sql_project", con=engine, if_exists="replace", index=False)
            print("✅ Cleaned articles successfully written to sql_project.techcrunch_articles")

    except Exception as e:
        print("❌ An error occurred while processing the response:", e)

else:
    print(f"❌ Request failed with status code {response.status_code}")
    print("Response:", response.text)
