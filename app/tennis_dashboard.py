<<<<<<< HEAD
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
st.write("📁 Using DATA_DIR:", DATA_DIR)

# =====================================================
# LOAD DATA
# =====================================================
competitors_df = pd.read_csv(os.path.join(DATA_DIR, "competitors.csv"))
rankings_df = pd.read_csv(os.path.join(DATA_DIR, "competitor_rankings.csv"))

competitions_df = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
categories_df = pd.read_csv(os.path.join(DATA_DIR, "categories.csv"))

complexes_df = pd.read_csv(os.path.join(DATA_DIR, "complexes.csv"))
venues_df = pd.read_csv(os.path.join(DATA_DIR, "venues.csv"))

# Merge competitor + rankings
merged_df = competitors_df.merge(rankings_df, on="competitor_id", how="inner")

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
# REUSABLE PAGINATION
# =====================================================
def paginate_dataframe(df, page_size=20):
    total_rows = df.shape[0]
    total_pages = math.ceil(total_rows / page_size)

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
# OVERVIEW PAGE
# =====================================================
if page == "🏠 Overview":
    st.title("🎾 Tennis Game Analytics Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", merged_df["competitor_id"].nunique())
    col2.metric("Countries Represented", merged_df["country"].nunique())
    col3.metric("Highest Points", merged_df["points"].max())

    st.divider()

    st.subheader("📌 What You Can Explore")
    st.markdown("""
    - 🎯 Competitor rankings & performance  
    - 🏆 Tournament & competition insights  
    - 🏟️ Sports complexes & venues distribution  
    - 🧠 SQL-powered analytics (user friendly)  
    """)

# =====================================================
# COMPETITORS DASHBOARD
# =====================================================
elif page == "👤 Competitors":
    st.title("👤 Competitor Analytics")

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", merged_df.shape[0])
    col2.metric("Countries", merged_df["country"].nunique())
    col3.metric("Max Points", merged_df["points"].max())

    st.divider()

    # SEARCH WITH AUTOCOMPLETE
    st.subheader("🔍 Search Competitor")
    competitor_name = st.selectbox(
        "Search by Competitor Name",
        options=[""] + sorted(merged_df["name"].unique())
    )

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

    if competitor_name:
        filtered_df = filtered_df[filtered_df["name"] == competitor_name]

    if country_filter != "All":
        filtered_df = filtered_df[filtered_df["country"] == country_filter]

    filtered_df = filtered_df[filtered_df["points"] >= min_points]

    st.subheader("📋 Competitor Details")
    paged_df = paginate_dataframe(filtered_df.sort_values("rank"))
    st.dataframe(
        paged_df[["name", "country", "rank", "movement", "points", "competitions_played"]],
        use_container_width=True
    )

    # Visualization 1
    st.subheader("🏆 Top 10 by Rank")
    st.bar_chart(
        merged_df.sort_values("rank").head(10).set_index("name")["points"]
    )

    # Visualization 2
    st.subheader("🌍 Competitors by Country")
    st.bar_chart(merged_df["country"].value_counts().head(10))

# =====================================================
# COMPETITIONS DASHBOARD
# =====================================================
elif page == "🏆 Competitions":
    st.title("🏆 Competitions Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitions", competitions_df.shape[0])
    col2.metric("Competition Types", competitions_df["type"].nunique())
    col3.metric("Categories", categories_df.shape[0])

    st.divider()

    comp_merged = competitions_df.merge(categories_df, on="category_id", how="left")

    # Visualization 3
    st.subheader("📊 Competition Type Distribution")
    st.bar_chart(comp_merged["type"].value_counts())

    # Visualization 4
    st.subheader("🚻 Gender Distribution")
    st.bar_chart(comp_merged["gender"].value_counts())

    # Visualization 5
    st.subheader("🏷️ Top Categories by Competition Count")
    st.bar_chart(comp_merged["category_name"].value_counts().head(15))

    st.subheader("📋 Competition Details (Paginated)")
    paged_df = paginate_dataframe(comp_merged, page_size=25)
    st.dataframe(paged_df, use_container_width=True)

# =====================================================
# COMPLEXES & VENUES DASHBOARD
# =====================================================
elif page == "🏟️ Complexes & Venues":
    st.title("🏟️ Complexes & Venues Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complexes", complexes_df.shape[0])
    col2.metric("Total Venues", venues_df.shape[0])
    col3.metric("Countries", venues_df["country_name"].nunique())

    st.divider()

    st.subheader("🌍 Venues by Country")
    st.bar_chart(venues_df["country_name"].value_counts().head(15))

    st.subheader("🏟️ Venues per Complex")
    st.bar_chart(
        venues_df.groupby("complex_id").size().sort_values(ascending=False).head(15)
    )

    country_filter = st.selectbox(
        "Filter Venues by Country",
        ["All"] + sorted(venues_df["country_name"].unique())
    )

    filtered_venues = venues_df.copy()
    if country_filter != "All":
        filtered_venues = filtered_venues[
            filtered_venues["country_name"] == country_filter
        ]

    st.subheader("📋 Venue Details (Paginated)")
    paged_df = paginate_dataframe(filtered_venues, page_size=25)
    st.dataframe(paged_df, use_container_width=True)

# =====================================================
# SQL QUERY EXPLORER (USER FRIENDLY)
# =====================================================
elif page == "🧠 SQL Explorer":
    st.title("🧠 SQL Analytics Explorer")

    sql_options = {
        "Top 5 Ranked Competitors":
            "SELECT name, rank, points FROM competitors c "
            "JOIN competitor_rankings r ON c.competitor_id = r.competitor_id "
            "ORDER BY rank LIMIT 5;",

        "Competitors with Highest Points":
            "SELECT name, points FROM competitors c "
            "JOIN competitor_rankings r ON c.competitor_id = r.competitor_id "
            "ORDER BY points DESC LIMIT 5;",

        "Competitions by Category":
            "SELECT category_name, COUNT(*) FROM competitions c "
            "JOIN categories cat ON c.category_id = cat.category_id "
            "GROUP BY category_name;",

        "Venues by Country":
            "SELECT country_name, COUNT(*) FROM venues GROUP BY country_name;"
    }

    selected_query = st.selectbox(
        "Select an analysis",
        list(sql_options.keys())
    )

    st.subheader("📄 SQL Query")
    st.code(sql_options[selected_query], language="sql")

    st.subheader("📊 Query Result (Preview)")

    if selected_query == "Top 5 Ranked Competitors":
        st.dataframe(merged_df.sort_values("rank").head(5))
    elif selected_query == "Competitors with Highest Points":
        st.dataframe(merged_df.sort_values("points", ascending=False).head(5))
    elif selected_query == "Competitions by Category":
        st.dataframe(
            competitions_df.merge(categories_df, on="category_id")
            .groupby("category_name")
            .size()
            .reset_index(name="count")
        )
    elif selected_query == "Venues by Country":
        st.dataframe(
            venues_df["country_name"].value_counts().reset_index()
        )

# =====================================================
# FOOTER
# =====================================================
st.caption(
    "📌 Data Source: Sportradar API (Mock Rankings Data) | "
    "Project by Debashish Borah, Akash Rawat, Harshad Apage, Siya Negi"
)
=======
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
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

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

# Merge competitor + rankings
merged_df = competitors_df.merge(rankings_df, on="competitor_id", how="inner")

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
# REUSABLE PAGINATION
# =====================================================
def paginate_dataframe(df, page_size=20):
    total_rows = df.shape[0]
    total_pages = math.ceil(total_rows / page_size)

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
# OVERVIEW PAGE
# =====================================================
if page == "🏠 Overview":
    st.title("🎾 Tennis Game Analytics Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", merged_df["competitor_id"].nunique())
    col2.metric("Countries Represented", merged_df["country"].nunique())
    col3.metric("Highest Points", merged_df["points"].max())

    st.divider()

    st.subheader("📌 What You Can Explore")
    st.markdown("""
    - 🎯 Competitor rankings & performance  
    - 🏆 Tournament & competition insights  
    - 🏟️ Sports complexes & venues distribution  
    - 🧠 SQL-powered analytics (user friendly)  
    """)

# =====================================================
# COMPETITORS DASHBOARD
# =====================================================
elif page == "👤 Competitors":
    st.title("👤 Competitor Analytics")

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", merged_df.shape[0])
    col2.metric("Countries", merged_df["country"].nunique())
    col3.metric("Max Points", merged_df["points"].max())

    st.divider()

    # SEARCH WITH AUTOCOMPLETE
    st.subheader("🔍 Search Competitor")
    competitor_name = st.selectbox(
        "Search by Competitor Name",
        options=[""] + sorted(merged_df["name"].unique())
    )

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

    if competitor_name:
        filtered_df = filtered_df[filtered_df["name"] == competitor_name]

    if country_filter != "All":
        filtered_df = filtered_df[filtered_df["country"] == country_filter]

    filtered_df = filtered_df[filtered_df["points"] >= min_points]

    st.subheader("📋 Competitor Details")
    paged_df = paginate_dataframe(filtered_df.sort_values("rank"))
    st.dataframe(
        paged_df[["name", "country", "rank", "movement", "points", "competitions_played"]],
        use_container_width=True
    )

    # Visualization 1
    st.subheader("🏆 Top 10 by Rank")
    st.bar_chart(
        merged_df.sort_values("rank").head(10).set_index("name")["points"]
    )

    # Visualization 2
    st.subheader("🌍 Competitors by Country")
    st.bar_chart(merged_df["country"].value_counts().head(10))

# =====================================================
# COMPETITIONS DASHBOARD
# =====================================================
elif page == "🏆 Competitions":
    st.title("🏆 Competitions Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitions", competitions_df.shape[0])
    col2.metric("Competition Types", competitions_df["type"].nunique())
    col3.metric("Categories", categories_df.shape[0])

    st.divider()

    comp_merged = competitions_df.merge(categories_df, on="category_id", how="left")

    # Visualization 3
    st.subheader("📊 Competition Type Distribution")
    st.bar_chart(comp_merged["type"].value_counts())

    # Visualization 4
    st.subheader("🚻 Gender Distribution")
    st.bar_chart(comp_merged["gender"].value_counts())

    # Visualization 5
    st.subheader("🏷️ Top Categories by Competition Count")
    st.bar_chart(comp_merged["category_name"].value_counts().head(15))

    st.subheader("📋 Competition Details (Paginated)")
    paged_df = paginate_dataframe(comp_merged, page_size=25)
    st.dataframe(paged_df, use_container_width=True)

# =====================================================
# COMPLEXES & VENUES DASHBOARD
# =====================================================
elif page == "🏟️ Complexes & Venues":
    st.title("🏟️ Complexes & Venues Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complexes", complexes_df.shape[0])
    col2.metric("Total Venues", venues_df.shape[0])
    col3.metric("Countries", venues_df["country_name"].nunique())

    st.divider()

    st.subheader("🌍 Venues by Country")
    st.bar_chart(venues_df["country_name"].value_counts().head(15))

    st.subheader("🏟️ Venues per Complex")
    st.bar_chart(
        venues_df.groupby("complex_id").size().sort_values(ascending=False).head(15)
    )

    country_filter = st.selectbox(
        "Filter Venues by Country",
        ["All"] + sorted(venues_df["country_name"].unique())
    )

    filtered_venues = venues_df.copy()
    if country_filter != "All":
        filtered_venues = filtered_venues[
            filtered_venues["country_name"] == country_filter
        ]

    st.subheader("📋 Venue Details (Paginated)")
    paged_df = paginate_dataframe(filtered_venues, page_size=25)
    st.dataframe(paged_df, use_container_width=True)

# =====================================================
# SQL QUERY EXPLORER (USER FRIENDLY)
# =====================================================
elif page == "🧠 SQL Explorer":
    st.title("🧠 SQL Analytics Explorer")

    sql_options = {
        "Top 5 Ranked Competitors":
            "SELECT name, rank, points FROM competitors c "
            "JOIN competitor_rankings r ON c.competitor_id = r.competitor_id "
            "ORDER BY rank LIMIT 5;",

        "Competitors with Highest Points":
            "SELECT name, points FROM competitors c "
            "JOIN competitor_rankings r ON c.competitor_id = r.competitor_id "
            "ORDER BY points DESC LIMIT 5;",

        "Competitions by Category":
            "SELECT category_name, COUNT(*) FROM competitions c "
            "JOIN categories cat ON c.category_id = cat.category_id "
            "GROUP BY category_name;",

        "Venues by Country":
            "SELECT country_name, COUNT(*) FROM venues GROUP BY country_name;"
    }

    selected_query = st.selectbox(
        "Select an analysis",
        list(sql_options.keys())
    )

    st.subheader("📄 SQL Query")
    st.code(sql_options[selected_query], language="sql")

    st.subheader("📊 Query Result (Preview)")

    if selected_query == "Top 5 Ranked Competitors":
        st.dataframe(merged_df.sort_values("rank").head(5))
    elif selected_query == "Competitors with Highest Points":
        st.dataframe(merged_df.sort_values("points", ascending=False).head(5))
    elif selected_query == "Competitions by Category":
        st.dataframe(
            competitions_df.merge(categories_df, on="category_id")
            .groupby("category_name")
            .size()
            .reset_index(name="count")
        )
    elif selected_query == "Venues by Country":
        st.dataframe(
            venues_df["country_name"].value_counts().reset_index()
        )

# =====================================================
# FOOTER
# =====================================================
st.caption(
    "📌 Data Source: Sportradar API (Mock Rankings Data) | "
    "Project by Debashish Borah, Akash Rawat, Harshad Apage, Siya Negi"
)
>>>>>>> 52cdd34d18d48a1052a6d6287e4c439b08e1a324
