import pandas as pd
from pathlib import Path
from unidecode import unidecode

DATA_PATH = Path(r"C:\Users\joshu\Downloads\Everything\Programming\summer project\football-scouting-app\data\database.csv")


def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")

    # normalise column names (lowercase, underscores)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "perc")
        .str.replace(r"[^\w\s]", "", regex=True)  # remove brackets/symbols
    )

    #remove accents fromm player names for ease of use
    df["player"] = df["player"].apply(lambda x: unidecode(str(x)))

    return df


def aggregate_all_stats(df):
    # Columns we want to keep as identifiers (not summed)
    non_numeric_cols = ["player", "team", "position", "nation", "age"]

    # Numeric = the rest
    numeric_cols = df.select_dtypes(include="number").columns

    agg_dict = {col: "sum" for col in numeric_cols if col not in non_numeric_cols}

    # Keep first value for identifiers
    for col in non_numeric_cols:
        if col in df.columns:
            agg_dict[col] = "first"

    season_df = df.groupby(["player", "team"], as_index=False).agg(agg_dict)

    return season_df








