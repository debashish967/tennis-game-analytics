import streamlit as st
import pandas as pd
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="🎾 Tennis Game Analytics",
    layout="wide"
)

st.title("🎾 Tennis Game Analytics Dashboard")

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

# -------------------------------
# LOAD DATA (CSV)
# -------------------------------
@st.cache_data
def load_data():
    competitors = pd.read_csv(os.path.join(DATA_DIR, "competitors.csv"))
    rankings = pd.read_csv(os.path.join(DATA_DIR, "competitor_rankings.csv"))
    return competitors, rankings

competitors_df, rankings_df = load_data()

# Merge data
df = competitors_df.merge(rankings_df, on="competitor_id", how="inner")

# -------------------------------
# KPI SECTION
# -------------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Competitors", df["competitor_id"].nunique())

with col2:
    st.metric("Countries Represented", df["country"].nunique())

with col3:
    st.metric("Highest Points", int(df["points"].max()))

st.divider()

# -------------------------------
# SEARCH & FILTER
# -------------------------------
st.subheader("🔍 Search Competitor")

search = st.text_input("Enter competitor name")

if search:
    filtered_df = df[df["name"].str.contains(search, case=False, na=False)]
else:
    filtered_df = df

st.dataframe(
    filtered_df[["name", "country", "rank", "points", "competitions_played"]],
    use_container_width=True
)

st.divider()

# -------------------------------
# LEADERBOARD
# -------------------------------
st.subheader("🏆 Top 10 Competitors")

top10 = df.sort_values("rank").head(10)

st.dataframe(
    top10[["name", "country", "rank", "points"]],
    use_container_width=True
)

st.divider()

# -------------------------------
# COUNTRY-WISE ANALYSIS
# -------------------------------
st.subheader("🌍 Country-wise Competitor Count")

country_count = (
    df.groupby("country")
    .size()
    .reset_index(name="Competitor Count")
    .sort_values("Competitor Count", ascending=False)
)

st.bar_chart(country_count.set_index("country"))

# -------------------------------
# OVERVIEW METRICS
# -------------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Competitors", competitors_df.shape[0])

with col2:
    st.metric(
        "Countries Represented",
        competitors_df["country"].nunique()
    )

with col3:
    st.metric(
        "Highest Points",
        rankings_df["points"].max()
    )

st.divider()

# -------------------------------
# JOINED DATA
# -------------------------------
merged_df = competitors_df.merge(
    rankings_df,
    on="competitor_id",
    how="inner"
)

# -------------------------------
# FILTERS
# -------------------------------
st.subheader("🔍 Search & Filters")

col1, col2, col3 = st.columns(3)

with col1:
    name_filter = st.text_input("Search Competitor Name")

with col2:
    country_filter = st.selectbox(
        "Filter by Country",
        ["All"] + sorted(merged_df["country"].unique())
    )

with col3:
    min_points = st.slider(
        "Minimum Points",
        int(merged_df["points"].min()),
        int(merged_df["points"].max()),
        int(merged_df["points"].min())
    )

filtered_df = merged_df.copy()

if name_filter:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(name_filter, case=False)
    ]

if country_filter != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == country_filter
    ]

filtered_df = filtered_df[
    filtered_df["points"] >= min_points
]

# -------------------------------
# COMPETITOR TABLE
# -------------------------------
st.subheader("👥 Competitor Rankings")

st.dataframe(
    filtered_df[
        [
            "name",
            "country",
            "rank",
            "movement",
            "points",
            "competitions_played"
        ]
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
        merged_df.sort_values("rank").head(10)[
            ["name", "country", "rank", "points"]
        ],
        use_container_width=True
    )

with col2:
    st.markdown("### 💎 Highest Points")
    st.dataframe(
        merged_df.sort_values("points", ascending=False).head(10)[
            ["name", "country", "points"]
        ],
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

# -------------------------------
# FOOTER
# -------------------------------
st.caption("📌 Data Source: Sportradar API (Mock Data for Rankings)")
