from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# Page configuration
st.set_page_config(
    page_title="World Happiness Report",
    page_icon="🌐",
    layout="wide",
)

st.title("🌍 World Happiness Dashboard")
st.caption("Source: World Happiness Report 2023 | Kaggle")

# Load the CSV from the data folder beside this app
DATA = Path(__file__).parent / "data" / "world_happiness_2023.csv"

if not DATA.exists():
    st.error(
        "Dataset not found. Place world_happiness_2023.csv inside the "
        "'data' folder next to app.py."
    )
    st.stop()

df = pd.read_csv(DATA)

# The lecture dataset is expected to contain these nine columns
expected_columns = [
    "Country", "Region", "Score", "GDP", "Social_Support",
    "Life_Expectancy", "Freedom", "Generosity", "Corruption"
]

if len(df.columns) == len(expected_columns):
    df.columns = expected_columns
else:
    st.error(
        f"Expected {len(expected_columns)} columns, but the CSV has "
        f"{len(df.columns)}. Please check that you downloaded the "
        "World Happiness Report 2023 dataset used in class."
    )
    st.stop()

# Ensure the chart variables are numeric
for column in ["Score", "GDP"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=["Country", "Region", "Score", "GDP"])

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    regions = ["All Regions"] + sorted(df["Region"].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N countries", 5, 25, 15)

# Apply region filter
filtered = (
    df.copy()
    if selected_region == "All Regions"
    else df[df["Region"] == selected_region].copy()
)

top = filtered.nlargest(top_n, "Score").sort_values("Score")

# KPI row
col1, col2, col3 = st.columns(3)
col1.metric("Countries", len(filtered))

global_avg = df["Score"].mean()
region_avg = filtered["Score"].mean()
col2.metric(
    "Average Happiness Score",
    f"{region_avg:.2f}",
    f"{region_avg - global_avg:+.2f} vs global average",
)

happiest_country = filtered.nlargest(1, "Score")["Country"].iloc[0]
col3.metric("Happiest Country", happiest_country)

st.divider()

# Chart 1: Top happiest countries
st.subheader(f"Top {top_n} Happiest Countries — {selected_region}")

fig1 = px.bar(
    top,
    x="Score",
    y="Country",
    orientation="h",
    labels={"Score": "Happiness Score (0–10)", "Country": ""},
    template="plotly_white",
    height=600,
)

fig1.update_layout(
    title_font=dict(family="Arial", size=16, color="slategrey"),
    xaxis=dict(range=[0, 8.0]),
)

st.plotly_chart(fig1, width="stretch")

st.divider()

# Chart 2: Diverging continuous colour scale
# The meaningful midpoint is the global average happiness score.
st.subheader("GDP per Capita vs Happiness Score")
st.write(
    "Colour shows happiness score relative to the global average. "
    "Red indicates below-average scores and blue indicates above-average scores."
)

# Use a symmetric colour range around the global average so the midpoint
# is centred in the diverging scale.
score_min = df["Score"].min()
score_max = df["Score"].max()
spread = max(global_avg - score_min, score_max - global_avg)
color_range = [global_avg - spread, global_avg + spread]

fig2 = px.scatter(
    filtered,
    x="GDP",
    y="Score",
    hover_name="Country",
    color="Score",
    color_continuous_scale="RdBu",
    range_color=color_range,
    color_continuous_midpoint=global_avg,
    labels={
        "GDP": "GDP per capita",
        "Score": "Happiness Score (0–10)",
    },
    template="plotly_white",
    title="Happiness Score and GDP per Capita",
)

# Annotate the meaningful midpoint directly on the chart
fig2.add_hline(
    y=global_avg,
    line_dash="dash",
    line_width=2,
    line_color="gray",
    annotation_text=f"Midpoint: global average = {global_avg:.2f}",
    annotation_position="top left",
)

fig2.update_layout(height=550)
st.plotly_chart(fig2, width="stretch")

st.divider()

if st.button("Send balloons!"):
    st.balloons()

st.caption("Built with Streamlit + Plotly")
