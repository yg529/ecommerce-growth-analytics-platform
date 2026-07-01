from pathlib import Path

import pandas as pd

from src.core.config import PROCESSED_DATA_PATH, RAW_DATA_PATH


EVENT_COLUMNS = [
    "timestamp",
    "visitorid",
    "event",
    "itemid",
    "transactionid",
]


def load_raw_events(path: str | Path | None = None) -> pd.DataFrame:
    """Load the original RetailRocket events file."""
    csv_path = Path(path) if path is not None else RAW_DATA_PATH

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Raw events file not found: {csv_path}. "
            "Download events.csv and place it under 1_data/raw/."
        )

    df = pd.read_csv(csv_path)
    df.columns = EVENT_COLUMNS
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def load_clean_events(path: str | Path | None = None) -> pd.DataFrame:
    """Load cleaned events produced by src/preprocessing/clean_events.py."""
    csv_path = (
        Path(path)
        if path is not None
        else PROCESSED_DATA_PATH / "events_clean.csv"
    )

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Clean events file not found: {csv_path}. "
            "Run `python src/preprocessing/clean_events.py` first."
        )

    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
