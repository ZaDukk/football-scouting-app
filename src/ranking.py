import pandas as pd


def rank_players(df, key_stats, position_col="position"):
    score_col = "ranking_score"

    # Collect percentile columns
    pct_cols = [f"{s}_per90_pct" for s in key_stats if f"{s}_per90_pct" in df.columns]

    if not pct_cols:
        raise ValueError("None of the chosen stats exist in dataframe!")

    df[score_col] = df[pct_cols].mean(axis=1)  # mean percentile
    return df