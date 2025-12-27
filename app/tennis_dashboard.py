# tennis_dashboard.py
import streamlit as st
import pandas as pd
import os
import math

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="🎾 Tennis Game Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PATH SETUP
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "Data", "Processed")

if not os.path.exists(DATA_DIR):
    st.error(f"DATA_DIR not found: {DATA_DIR}")
    st.stop()

# =====================================================
# LOAD DATA
# =====================================================
competitors_df = pd.read_csv(os.path.join(DATA_DIR, "competitors.csv"))
rankings_df = pd.read_csv(os.path.join(DATA_DIR, "competitor_rankings.csv"))
competitions_df = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
categories_df = pd.read_csv(os.path.join(DATA_DIR, "categories.csv"))
complexes_df = pd.read_csv(os.path.join(DATA_DIR, "complexes.csv"))
venues_df = pd.read_csv(os.path.join(DATA_DIR, "venues.csv"))

merged_df = competitors_df.merge(
    rankings_df, on="competitor_id", how="inner"
)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.title("🎾 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Overview",
        "👤 Competitors",
        "🏆 Competitions",
        "🏟️ Complexes & Venues",
        "🧠 SQL Explorer"
    ]
)

# =====================================================
# PAGINATION
# =====================================================
def paginate_dataframe(df, page_size=20):
    total_rows = df.shape[0]
    total_pages = max(1, math.ceil(total_rows / page_size))

    page_num = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1,
        step=1
    )

    start = (page_num - 1) * page_size
    end = start + page_size
    return df.iloc[start:end]

# =====================================================
# OVERVIEW
# =====================================================
if page == "🏠 Overview":
    st.title("🎾 Tennis Game Analytics Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", merged_df["competitor_id"].nunique())
    col2.metric("Countries Represented", merged_df["country"].nunique())
    col3.metric("Highest Points", merged_df["points"].max())

    st.divider()
    st.markdown("""
    ### 📌 Dashboard Capabilities
    - 👤 Competitor performance & rankings  
    - 🏆 Competition & category insights  
    - 🏟️ Venues & sports complexes  
    - 🧠 SQL-driven analytics (beginner-friendly)  
    """)

# =====================================================
# COMPETITORS
# =====================================================
elif page == "👤 Competitors":
    st.title("👤 Competitor Analytics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Competitors", merged_df.shape[0])
    col2.metric("Countries", merged_df["country"].nunique())
    col3.metric("Max Points", merged_df["points"].max())

    st.divider()

    name_filter = st.selectbox(
        "Search Competitor",
        ["All"] + sorted(merged_df["name"].unique())
    )

    country_filter = st.selectbox(
        "Country",
        ["All"] + sorted(merged_df["country"].unique())
    )

    min_points = st.slider(
        "Minimum Points",
        int(merged_df["points"].min()),
        int(merged_df["points"].max()),
        int(merged_df["points"].min())
    )

    df = merged_df.copy()
    if name_filter != "All":
        df = df[df["name"] == name_filter]
    if country_filter != "All":
        df = df[df["country"] == country_filter]

    df = df[df["points"] >= min_points]

    st.subheader("📋 Competitor Table")
    st.dataframe(
        paginate_dataframe(df.sort_values("rank")),
        use_container_width=True
    )

    st.subheader("🏆 Top 10 Competitors")
    st.bar_chart(
        merged_df.sort_values("rank").head(10).set_index("name")["points"]
    )

# =====================================================
# COMPETITIONS
# =====================================================
elif page == "🏆 Competitions":
    st.title("🏆 Competitions Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Competitions", competitions_df.shape[0])
    col2.metric("Types", competitions_df["type"].nunique())
    col3.metric("Categories", categories_df.shape[0])

    comp_merged = competitions_df.merge(
        categories_df, on="category_id", how="left"
    )

    st.subheader("📊 Competition Types")
    st.bar_chart(comp_merged["type"].value_counts())

    st.subheader("🚻 Gender Distribution")
    st.bar_chart(comp_merged["gender"].value_counts())

    st.subheader("📋 Competition Details")
    st.dataframe(
        paginate_dataframe(comp_merged, 25),
        use_container_width=True
    )

# =====================================================
# COMPLEXES & VENUES
# =====================================================
elif page == "🏟️ Complexes & Venues":
    st.title("🏟️ Complexes & Venues Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Complexes", complexes_df.shape[0])
    col2.metric("Venues", venues_df.shape[0])
    col3.metric("Countries", venues_df["country_name"].nunique())

    st.subheader("🌍 Venues by Country")
    st.bar_chart(venues_df["country_name"].value_counts().head(15))

    st.subheader("🏟️ Venues per Complex")
    st.bar_chart(
        venues_df.groupby("complex_id").size().head(15)
    )

    st.subheader("📋 Venue Details")
    st.dataframe(
        paginate_dataframe(venues_df, 25),
        use_container_width=True
    )

# =====================================================
# SQL EXPLORER (FIXED & EXTENDED)
# =====================================================
elif page == "🧠 SQL Explorer":
    st.title("🧠 SQL Analytics Explorer")

    sql_catalog = {
        "Top 5 Ranked Competitors":
            merged_df.sort_values("rank").head(5),

        "Top 10 Competitors by Points":
            merged_df.sort_values("points", ascending=False).head(10),

        "Competitors per Country":
            merged_df["country"].value_counts().reset_index(),

        "Average Points by Country":
            merged_df.groupby("country")["points"].mean().reset_index(),

        "Total Competitions by Category":
            competitions_df.merge(categories_df, on="category_id")
            .groupby("category_name").size().reset_index(name="count"),

        "Competitions by Gender":
            competitions_df["gender"].value_counts().reset_index(),

        "Venues by Country":
            venues_df["country_name"].value_counts().reset_index(),

        "Venues per Complex":
            venues_df.groupby("complex_id").size().reset_index(name="venues"),

        "Countries with Most Competitors":
            merged_df["country"].value_counts().head(10).reset_index(),

        "Lowest Ranked Competitors":
            merged_df.sort_values("rank", ascending=False).head(10),

        "Competitors with Rank Movement":
            merged_df[merged_df["movement"] != 0]
            .sort_values("movement", ascending=False)
            .head(10),

        "Competitors Played Most Competitions":
            merged_df.sort_values(
                "competitions_played", ascending=False
            ).head(10)
    }

    selected_analysis = st.selectbox(
        "Select an Analysis (Human Language)",
        list(sql_catalog.keys())
    )

    st.subheader("📊 Result")
    st.dataframe(
        sql_catalog[selected_analysis],
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================
st.caption(
    "📌 Data Source: Sportradar API (Mock Data) | "
    "Project Done by Debashish Borah, Akash Rawat, Harshad Apage, Siya Negi"
)
