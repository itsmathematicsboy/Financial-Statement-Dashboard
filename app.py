# =========================
# IMPORT LIBRARY
# =========================
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Investor Financial Dashboard", layout="wide")

# =========================
# LOAD DATA (CACHED)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/itsmathematicsboy/Financial-Statement-Dashboard/main/Financial%20Statements.csv"
    )
    df.columns = [col.strip() for col in df.columns]
    df = df.dropna()
    return df

df = load_data()

# =========================
# SAFE FUNCTIONS
# =========================
def safe_sum(data, col):
    return data[col].sum() if col in data.columns and not data.empty else 0

def safe_mean(data, col):
    return data[col].mean() if col in data.columns and not data.empty else 0

def safe_group_sum(data, col):
    if col in data.columns and not data.empty:
        return data.groupby("Year")[col].sum().reset_index()
    return pd.DataFrame()

def safe_group_mean(data, col):
    if col in data.columns and not data.empty:
        return data.groupby("Year")[col].mean().reset_index()
    return pd.DataFrame()

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

    company = st.selectbox("Company", ["All"] + company_list)

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
# IF NO DATA
# =========================
if filtered.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# =========================
# YEAR DELTA
# =========================
start_year, end_year = year_range

start_data = filtered[filtered["Year"] == start_year]
end_data = filtered[filtered["Year"] == end_year]

def calc_delta(metric):
    return safe_sum(end_data, metric) - safe_sum(start_data, metric)

# =========================
# HEADER
# =========================
st.title("📊 Investor Financial Dashboard")

st.caption("Growth • Profitability • Risk • Cash Flow Analysis")

# =========================
# KPI SECTION
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"${safe_sum(filtered,'Revenue'):,.0f}",
    f"{calc_delta('Revenue'):,.0f}"
)

col2.metric(
    "Net Income",
    f"${safe_sum(filtered,'Net Income'):,.0f}",
    f"{calc_delta('Net Income'):,.0f}"
)

col3.metric(
    "Average ROE",
    f"{safe_mean(filtered,'ROE'):.2f}%"
)

col4.metric(
    "Debt / Equity",
    f"{safe_mean(filtered,'Debt/Equity Ratio'):.2f}"
)

st.divider()

# =========================
# GROWTH SECTION
# =========================
st.subheader("📈 Growth Analysis")

col1, col2 = st.columns(2)

rev_data = safe_group_sum(filtered, "Revenue")
net_data = safe_group_sum(filtered, "Net Income")

if not rev_data.empty:
    col1.plotly_chart(
        px.line(rev_data, x="Year", y="Revenue", title="Revenue Trend"),
        use_container_width=True
    )

if not net_data.empty:
    col2.plotly_chart(
        px.line(net_data, x="Year", y="Net Income", title="Net Income Trend"),
        use_container_width=True
    )

# =========================
# PROFITABILITY SECTION
# =========================
st.subheader("💰 Profitability")

col1, col2 = st.columns(2)

roe_data = safe_group_mean(filtered, "ROE")
margin_data = safe_group_mean(filtered, "Net Profit Margin")

if not roe_data.empty:
    col1.plotly_chart(
        px.line(roe_data, x="Year", y="ROE", title="ROE Trend"),
        use_container_width=True
    )

if not margin_data.empty:
    col2.plotly_chart(
        px.line(margin_data, x="Year", y="Net Profit Margin", title="Net Margin Trend"),
        use_container_width=True
    )

# =========================
# LEVERAGE SECTION
# =========================
st.subheader("🏦 Risk & Leverage")

col1, col2 = st.columns(2)

de_data = safe_group_mean(filtered, "Debt/Equity Ratio")
cr_data = safe_group_mean(filtered, "Current Ratio")

if not de_data.empty:
    col1.plotly_chart(
        px.line(de_data, x="Year", y="Debt/Equity Ratio", title="Debt / Equity Trend"),
        use_container_width=True
    )

if not cr_data.empty:
    col2.plotly_chart(
        px.line(cr_data, x="Year", y="Current Ratio", title="Current Ratio Trend"),
        use_container_width=True
    )

# =========================
# CASH FLOW SECTION
# =========================
st.subheader("💵 Cash Flow Strength")

col1, col2 = st.columns(2)

ocf_data = safe_group_sum(filtered, "Operating Cash Flow")
fcf_data = safe_group_sum(filtered, "Free Cash Flow")

if not ocf_data.empty:
    col1.plotly_chart(
        px.line(ocf_data, x="Year", y="Operating Cash Flow", title="Operating Cash Flow"),
        use_container_width=True
    )

if not fcf_data.empty:
    col2.plotly_chart(
        px.line(fcf_data, x="Year", y="Free Cash Flow", title="Free Cash Flow"),
        use_container_width=True
    )
