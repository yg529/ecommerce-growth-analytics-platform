import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.core.config import PROCESSED_DATA_PATH, RAW_DATA_PATH
from src.core.data_loader import EVENT_COLUMNS


def load_raw_events(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = EVENT_COLUMNS
    return df


def convert_time(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], unit="ms")
    return cleaned


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["visitorid", "event", "itemid"])


def normalize_event(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["event"] = cleaned["event"].str.lower()
    valid_events = {"view", "addtocart", "transaction"}
    return cleaned[cleaned["event"].isin(valid_events)]


def sort_events(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(["visitorid", "timestamp"])


def clean_events(path: str | Path) -> pd.DataFrame:
    df = load_raw_events(path)
    df = convert_time(df)
    df = drop_duplicates(df)
    df = handle_missing(df)
    df = normalize_event(df)
    return sort_events(df)


def save_clean(df: pd.DataFrame, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def main():
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_DATA_PATH}. "
            "Download RetailRocket events.csv into 1_data/raw/."
        )

    output_path = PROCESSED_DATA_PATH / "events_clean.csv"
    df = clean_events(RAW_DATA_PATH)
    save_clean(df, output_path)
    print(f"Cleaning done: {df.shape}, saved to {output_path}")


if __name__ == "__main__":
    main()
