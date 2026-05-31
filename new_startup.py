import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Indian Startup Funding Dashboard",
    
    layout="wide"
)

st.title("Indian Startup Funding Dashboard (2020-2025)")
st.markdown("---")

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("2020-2025.csv")

# =====================================
# KPI METRICS
# =====================================

total_funding = df["amount"].sum()
total_startups = df["startup"].nunique()
total_industries = df["industry"].nunique()

total_investors = len(
    set(
        df["investors"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )
)

avg_funding = df["amount"].mean()
max_funding = df["amount"].max()

st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Funding", f"₹ {total_funding:,.0f} Cr")

with col2:
    st.metric("🚀 Startups", total_startups)

with col3:
    st.metric("🏭 Industries", total_industries)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("🤝 Investors", total_investors)

with col5:
    st.metric("📈 Avg Funding", f"₹ {avg_funding:,.2f} Cr")

with col6:
    st.metric("🏆 Highest Funding", f"₹ {max_funding:,.2f} Cr")

st.markdown("---")

# =====================================
# YEARLY TREND & ROUND DISTRIBUTION
# =====================================

col1, col2 = st.columns(2)

with col1:

    yearly = (
        df.groupby("year")["amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        yearly,
        x="year",
        y="amount",
        markers=True,
        title="📈 Funding Trend by Year"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    rounds = (
        df["round"]
        .value_counts()
        .reset_index()
    )

    rounds.columns = ["round", "count"]

    fig = px.pie(
        rounds,
        names="round",
        values="count",
        title="🥧 Funding Round Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================
# CITY & INDUSTRY ANALYSIS
# =====================================

col1, col2 = st.columns(2)

with col1:

    city_funding = (
        df.groupby("city")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        city_funding,
        x="amount",
        y="city",
        orientation="h",
        title="🏙️ Top 10 Cities by Funding"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    industry_funding = (
        df.groupby("industry")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        industry_funding,
        x="amount",
        y="industry",
        orientation="h",
        title="🏭 Top 10 Industries by Funding"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================
# INVESTOR & STARTUP ANALYSIS
# =====================================

col1, col2 = st.columns(2)

with col1:

    investors = (
        df["investors"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )

    investors.columns = ["Investor", "Investments"]

    fig = px.bar(
        investors,
        x="Investor",
        y="Investments",
        title="🤝 Top Investors"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    startups = (
        df.groupby("startup")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        startups,
        x="startup",
        y="amount",
        title="🚀 Top Funded Startups"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================
# ADVANCED INSIGHTS
# =====================================

col1, col2 = st.columns(2)

with col1:

    mom = (
        df.groupby(["year", "month"])["amount"]
        .sum()
        .reset_index()
        .sort_values(["year", "month"])
    )

    mom["date"] = pd.to_datetime(
        mom["year"].astype(str)
        + "-"
        + mom["month"].astype(str)
        + "-01"
    )

    fig = px.line(
        mom,
        x="date",
        y="amount",
        markers=True,
        title="📅 Month-on-Month Funding Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    avg_industry = (
        df.groupby("industry")["amount"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        avg_industry,
        x="amount",
        y="industry",
        orientation="h",
        title="🏭 Top Industries by Avg Funding"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================
# INSIGHT TABLES
# =====================================

st.subheader("🔍 Quick Insights")

col1, col2 = st.columns(2)

with col1:

    yearly_startups = (
        df.groupby("year")["startup"]
        .nunique()
        .reset_index()
    )

    yearly_startups.columns = [
        "Year",
        "Unique Startups Funded"
    ]

    st.dataframe(
        yearly_startups,
        use_container_width=True
    )

with col2:

    top_industry_table = (
        df.groupby("industry")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        top_industry_table,
        use_container_width=True
    )

st.markdown("---")

# =====================================
# DOWNLOAD DATA
# =====================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Dataset",
    csv,
    "startup_funding_data.csv",
    "text/csv"
)

# =====================================
# RAW DATA
# =====================================

with st.expander("📄 View Raw Dataset"):
    st.dataframe(df, use_container_width=True)