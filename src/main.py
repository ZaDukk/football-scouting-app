from data_loader import load_data, aggregate_all_stats
from features import add_per90_stats, add_percentiles
from ranking import rank_players

if __name__ == "__main__":

    df = load_data()
    df = aggregate_all_stats(df)

    # Key stats
    key_stats = ["goals", "assists", "expected_goals_xg", "progressive_passes", "tackles", "blocks"]

    # Add per90 + percentiles
    df, per90_cols = add_per90_stats(df, [c for c in key_stats if c != "pass_completion_perc"])
    df, pct_cols = add_percentiles(df, per90_cols)

    # Rank players across chosen stats
    df = rank_players(df, key_stats)

    print(df[["player", "team", "position", "ranking_score"]].sort_values("ranking_score", ascending=False).head(20))