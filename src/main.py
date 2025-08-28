from data_loader import load_data, aggregate_all_stats
from features import add_per90_stats, add_percentiles
from ranking import rank_players

if __name__ == "__main__":
    df = load_data()
    df = aggregate_all_stats(df)

    # Choose some example stats
    key_stats = ["touches","pass_completion_%","progressive_passes","tackles","blocks"]

    # Apply per90 + percentiles
    df, per90_cols = add_per90_stats(df, [c for c in key_stats if c != "pass_completion_perc"])
    df, pct_cols = add_percentiles(df, per90_cols)


    selected_positions = ["CB","RB","LB"]

    ranking_df = rank_players(df, key_stats, selected_positions)

    print(ranking_df[["player","team","position","ranking_score"]].head(20))