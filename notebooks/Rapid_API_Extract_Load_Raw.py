import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime

# Load environment variables
load_dotenv()

# DB and API credentials
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")

# PostgreSQL engine
engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

# API config
url = "https://seo-keyword-research.p.rapidapi.com/keynew.php"
querystring = {"keyword": "email marketing", "country": "in"}
headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST
}

try:
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    data = response.json()
    print("🔍 Raw API Response:", data)

    # Parse response
    if not isinstance(data, list):
        raise ValueError("❌ Expected a list of keyword entries in the API response.")

    df = pd.DataFrame(data)

    # Clean columns
    df.columns = df.columns.str.lower().str.strip()

    # Rename 'text' to 'keyword'
    if "text" in df.columns:
        df.rename(columns={"text": "keyword"}, inplace=True)

    if "keyword" not in df.columns:
        raise ValueError("❌ 'keyword' column not found after renaming 'text'.")

    df["keyword"] = df["keyword"].astype(str).str.strip().str.lower()
    df = df[df["keyword"].notna() & (df["keyword"] != "")]

    # Add metadata
    df["source"] = "RapidAPI"
    df["scraped_at"] = datetime.utcnow()

    # Load to PostgreSQL
    df.to_sql("api_keywords", schema="public", con=engine, if_exists="replace", index=False)
    print("✅ Cleaned data successfully written to sql_project.api_keywords")

except requests.exceptions.RequestException as e:
    print(f"❌ API request failed: {e}")

except Exception as db_error:
    print(f"❌ Database write failed: {db_error}")
