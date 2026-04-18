import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Import pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.model_pipeline import train_and_evaluate, predict_yield

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

# -------------------------------------------------
# GitHub-Style Professional Dark Theme
# -------------------------------------------------
st.markdown("""
<style>

/* Main background */
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #c9d1d9;
}

/* Global accent override (radio bullets, checkboxes, etc.) */
:root {
    --primary-color: #238636 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b22;
}

/* Headings */
h1, h2, h3 {
    color: #c9d1d9 !important;
    font-weight: 600;
}

/* KPI Cards */
.kpi-card {
    background-color: #161b22;
    padding: 22px;
    border-radius: 8px;
    border: 1px solid #30363d;
}

.kpi-title {
    font-size: 13px;
    color: #8b949e;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 24px;
    font-weight: 600;
    color: #c9d1d9;
}

/* Multiselect tags */
span[data-baseweb="tag"] {
    background-color: #238636 !important;
    color: white !important;
    border: none !important;
}

/* Multiselect dropdown highlight */
li[role="option"][aria-selected="true"] {
    background-color: rgba(35, 134, 54, 0.2) !important;
}

/* Radio & checkbox accent */
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #c9d1d9 !important;
}

/* Download Button */
.stDownloadButton button {
    background-color: #238636;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}

</style>
""", unsafe_allow_html=True)

st.title("Crop Yield Analysis Dashboard")

# -------------------------------------------------
# DATA SOURCE
# -------------------------------------------------
st.sidebar.header("Data Source")

option = st.sidebar.radio("Select Dataset", ["Default Dataset", "Upload CSV"])

if option == "Default Dataset":
    data_path = "data/crop_yield.csv"
    df_full = pd.read_csv(data_path)
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df_full = pd.read_csv(uploaded_file)
        data_path = "temp_uploaded.csv"
        df_full.to_csv(data_path, index=False)
    else:
        st.stop()

# -------------------------------------------------
# TRAIN MODEL ONCE (SESSION SAFE)
# -------------------------------------------------
if "trained_dataset" not in st.session_state or st.session_state.trained_dataset != option:

    model_name, metrics = train_and_evaluate(data_path)

    st.session_state.model_name = model_name
    st.session_state.metrics = metrics
    st.session_state.trained_dataset = option

model_name = st.session_state.model_name
metrics = st.session_state.metrics

# -------------------------------------------------
# FILTERS (ANALYSIS ONLY)
# -------------------------------------------------
df = df_full.copy()

st.sidebar.header("Filters")

if "Crop" in df.columns:
    crop_filter = st.sidebar.multiselect(
        "Crop", df["Crop"].unique(), default=df["Crop"].unique()
    )
    df = df[df["Crop"].isin(crop_filter)]

if "State" in df.columns:
    state_filter = st.sidebar.multiselect(
        "State", df["State"].unique(), default=df["State"].unique()
    )
    df = df[df["State"].isin(state_filter)]

if "Season" in df.columns:
    season_filter = st.sidebar.multiselect(
        "Season", df["Season"].unique(), default=df["Season"].unique()
    )
    df = df[df["Season"].isin(season_filter)]

# -------------------------------------------------
# EXECUTIVE SUMMARY (CUSTOM CARDS)
# -------------------------------------------------
st.subheader("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Total Records</div>
    <div class="kpi-value">{len(df)}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Average Yield</div>
    <div class="kpi-value">{round(df["Yield"].mean(), 2)}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Best Crop</div>
    <div class="kpi-value">{df.groupby("Crop")["Yield"].mean().idxmax()}</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Best State</div>
    <div class="kpi-value">{df.groupby("State")["Yield"].mean().idxmax()}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# YIELD ANALYSIS (PROFESSIONAL STYLING)
# -------------------------------------------------
st.subheader("Yield Analysis")

col1, col2 = st.columns(2)

def styled_bar_chart(data, x_col, y_col):

    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        color_discrete_sequence=["#238636"]
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Yield: %{y:.2f}<extra></extra>"
    )

    fig.update_layout(
        plot_bgcolor="#161b22",
        paper_bgcolor="#161b22",
        font=dict(color="#c9d1d9", size=13),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(color="#8b949e")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#30363d",
            zeroline=False,
            title_font=dict(color="#8b949e")
        )
    )

    return fig

crop_data = df.groupby("Crop")["Yield"].mean().reset_index()
state_data = df.groupby("State")["Yield"].mean().reset_index()

col1.plotly_chart(
    styled_bar_chart(crop_data, "Crop", "Yield"),
    use_container_width=True
)

col2.plotly_chart(
    styled_bar_chart(state_data, "State", "Yield"),
    use_container_width=True
)

# -------------------------------------------------
# MODEL PERFORMANCE
# -------------------------------------------------
st.subheader("Model Performance")

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">Best Model</div>
    <div class="kpi-value">{model_name}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">R² Score</div>
    <div class="kpi-value">{round(metrics["R2"], 4)}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
    <div class="kpi-title">RMSE</div>
    <div class="kpi-value">{round(metrics["RMSE"], 4)}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# PREDICTIONS
# -------------------------------------------------
st.subheader("Predicted Yield")

result_df, importance_df = predict_yield(df)
st.dataframe(result_df.head())

st.subheader("Feature Importance")

fig_importance = px.bar(
    importance_df.head(15),
    x="Importance",
    y="Feature",
    orientation="h",
    color_discrete_sequence=["#238636"]
)

fig_importance.update_traces(
    marker_line_width=0,
    hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>"
)

fig_importance.update_layout(
    plot_bgcolor="#161b22",
    paper_bgcolor="#161b22",
    font=dict(color="#c9d1d9", size=13),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=True, gridcolor="#30363d", zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)

st.plotly_chart(fig_importance, use_container_width=True)

csv = result_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Predictions", csv, "predictions.csv", "text/csv")