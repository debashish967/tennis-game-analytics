# 🎾 Game Analytics: Unlocking Tennis Data with SportRadar API

## 📌 Project Overview

This project is an **end-to-end sports data analytics application** built using the **SportRadar Tennis API** (with mock data where API access was restricted). It focuses on extracting, storing, analyzing, and visualizing **tennis competition, venue, and doubles competitor ranking data**.

The solution demonstrates a complete analytics workflow:

- API / Mock data extraction
- Data cleaning & sanity checks
- Relational database design (PostgreSQL)
- SQL-based analysis
- Interactive dashboard using Streamlit

---

## 🧠 Problem Statement

To build a comprehensive system that allows users to:

- Explore tennis competition hierarchies
- Analyze venues and complexes
- Study doubles competitor rankings
- Interactively visualize insights using a web application

---

## 🏢 Business Use Cases

1. **Event Exploration** – Navigate competition hierarchies (ATP, ITF, etc.)
2. **Trend Analysis** – Distribution by competition type, gender, category
3. **Performance Insights** – Analyze doubles competitor rankings and points
4. **Decision Support** – Assist organizers and analysts with data-driven insights

---

## 🛠️ Tech Stack

| Component       | Technology            |
| --------------- | --------------------- |
| Language        | Python                |
| API             | SportRadar Tennis API |
| Database        | PostgreSQL            |
| ORM / DB Access | SQLAlchemy            |
| Visualization   | Streamlit             |
| Data Handling   | Pandas                |

---

## 📂 Project Folder Structure

```
Tennis Game/
│
├── app/
│   └── tennis_dashboard.py        # Streamlit dashboard
│
├── data/
│   ├── raw/                        # Raw JSON files from API / mock
│   └── processed/                  # Cleaned CSV files
│       ├── categories.csv
│       ├── competitions.csv
│       ├── complexes.csv
│       ├── venues.csv
│       ├── competitors.csv
│       └── competitor_rankings.csv
│
├── sql/
│   └── tennis_game_analysis.sql    # All SQL DDL + analysis queries
│
└── README.md
```

---

## 🗄️ Database Schema

### 1️⃣ Categories

- `category_id` (PK)
- `category_name`

### 2️⃣ Competitions

- `competition_id` (PK)
- `competition_name`
- `parent_id`
- `type`
- `gender`
- `category_id` (FK)

### 3️⃣ Complexes

- `complex_id` (PK)
- `complex_name`

### 4️⃣ Venues

- `venue_id` (PK)
- `venue_name`
- `city_name`
- `country_name`
- `country_code`
- `timezone`
- `complex_id` (FK)

### 5️⃣ Competitors

- `competitor_id` (PK)
- `name`
- `country`
- `country_code`
- `abbreviation`

### 6️⃣ Competitor Rankings

- `rank`
- `movement`
- `points`
- `competitions_played`
- `competitor_id` (FK)

---

## 📊 SQL Analysis Performed

### Competitions Module

- Competitions by category
- Doubles competitions
- Parent–child competition hierarchy
- Top-level competitions

### Complexes & Venues Module

- Venues per complex
- Country-wise venue distribution
- Timezone analysis
- Multi-venue complexes

### Doubles Rankings Module

- Top-ranked competitors
- Country-wise competitor count
- Highest points leaderboard
- Stable rank competitors

All queries are included in ``.

---

## 📈 Streamlit Dashboard Features

### 🏠 Homepage Dashboard

- Total competitors
- Countries represented
- Highest points scored

### 🔍 Search & Filter

- Search competitor by name
- Filter by country
- Filter by rank range

### 🏆 Leaderboards

- Top-ranked competitors
- Highest points holders

### 🌍 Country-wise Analysis

- Competitor count per country
- Average points per country

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install streamlit pandas sqlalchemy psycopg2-binary
```

### 2️⃣ Start PostgreSQL

- Create database: `tennis_game`
- Execute SQL file: `tennis_game_analysis.sql`

### 3️⃣ Run Streamlit App

```bash
streamlit run app/tennis_dashboard.py
```

---

## ⚠️ Notes on API Usage

- Some SportRadar endpoints (Doubles Rankings) returned **403 / 404** under trial access
- To ensure project completeness, **realistic mock datasets** were generated and used
- Structure and logic strictly follow SportRadar API documentation

---

## ✅ Project Evaluation Checklist

✔ API / Mock data extraction ✔ Clean relational schema ✔ SQL analysis queries ✔ Index optimization ✔ Streamlit interactive dashboard ✔ Error handling & debugging ✔ Documentation & GitHub-ready structure

---

## 🎯 Key Learnings

- Real-world API limitations & workarounds
- Database normalization & FK integrity
- SQL performance optimization
- End-to-end analytics pipeline
- Building data apps with Streamlit

---

## 📌 Author

**Debashish Borah | Data Analyst Project**\
Akash Rawat, Harshad Apage, Siya Negi (Mates)



This project demonstrates production-level data engineering and analytics practices suitable for portfolio and professional evaluation.

---

✨ *End of README*

Thanks to my Teammates!!!
