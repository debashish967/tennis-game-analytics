# tennis_dashboard.py
import streamlit as st
import pandas as pd
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="🎾 Tennis Game Analytics", layout="wide")

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
if not os.path.exists(DATA_DIR):
    st.error(f"DATA_DIR not found: {DATA_DIR}")
    st.stop()




# -------------------------------
# LOAD DATA
# -------------------------------
competitors_df = pd.read_csv(os.path.join(DATA_DIR, "competitors.csv"))
rankings_df = pd.read_csv(os.path.join(DATA_DIR, "competitor_rankings.csv"))

# Merge for analysis
merged_df = competitors_df.merge(rankings_df, on="competitor_id", how="inner")

# -------------------------------
# DASHBOARD TITLE
# -------------------------------
st.title("🎾 Tennis Game Analytics Dashboard")

# -------------------------------
# KPI SECTION
# -------------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Competitors", merged_df["competitor_id"].nunique())
col2.metric("Countries Represented", merged_df["country"].nunique())
col3.metric("Highest Points", merged_df["points"].max())

st.divider()

# -------------------------------
# SEARCH & FILTER
# -------------------------------
st.subheader("🔍 Search & Filter Competitors")

# Filters
name_filter = st.text_input("Search by Competitor Name")
country_filter = st.selectbox(
    "Filter by Country",
    ["All"] + sorted(merged_df["country"].unique())
)
min_points = st.slider(
    "Minimum Points",
    int(merged_df["points"].min()),
    int(merged_df["points"].max()),
    int(merged_df["points"].min())
)

filtered_df = merged_df.copy()
if name_filter:
    filtered_df = filtered_df[filtered_df["name"].str.contains(name_filter, case=False)]
if country_filter != "All":
    filtered_df = filtered_df[filtered_df["country"] == country_filter]
filtered_df = filtered_df[filtered_df["points"] >= min_points]

st.dataframe(
    filtered_df[
        ["name", "country", "rank", "movement", "points", "competitions_played"]
    ].sort_values("rank"),
    use_container_width=True
)

st.divider()

# -------------------------------
# LEADERBOARDS
# -------------------------------
st.subheader("🏆 Leaderboards")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔝 Top 10 by Rank")
    st.dataframe(
        merged_df.sort_values("rank").head(10)[["name", "country", "rank", "points"]],
        use_container_width=True
    )

with col2:
    st.markdown("### 💎 Top 10 by Points")
    st.dataframe(
        merged_df.sort_values("points", ascending=False).head(10)[["name", "country", "points"]],
        use_container_width=True
    )

st.divider()

# -------------------------------
# COUNTRY-WISE ANALYSIS
# -------------------------------
st.subheader("🌍 Country-wise Analysis")

country_stats = (
    merged_df
    .groupby("country")
    .agg(
        total_competitors=("competitor_id", "count"),
        avg_points=("points", "mean")
    )
    .reset_index()
    .sort_values("total_competitors", ascending=False)
)

st.dataframe(country_stats, use_container_width=True)

st.bar_chart(country_stats.set_index("country")["total_competitors"])

# -------------------------------
# FOOTER
# -------------------------------
st.caption("📌 Data Source: Sportradar API (Mock Data for Rankings) ")


