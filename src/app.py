import streamlit as st
import pandas as pd
from data_loader import load_data, aggregate_all_stats
from features import add_per90_stats, add_percentiles
from ranking import rank_players

#cache so it loads faster
@st.cache_data
def prepare_data():
    df = load_data()
    df = aggregate_all_stats(df)
    return df

df = prepare_data()

st.sidebar.title("⚽ Football Scouting App")
page = st.sidebar.radio("Navigate", ["Home", "Rankings", "Player Profile"])

if page == "Home":
    st.title("🏠 Home Page")
    st.write("Welcome to my Football Scouting App! ")

elif page == "Rankings":
    st.title("📊 Player Rankings")

    # user selects positions
    positions = st.multiselect(
        "Select positions:",
        options=sorted(df["position"].unique()),
        default=["FW"]
    )

    # user selects stats -> filter out identity columns
    excluded_cols = ["player", "team", "position", "minutes", "age", "nation"]
    all_stats = [c for c in df.columns if c not in excluded_cols]
    key_stats = st.multiselect("Select stats to rank by:", all_stats, default=["goals","expected_goals_xg"])

    if key_stats and positions:
        # apply per90 + percentiles
        df_proc, per90_cols = add_per90_stats(df.copy(), [c for c in key_stats if c != "pass_completion_perc"])
        df_proc, pct_cols = add_percentiles(df_proc, per90_cols)

        # rank players
        ranking_df = rank_players(df_proc, key_stats, positions)

        st.write(f"### Top Players for {positions} ranked by {', '.join(key_stats)}")
        st.dataframe(ranking_df[["player","team","position","ranking_score"]].head(20))

elif page == "Player Profile":
    st.title("📝 Player Profile Page")
    st.write("This is where radar plots will go.")