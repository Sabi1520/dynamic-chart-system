import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG
# -----------------------------
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Dynamic AI-Powered Chart Dashboard",
    layout="wide"
)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_chart_config():
    response = requests.get(f"{BACKEND_URL}/api/chart/config")
    response.raise_for_status()
    return response.json()

def update_context(payload):
    response = requests.post(f"{BACKEND_URL}/api/context", json=payload)
    response.raise_for_status()
    return response.json()

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.title("Chart Controls")

chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["bar", "pie", "line"]
)

x_axis = st.sidebar.selectbox(
    "X Axis",
    ["region", "product_category"]
)

y_axis = st.sidebar.selectbox(
    "Y Axis",
    ["amount", "units_sold"]
)

if st.sidebar.button("Update Chart"):
    payload = {
        "chart_type": chart_type,
        "x_axis": x_axis,
        "y_axis": y_axis
    }
    update_context(payload)
    st.success("Chart context updated!")
    st.rerun()

# -----------------------------
# MAIN UI
# -----------------------------
st.title("📊 Dynamic AI-Powered Chart Dashboard")

# Fetch chart configuration
chart_config = get_chart_config()

chart_type = chart_config["chart_type"]
data = chart_config["data"]
x_axis = chart_config.get("x_axis")
y_axis = chart_config.get("y_axis")

df = pd.DataFrame(data)

st.subheader(f"Chart Type: {chart_type.upper()}")

# -----------------------------
# CHART RENDERING LOGIC
# -----------------------------
if x_axis and "value" in df.columns:
    df_plot = df.copy()
else:
    st.warning("No aggregated data available for chart rendering.")
    df_plot = None

if df_plot is not None:
    if chart_type == "bar":
        st.bar_chart(df_plot.set_index(x_axis)["value"])

    elif chart_type == "line":
        st.line_chart(df_plot.set_index(x_axis)["value"])

    elif chart_type == "pie":
        fig, ax = plt.subplots()
        ax.pie(
            df_plot["value"],
            labels=df_plot[x_axis],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

# -----------------------------
# RAW DATA VIEW
# -----------------------------
with st.expander("View Raw Data"):
    st.dataframe(df)
