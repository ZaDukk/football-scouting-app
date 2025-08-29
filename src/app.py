import streamlit as st

from data_loader import load_data, aggregate_all_stats, normalize_positions, clean_age_column
from features import add_per90_stats, add_percentiles
from ranking import rank_players
from viz import plot_player_radar

# --------------------------------------------------------------------
# DATA PREP FUNCTIONS
# --------------------------------------------------------------------
@st.cache_data
def load_base_data():
    """Light aggregation only (fast)"""
    df = load_data()
    df = aggregate_all_stats(df)
    df = clean_age_column(df)
    df = normalize_positions(df)
    return df

@st.cache_data
def prepare_profile_data():
    """Heavier step: adds per90 + percentiles for ALL numeric stats."""
    df = load_base_data()
    numeric_cols = df.select_dtypes(include=["number"]).columns
    excluded_cols = ["minutes"]
    all_stats = [c for c in numeric_cols if c not in excluded_cols]
    df, per90_cols = add_per90_stats(df.copy(), [c for c in all_stats if c != "pass_completion_perc"])
    df, pct_cols = add_percentiles(df, per90_cols)
    return df

# --------------------------------------------------------------------
# PAGE NAVIGATION
# --------------------------------------------------------------------
st.sidebar.title("⚽ Football Scouting App")
page = st.sidebar.radio("Navigate", ["Home", "Rankings", "Player Profile"])

# --------------------------------------------------------------------
# HOME PAGE
# --------------------------------------------------------------------

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
    - Automatically get data from many previous seasons and leagues
    - Add scatter plots (e.g. xG vs Goals, Progressive Passes vs Assists)  
    - Market value filters 
    - Custom export/share functionality
    """)

    st.markdown("---")

    st.write(" Navigate using the **sidebar** to get started!")
# --------------------------------------------------------------------
# RANKINGS PAGE
# --------------------------------------------------------------------
elif page == "Rankings":
    st.title("📊 Player Rankings")

    df = load_base_data()

    # Position selector
    positions = st.multiselect(
        "Select positions:",
        options=sorted({pos for sublist in df["position_list"] for pos in sublist}),
        default=["FW"]
    )

    # Age filter
    max_age = st.slider("Show players under age:", min_value=15, max_value=40, value=21)

    # Stats selector
    numeric_cols = df.select_dtypes(include=["number"]).columns
    excluded_cols = ["minutes"]
    all_stats = [c for c in numeric_cols if c not in excluded_cols]
    key_stats = st.multiselect("Select stats to rank by:", all_stats, default=["goals", "expected_goals_xg"])

    # Weight sliders
    weights = {}
    if key_stats:
        with st.expander("⚖️ Adjust Weights", expanded=False):
            st.write("Use sliders to set importance (default = equal).")
            for stat in key_stats:
                weights[stat] = st.slider(
                    f"Weight for {stat}",
                    min_value=0.0, max_value=1.0,
                    value=1.0, step=0.05, key=stat
                )

    # Compute rankings
    if key_stats and positions:
        df_proc, per90_cols = add_per90_stats(df.copy(), [c for c in key_stats if c != "pass_completion_perc"])
        df_proc, pct_cols = add_percentiles(df_proc, per90_cols)

        ranking_df = rank_players(df_proc, key_stats, selected_positions=positions, weights=weights)
        ranking_df = ranking_df[ranking_df["age_years"] <= max_age]

        st.write(f"### Top U{max_age} Players ({positions}) ranked by {', '.join(key_stats)}")
        st.dataframe(ranking_df[["player", "team", "position", "age_years", "ranking_score"]].head(20))

# --------------------------------------------------------------------
# PLAYER PROFILE PAGE
# --------------------------------------------------------------------
elif page == "Player Profile":
    st.title("📝 Player Profiles")

    with st.spinner("Loading player profile data..."):
        df = prepare_profile_data()

    # suggested players (random)
    st.subheader("🎲 Suggested Players")
    suggested = df.sample(3)["player"].tolist()
    st.write(", ".join(suggested))

    st.markdown("---")

    # search bar
    st.subheader("🔎 Search for a Player")
    player_name = st.selectbox("Type or search for a player:", options=sorted(df["player"].unique()))

    if player_name:
        st.markdown(f"### {player_name}")
        team = df[df["player"] == player_name]["team"].iloc[0]
        st.caption(f"Team: {team}")

        # Key stats selector
        default_stats = ["goals", "expected_goals_xg", "goalcreating_actions",
                         "progressive_passes", "carries", "tackles", "blocks"]
        key_stats = st.multiselect(
            "Select stats for radar:",
            options=[c.replace("_per90_pct", "") for c in df.columns if c.endswith("_per90_pct")],
            default=default_stats
        )

        if key_stats:
            row = df[df["player"] == player_name].iloc[0]

            # Plot radar
            fig, ax = plot_player_radar(row, key_stats, title=f"{player_name} Profile")
            st.pyplot(fig)

            # Show raw stats alongside radar
            st.subheader("📊 Raw Stats")
            st.write(row[key_stats])