def add_per90_stats(df, stats_columns, minutes_column="minutes"):

    per90_cols = []
    for col in stats_columns:
        if col in df.columns:
            df[col + "_per90"] = df[col] / (df[minutes_column] / 90).replace(0, 1)
            per90_cols.append(col + "_per90")
        else:
            print(f"️ Column '{col}' not found in dataframe, skipping.")
    return df, per90_cols


def add_percentiles(df, stats_columns):

    pct_cols = []
    for col in stats_columns:
        if col in df.columns:
            df[col + "_pct"] = df[col].rank(pct=True) * 100
            pct_cols.append(col + "_pct")
        else:
            print(f" Column '{col}' not found in dataframe, skipping.")
    return df, pct_cols