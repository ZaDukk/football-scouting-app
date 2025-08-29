import streamlit as st
import pandas as pd
from data_loader import load_data, aggregate_all_stats, normalize_positions, clean_age_column
from features import add_per90_stats, add_percentiles
from ranking import rank_players
from viz import plot_player_radar

#cache so it loads faster
@st.cache_data
def prepare_data():
    df = load_data()
    df = aggregate_all_stats(df)
    df = normalize_positions(df)
    df = clean_age_column(df)
    return df

df = prepare_data()

st.sidebar.title("⚽ Football Scouting App")
page = st.sidebar.radio("Navigate", ["Home", "Rankings", "Player Profile"])

if page == "Home":
    st.title("⚽ Football Scouting App")
    st.subheader("by **Joshua Kaitharam Thomas**")

    st.markdown("---")

    st.markdown("""
    ## 📖 Overview
    Welcome to the **Football Scouting App**, built to combine football analytics with an interactive scouting tool.
    This web app currently uses only EPL 24/25 data and allows you explore and visualise player performance in key metrics and create rankings to find hidden gems.  

    ### ✅ Current Features
    - **Rankings Page**  
      ⚽ Select positions and stats → ranks all players dynamically  
      📊 Supports custom age filters (e.g. U21, U23)  
      ⚖️ Adjust weights for selected stats via interactive sliders  

    - **Player Profile Page**  
      🎲 Random player suggestions for discovery  
      🔎 Search any player with auto‑fill  
      📈 Create radar charts with customizable stats  
      🗒 View raw values alongside radar visualizations  

    ### Planned Features 
    - Automatically get data from many pervious seasons and leauges
    - Add scatterplots (e.g. xG vs Goals, Progressive Passes vs Assists)  
    - Market value filters 
    - Custom export/share functionality
    """)

    st.markdown("---")

    st.write(" Navigate using the **sidebar** to get started!")

elif page == "Rankings":
    st.title("📊 Player Rankings")

    positions = st.multiselect(
        "Select positions:",
        options=sorted({pos for sublist in df["position_list"] for pos in sublist}),
        default=["FW"]
    )

    max_age = st.slider("Show players under age:", min_value=15, max_value=40, value=21)

    numeric_cols = df.select_dtypes(include=["number"]).columns
    excluded_cols = ["minutes"]
    all_stats = [c for c in numeric_cols if c not in excluded_cols]

    key_stats = st.multiselect(
        "Select stats to rank by:",
        all_stats,
        default=["goals","expected_goals_xg"]
    )

    # expander for weights
    weights = {}
    if key_stats:
        with st.expander("⚖️ Adjust Weights", expanded=False):
            st.write("Use the sliders to set importance for each stat (default = equal).")
            for stat in key_stats:
                weights[stat] = st.slider(
                    f"Weight for {stat}",
                    min_value=0.0, max_value=1.0,
                    value=1.0, step=0.05, key=stat
                )

    if key_stats and positions:
        df_proc, per90_cols = add_per90_stats(
            df.copy(),
            [c for c in key_stats if c != "pass_completion_perc"]
        )
        df_proc, pct_cols = add_percentiles(df_proc, per90_cols)

        # pass weights to rank_players
        ranking_df = rank_players(df_proc, key_stats, positions, weights=weights)

        ranking_df = ranking_df[ranking_df["age_years"] <= max_age]

        st.write(f"### Top U{max_age} Players ({positions}) ranked by {', '.join(key_stats)}")
        st.dataframe(ranking_df[["player","team","position","age_years","ranking_score"]].head(20))

elif page == "Player Profile":
    st.title("📝 Player Profiles")

    # 🎲 Suggest a few random players
    st.subheader("Some Random Suggestions")
    suggested = df.sample(3)["player"].tolist()
    st.write(", ".join(suggested))

    st.markdown("---")

    # 🔎 Search Bar
    st.subheader("Search for a Player")
    player_name = st.selectbox(
        "Type to search for a player:",
        options=sorted(df["player"].unique())
    )

    if player_name:
        st.markdown(f"### {player_name}")

        # Default key_stats for profiles
        default_stats = [
            "goals", "expected_goals_xg",
            "goalcreating_actions", "progressive_passes",
            "carries", "tackles", "blocks"
        ]

        # Let user pick stats to plot
        key_stats = st.multiselect(
            "Select stats for radar:",
            options=[c for c in df.columns if c not in ["player","team","position","minutes","age","nation","position_list"]],
            default=default_stats
        )

        if key_stats:
            # Make sure per90 + percentiles exist
            df_proc, per90_cols = add_per90_stats(df.copy(), [c for c in key_stats if c != "pass_completion_perc"])
            df_proc, pct_cols = add_percentiles(df_proc, per90_cols)

            # Get the player row
            row = df_proc[df_proc["player"] == player_name].iloc[0]

            # Plot radar
            fig, ax = plot_player_radar(row, key_stats, title=f"{player_name} – Profile")
            st.pyplot(fig)

            # Show raw table of their stats (optional)
            st.subheader("Player Stats")
            st.write(row[key_stats])