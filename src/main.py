from matplotlib import pyplot as plt

from data_loader import load_data, aggregate_all_stats
from features import add_per90_stats, add_percentiles
from ranking import rank_players
from viz import plot_player_radar
import matplotlib
matplotlib.use("TkAgg")

if __name__ == "__main__":
    df = load_data()
    df = aggregate_all_stats(df)


    # Choose some example stats
    key_stats = ["goals","total_shoot"]
    selected_positions = ["FW"]

    # Apply per90 + percentiles
    df, per90_cols = add_per90_stats(df, [c for c in key_stats if c != "pass_completion_perc"])
    df, pct_cols = add_percentiles(df, per90_cols)




    ranking_df = rank_players(df, key_stats, selected_positions)

    print(ranking_df[["player","team","position","ranking_score"]].head(20))


    key_stats = ["goals","expected_goals_xg","goalcreating_actions",
                 "progressive_passes","carries","tackles","blocks"]

    df, per90_cols = add_per90_stats(df, [c for c in key_stats if c != "pass_completion_perc"])
    df, pct_cols = add_percentiles(df, per90_cols)

    player_name = "Cole Palmer"
    row = df[df["player"] == player_name].iloc[0]

    fig, ax = plot_player_radar(row, key_stats, title=f"{player_name} – Profile 24/25 PL")
    plt.show()

