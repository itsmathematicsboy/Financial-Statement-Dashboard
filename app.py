# =========================
# IMPORT LIBRARY
# =========================
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Investor Financial Dashboard", layout="wide")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    "https://raw.githubusercontent.com/itsmathematicsboy/Financial-Statement-Dashboard/main/Financial%20Statements.csv"
)

df.columns = [col.strip() for col in df.columns]
df = df.dropna()

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("Filter")

    category = st.selectbox(
        "Category",
        ["All"] + sorted(df["Category"].unique())
    )

    if category == "All":
        company_list = sorted(df["Company"].unique())
    else:
        company_list = sorted(df[df["Category"] == category]["Company"].unique())

    company = st.selectbox(
        "Company",
        ["All"] + company_list
    )

    year_range = st.slider(
        "Year Range",
        int(df["Year"].min()),
        int(df["Year"].max()),
        (int(df["Year"].min()), int(df["Year"].max()))
    )

# =========================
# APPLY FILTER
# =========================
filtered = df.copy()

if category != "All":
    filtered = filtered[filtered["Category"] == category]

if company != "All":
    filtered = filtered[filtered["Company"] == company]

filtered = filtered[
    (filtered["Year"] >= year_range[0]) &
    (filtered["Year"] <= year_range[1])
]

# =========================
# YEAR COMPARISON (DELTA)
# =========================
start_year = year_range[0]
end_year = year_range[1]

start_data = filtered[filtered["Year"] == start_year]
end_data = filtered[filtered["Year"] == end_year]

def calc_delta(metric):
    start_val = start_data[metric].sum()
    end_val = end_data[metric].sum()
    return end_val - start_val

# =========================
# EXECUTIVE KPI SECTION
# =========================
st.title("📊 Investor Financial Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"${filtered['Revenue'].sum():,.0f}",
    f"{calc_delta('Revenue'):,.0f}"
)

col2.metric(
    "Net Income",
    f"${filtered['Net Income'].sum():,.0f}",
    f"{calc_delta('Net Income'):,.0f}"
)

col3.metric(
    "Avg ROE",
    f"{filtered['ROE'].mean():.2f}%"
)

col4.metric(
    "Debt / Equity",
    f"{filtered['Debt/Equity Ratio'].mean():.2f}"
)

st.divider()

# =========================
# GROWTH SECTION
# =========================
st.subheader("📈 Growth Analysis")

col1, col2 = st.columns(2)

col1.plotly_chart(
    px.line(
        filtered.groupby("Year")["Revenue"].sum().reset_index(),
        x="Year",
        y="Revenue",
        title="Revenue Trend"
    ),
    use_container_width=True
)

col2.plotly_chart(
    px.line(
        filtered.groupby("Year")["Net Income"].sum().reset_index(),
        x="Year",
        y="Net Income",
        title="Net Income Trend"
    ),
    use_container_width=True
)

# =========================
# PROFITABILITY SECTION
# =========================
st.subheader("💰 Profitability")

col1, col2 = st.columns(2)

col1.plotly_chart(
    px.line(
        filtered.groupby("Year")["ROE"].mean().reset_index(),
        x="Year",
        y="ROE",
        title="ROE Trend"
    ),
    use_container_width=True
)

if "Net Profit Margin" in filtered.columns:
    col2.plotly_chart(
        px.line(
            filtered.groupby("Year")["Net Profit Margin"].mean().reset_index(),
            x="Year",
            y="Net Profit Margin",
            title="Net Margin Trend"
        ),
        use_container_width=True
    )

# =========================
# LEVERAGE SECTION
# =========================
st.subheader("🏦 Risk & Leverage")

col1, col2 = st.columns(2)

col1.plotly_chart(
    px.line(
        filtered.groupby("Year")["Debt/Equity Ratio"].mean().reset_index(),
        x="Year",
        y="Debt/Equity Ratio",
        title="Debt / Equity Trend"
    ),
    use_container_width=True
)

if "Current Ratio" in filtered.columns:
    col2.plotly_chart(
        px.line(
            filtered.groupby("Year")["Current Ratio"].mean().reset_index(),
            x="Year",
            y="Current Ratio",
            title="Current Ratio Trend"
        ),
        use_container_width=True
    )

# =========================
# CASH FLOW SECTION (IF AVAILABLE)
# =========================
if "Operating Cash Flow" in filtered.columns:

    st.subheader("💵 Cash Flow Strength")

    col1, col2 = st.columns(2)

    col1.plotly_chart(
        px.line(
            filtered.groupby("Year")["Operating Cash Flow"].sum().reset_index(),
            x="Year",
            y="Operating Cash Flow",
            title="Operating Cash Flow"
        ),
        use_container_width=True
    )

    if "Free Cash Flow" in filtered.columns:
        col2.plotly_chart(
            px.line(
                filtered.groupby("Year")["Free Cash Flow"].sum().reset_index(),
                x="Year",
                y="Free Cash Flow",
                title="Free Cash Flow"
            ),
            use_container_width=True
        )
