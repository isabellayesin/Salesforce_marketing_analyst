import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Get environment variables
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

# API call
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
    df = pd.DataFrame(data)

    # Write to PostgreSQL under sql_project schema
    df.to_sql("api_keywords", schema="sql_project", con=engine, if_exists="replace", index=False)
    print("Data loaded successfully into sql_project.api_keywords")

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")

except Exception as db_error:
    print(f"Database write failed: {db_error}")
