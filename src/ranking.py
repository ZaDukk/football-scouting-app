import pandas as pd


def rank_players(df, key_stats, selected_positions=None):

    pct_cols = [f"{s}_per90_pct" for s in key_stats if f"{s}_per90_pct" in df.columns]

    if not pct_cols:
        raise ValueError("No percentile columns found for selected stats!")

    ranking_df = df.copy()

    # Filter by positions, if provided
    if selected_positions:
        # Keep rows where ANY selected position is in the player's position string
        mask = ranking_df["position"].apply(
            lambda pos: any(sel in str(pos) for sel in selected_positions)
        )
        ranking_df = ranking_df[mask]


    ranking_df["ranking_score"] = ranking_df[pct_cols].mean(axis=1)

    # Sort descending (best players first)
    ranking_df = ranking_df.sort_values("ranking_score", ascending=False).reset_index(drop=True)

    return ranking_df