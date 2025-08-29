import pandas as pd


def rank_players(df, key_stats, selected_positions=None, weights=None):
    pct_cols = [f"{s}_per90_pct" for s in key_stats if f"{s}_per90_pct" in df.columns]

    if not pct_cols:
        raise ValueError("No percentile columns found for selected stats")

    ranking_df = df.copy()

    if selected_positions:
        mask = ranking_df["position_list"].apply(
            lambda pos_list: any(sel in pos_list for sel in selected_positions)
        )
        ranking_df = ranking_df[mask]

    # apply weights if given / apply  equal weights
    if weights is None:
        weights = {s: 1.0 for s in key_stats}

    # normalize weights so they sum to 1
    total_weight = sum(weights.values())
    weights = {k: v/total_weight for k,v in weights.items()}

    # weighted average score
    score = 0
    for s in key_stats:
        col = f"{s}_per90_pct"
        if col in ranking_df.columns:
            score += ranking_df[col] * weights.get(s, 0)

    ranking_df["ranking_score"] = score
    ranking_df = ranking_df.sort_values("ranking_score", ascending=False).reset_index(drop=True)
    return ranking_df