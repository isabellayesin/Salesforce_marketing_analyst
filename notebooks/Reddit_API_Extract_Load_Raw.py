
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env file
load_dotenv()

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")

# API call (you've already got this working)
url = "https://seo-keyword-research.p.rapidapi.com/keynew.php"
querystring = {"keyword": "email marketing", "country": "in"}
headers = {
    "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
    "X-RapidAPI-Host": os.getenv("RAPID_API_HOST")
}
response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)

# Connect to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}"
)

# Save data to `raw.api_keywords` table
df.to_sql("api_keywords", schema="raw", con=engine, if_exists="replace", index=False)

df


engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}')

