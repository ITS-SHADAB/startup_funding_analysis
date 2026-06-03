import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# page congif
st.set_page_config(
    page_title="Startup Funding Analysis",
    layout="wide"
)


# load data
df = pd.read_csv("2020-2025.csv")



# css
st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

[data-testid="stMetric"] {
    background-color: #1e1e1e;
    border: 1px solid #333;
    padding: 10px;
    border-radius: 15px;
    text-align: center
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# Overall Analysis
def overall_analysis():
    st.title("Overall Startup Funding Analysis")
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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Funding", f"₹ {total_funding:,.0f} Cr")
    with col2:
        st.metric("Startups", total_startups)
    with col3:
        st.metric("Industries", total_industries)


    col4,col5, col6 = st.columns(3)

    with col4:
        st.metric("Investors", total_investors)

    with col5:
        st.metric("avg Funding", f"₹ {avg_funding:,.2f} Cr")

    with col6:
        st.metric("Highest Funding", f"₹ {max_funding:,.2f} Cr")

    st.markdown("---")
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
            title="Month-on-Month Funding Trend"
        )

        st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")


    col1, col2 = st.columns(2)
    with col1:
        
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
            title="Funding Round Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
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
            title="Top 10 Cities by Funding"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1,col2=st.columns(2)

    with col1:
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
            title="Top 10 Industries by Funding"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
       
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

# investor
def load_investor(investor):
    st.title(f"{investor} Analysis")

    # Filter all rows where the specified investor is present

    investor_df=df[df["investors"].str.contains(investor,na=False)]

    # RECENT INVESTMENTS 

    st.subheader("Recent investment")

    recent_inv=investor_df.head()[["date", "startup", "industry", "city", "round", "amount"]]

    st.dataframe(recent_inv,use_container_width=True)

    # BIGGEST INVESTMENTS 

    col1,col2= st.columns(2)
    with col1:
        big_inv=investor_df.groupby("startup")["amount"].sum().sort_values(ascending=False).head()

        st.subheader("Biggest Investment")
        fig=px.bar(
            x=big_inv.index,
            y=big_inv.values,
            labels={"x":"Startup","y":"Amount"}

        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        industry_inv = (
            investor_df
            .groupby("industry")["amount"]
            .sum()
        )

        st.subheader("Sector Wise Investments")

        fig=px.pie(
            names=industry_inv.index,
            values=industry_inv.values
        )
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

    col3,col4=st.columns(2)

    with col3:

        st.subheader("stage wise investement")

        stage_inv=investor_df.groupby("round")["amount"].sum()

        fig=px.pie(
            names=stage_inv.index,
            values=stage_inv.values
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    with col4:

        st.subheader("city wise investment")
        city_inv=investor_df.groupby("city")["amount"].sum()

        fig=px.pie(
            names=city_inv.index,
            values=city_inv.values
        )

        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    # ================= YOY GRAPH =================

    yoy_inv = (
        investor_df
        .groupby("year")["amount"]
        .sum()
    )

    st.subheader("📈 Year on Year Investments")

    fig = px.line(
        x=yoy_inv.index,
        y=yoy_inv.values,
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Investment Amount",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    
 
# startup

def startup_analysis(startup):
    st.title(f"{startup} Analysis")

    startup_df = df[df["startup"]==startup]

    # Total Funding
    total_funding=round(startup_df["amount"].sum(),2)

    # Total Investor
    total_investors = startup_df["investors"].str.split(",").explode().nunique()

    # Industry
    industry=startup_df["industry"].mode()[0]

    # City
    city = startup_df["city"].iloc[0]

    col1,col2 = st.columns(2)

    with col1:
        st.metric("Total Funding", f"₹ {total_funding:,.0f} Cr")

    with col2:
        st.metric("Total Investors",total_investors)

    col3,col4 = st.columns(2)

    with col3:
        st.metric("Which Industry",industry)

    with col4:
        st.metric("City",city)





 
    col1,col2 = st.columns(2)
    with col1:

        st.subheader("Funding Timeline")

        timeline = startup_df.sort_values("date")

        fig = px.line(
            timeline,
            x="date",
            y="amount",
            title="Funding Timeline",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Funding Round Distribution")
        round_ds=startup_df["round"].value_counts()

        fig=px.pie(
            names=round_ds.index,
            values=round_ds.values,
            title="Funding Rounds Distribution"
        )

        st.plotly_chart(fig,use_container_width=True)

    col3,col4 = st.columns(2)

   
    st.subheader("Investors List")
    investor_detail = startup_df[["investors","round","amount","date"]].sort_values(by="date")

    st.dataframe(investor_detail,hide_index=True)


     
















st.sidebar.title("Startup Funding Dashboard")

option = st.sidebar.radio(
    "Navigate",
    [
        "Overall Analysis",
        "Startup Analysis",
        "Investor Analysis"
    ]
)

if option == "Overall Analysis":

    overall_analysis()

elif option == "Startup Analysis":

    startup = st.sidebar.selectbox(
        "Select Startup",
        sorted(df["startup"].unique())
    )

    startup_analysis(startup)

elif option == "Investor Analysis":

    investor = st.sidebar.selectbox(
        "Select Investor",
        sorted(
            set(
                df["investors"]
                .dropna()
                .str.split(",")
                .explode()
                .str.strip()
            )
        )
    )

    load_investor(investor)