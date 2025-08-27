import streamlit as st
import pandas as pd

from src.data_loader import load_csv, clean_players
from src.model import simple_rank
from src.viz import bar_top_players


st.set_page_config(page_title="Football Scouting App", layout="wide")
st.title("Football Scouting App")

uploaded = st.file_uploader("Upload player CSV", type=["csv"]) 

if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    st.info("Upload a CSV or place one under data/ and enter filename below.")
    default_name = st.text_input("Filename under data/ (e.g., players.csv)")
    df = None
    if default_name:
        try:
            df = load_csv(default_name)
        except FileNotFoundError:
            st.error("File not found in data/.")

if df is not None:
    st.subheader("Raw Data")
    st.dataframe(df.head(50))

    df = clean_players(df)
    st.subheader("Cleaned Data")
    st.dataframe(df.head(50))

    st.subheader("Ranking")
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    name_col = st.selectbox("Name column", options=list(df.columns))
    selected_metrics = st.multiselect("Metrics to weight", options=numeric_cols, default=numeric_cols[:3])
    weightings = {}
    for col in selected_metrics:
        weightings[col] = st.slider(f"Weight for {col}", -3.0, 3.0, 1.0, 0.1)

    if selected_metrics:
        ranked = simple_rank(df, weightings)
        st.dataframe(ranked[[name_col, *selected_metrics, "score"]].head(50))

        st.subheader("Top Players Chart")
        fig = bar_top_players(ranked, value_col="score", name_col=name_col, top_n=15)
        st.pyplot(fig)
    else:
        st.info("Select at least one metric to rank players.")
else:
    st.stop()


