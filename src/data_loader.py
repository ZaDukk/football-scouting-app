import pandas as pd
from pathlib import Path
from unidecode import unidecode

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "database.csv"


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


def normalize_positions(df):
    """
    convert comma-separated position strings into clean lists.
    """
    df["position_list"] = df["position"].apply(
        lambda x: [p.strip() for p in str(x).split(",")]
    )
    return df


def clean_age_column(df):

    # Convert FBref style age '22-123' into just 22
    if df["age"].dtype == "object":
        df["age_years"] = df["age"].astype(str).str.split("-").str[0].astype(int)
    else:
        df["age_years"] = df["age"]
    return df







