# 🔍 SEO + Tech Web Pipeline: Automated Data Collection and Reporting

## 🛠️ Tech Stack

- **Languages & Libraries**: Python, SQL, Pandas, SQLAlchemy, BeautifulSoup
- **Data Warehousing**: AWS RDS – PostgreSQL
- **Scheduling**: GitHub Actions
- **Visualization**: Looker Studio
- **APIs**: Firecrawl API, RapidAPI (Keynew)
- **Version Control**: Git + GitHub

## 🎯 Project Objective

This project is built for **marketing analysts and digital strategists** who need real-time insights into trending keywords and technology news.

- **Who are you helping?**  
  B2B marketers and SEO strategists looking to optimize content or ad targeting with trending, low-competition search terms and timely tech news.
  
- **What problem are you solving?**  
  Manual keyword research and tech trend tracking are time-consuming and often lag behind current events.

- **How will you solve their problem?**  
  By creating an automated data pipeline that scrapes SEO and tech article data daily, stores it in PostgreSQL, and visualizes key trends via Looker dashboards.


## 💼 Job Description

This project aligns with the **Salesforce Marketing Data Analyst** role, which focuses on transforming complex marketing and sales data into actionable insights that drive business growth. As outlined in the job posting, the position requires advanced SQL and data storytelling skills, a strong understanding of marketing KPIs, and the ability to work across teams to support executive decision-making.

The role emphasizes working with large, multi-source datasets, developing custom reports, and building scalable analytical frameworks. It also highlights experience with Looker, Tableau, and Salesforce product knowledge as valuable assets. Analysts are expected to deliver insights through compelling dashboards, presentations, and cross-functional collaboration.

This portfolio project simulates key aspects of that job by:
- Scraping marketing-related data from SEO APIs and news sources
- Transforming unstructured data into analysis-ready tables using Python and SQL
- Loading data into a PostgreSQL RDS instance with a raw schema for scalability
- Automating ingestion with GitHub Actions
- Visualizing insights using Looker Studio to replicate the data storytelling expected of the role

📎 [View full job posting here →](proposal/Job_Description.pdf)


## 📊 Data

### 🔗 Sources
- [https://techcrunch.com](https://techcrunch.com) – scraped via Firecrawl API  
- [https://rapidapi.com/](https://rapidapi.com/hub) – Keynew SEO Keyword API  

### 📌 Characteristics
- **TechCrunch**: title, URL, publish date, source  
- **Keynew**: keyword, volume, CPC, competition, score, timestamp  

## 🧪 Notebooks / Python Scripts

| Script | Description |
|--------|-------------|
| [`Keynew_API_Extract_Load_Raw.py`](notebooks/reports/Keynew_API_Extract_Load_Raw.py) | Extracts keyword data from the Keynew SEO API (via RapidAPI), transforms and filters the data, and loads it to the `raw.api_keywords` table in PostgreSQL. |
| [`Keynew_API_SQL_Analysis.ipynb`](notebooks/Keynew_API_SQL_Analysis.ipynb) | SQL notebook that analyzes keyword trends, identifying high-volume, low-competition terms. |
| [`Techcrunch_Web_Scrape_Extract_Load_Raw.py`](notebooks/reports/Techcrunch_Web_Scrape_Extract_Load_Raw.py) | Scrapes TechCrunch articles using Firecrawl API, parses titles and publish dates, and loads clean data into `raw.techcrunch_articles`. |
| [`Techcrunch_Web_Scrape_SQL_Analysis.ipynb`](notebooks/Techcrunch_Web_Scrape_SQL_Analysis.ipynb) | Notebook that queries the most repeated TechCrunch article titles and visualizes publication frequency trends. |


## 🚀 Future Improvements

- Add **staging and warehouse layers** using dbt for more robust transformations
- Deploy a **dashboard refresh API** trigger from GitHub Actions to automate visual updates in Looker

---
