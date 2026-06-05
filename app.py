# Global Conflict Intelligence Dashboard
## app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Global Conflict Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/cleaned/final_dataset.csv")

# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>

    
    .main {
        background-color: #020617;
    }

    section[data-testid="stSidebar"] {
        background-color: #0B1220;
        border-right: 1px solid #1e293b;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #0f172a, #111827);
        border: 1px solid #1e293b;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0px 0px 10px rgba(0,255,255,0.08);
    }

    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
    }

    div[data-testid="metric-container"] div {
        color: white !important;
    }

    .dashboard-title {
        font-size: 48px;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #94a3b8;
        margin-bottom: 1rem;
    }

    .live-status {
        color: #00FFA3;
        font-weight: 600;
        text-align: right;
        font-size: 14px;
        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Control Panel")

country = st.sidebar.multiselect(
    "Select Country",
    sorted(df["Country"].unique())
)

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    df["risk"].unique(),
    default=df["risk"].unique()
)

year_range = st.sidebar.slider(
    "Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (
        int(df["Year"].min()),
        int(df["Year"].max())
    )
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

if country:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(country)
    ]

filtered_df = filtered_df[
    filtered_df["risk"].isin(risk_filter)
]

# =========================
# HEADER
# =========================
col_title, col_status = st.columns([4, 1])

with col_title:
    st.markdown(
        '<div class="dashboard-title"> Global Conflict Intelligence Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Real-time geopolitical conflict analytics and risk assessment system</div>',
        unsafe_allow_html=True
    )

with col_status:
    current_time = datetime.utcnow().strftime("%H:%M UTC")

    st.markdown(
        f'''
        <div class="live-status">
        LIVE FEED ACTIVE<br>
        {current_time}<br>
         AI Monitoring Enabled
        </div>
        ''',
        unsafe_allow_html=True
    )

# =========================
# KPI CARDS (WITH UNITS)
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Conflict Deaths",
    f"{int(filtered_df['deaths'].sum()):,} people"
)

col2.metric(
    "Countries Analyzed",
    f"{filtered_df['Country'].nunique()} countries"
)

col3.metric(
    " High Risk Records",
    f"{(filtered_df['risk'] == 'High').sum()} records"
)

col4.metric(
    " Avg GDP per Capita",
    f"${filtered_df['gdp'].mean():,.2f}"
)

st.markdown("<br>", unsafe_allow_html=True)

col5, col6, col7 = st.columns(3)

col5.metric(
    "📈 Avg Inflation",
    f"{filtered_df['inflation'].mean():.2f}%"
)

col6.metric(
    "👷 Avg Unemployment",
    f"{filtered_df['unemployment'].mean():.2f}%"
)

col7.metric(
    "🗳 Democracy Index",
    f"{filtered_df['democracy'].mean():.3f} / 1.0"
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# MAP MODE SELECTOR
# =========================
map_mode = st.selectbox(
    "Select Map Visualization",
    [
        "Conflict Risk Map",
        "Conflict Deaths",
        "GDP Distribution",
        "Inflation Heatmap"
    ]
)

# =========================
# MAIN MAP
# =========================
st.subheader("Global Intelligence Map")

if map_mode == "Conflict Risk Map":
    fig_map = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="risk",
        hover_name="Country",
        hover_data=["deaths", "gdp", "inflation", "unemployment"],
        color_discrete_map={
            "Low": "#00FFA3",
            "Medium": "#FFB020",
            "High": "#FF4D4D"
        }
    )

elif map_mode == "Conflict Deaths":
    fig_map = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="deaths",
        hover_name="Country",
        color_continuous_scale="Reds"
    )

elif map_mode == "GDP Distribution":
    fig_map = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="gdp",
        hover_name="Country",
        color_continuous_scale="Viridis"
    )

else:
    fig_map = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="inflation",
        hover_name="Country",
        color_continuous_scale="Plasma"
    )

fig_map.update_geos(
    projection_type="natural earth",
    showcoastlines=True,
    coastlinecolor="#475569",
    showland=True,
    landcolor="#1e293b",
    showocean=True,
    oceancolor="#020617",
    bgcolor="#020617"
)

fig_map.update_layout(
    height=700,
    paper_bgcolor="#020617",
    plot_bgcolor="#020617",
    font_color="white",
    margin=dict(l=0, r=0, t=20, b=0)
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# =========================
# ANALYTICS SECTION
# =========================
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("⚠ Top Conflict Countries")

    top_countries = (
        filtered_df.groupby("Country")["deaths"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_bar = px.bar(
        top_countries,
        x="Country",
        y="deaths",
        color="deaths",
        color_continuous_scale="Reds"
    )

    fig_bar.update_layout(
        height=420,
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        font_color="white",
        xaxis_title="",
        yaxis_title="Conflict Deaths"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with right_col:
    st.subheader("Risk Distribution")

    risk_counts = (
        filtered_df["risk"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = ["risk", "count"]

    fig_pie = px.pie(
        risk_counts,
        names="risk",
        values="count",
        hole=0.5,
        color="risk",
        color_discrete_map={
            "Low": "#00FFA3",
            "Medium": "#FFB020",
            "High": "#FF4D4D"
        }
    )

    fig_pie.update_layout(
        height=420,
        paper_bgcolor="#0B1220",
        font_color="white"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# TIMELINE SECTION
# =========================
st.subheader("Conflict Trend Timeline")

trend = (
    filtered_df.groupby("Year")["deaths"]
    .sum()
    .reset_index()
)

fig_line = px.line(
    trend,
    x="Year",
    y="deaths"
)

fig_line.update_traces(line=dict(width=4))

fig_line.update_layout(
    height=450,
    paper_bgcolor="#01030F",
    plot_bgcolor="#0B1220",
    font_color="white",
    xaxis_title="Year",
    yaxis_title="Conflict Deaths"
)

st.plotly_chart(fig_line, use_container_width=True)

# =========================
# DATA TABLE
# =========================
st.subheader("Intelligence Data Feed")

st.dataframe(
    filtered_df.sort_values("deaths", ascending=False),
    use_container_width=True,
    height=350
)
