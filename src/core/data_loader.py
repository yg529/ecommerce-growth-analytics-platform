import pandas as pd

from src.core.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH
)


def load_raw_events():
    """
    读取原始行为数据
    """

    df = pd.read_csv(
        RAW_DATA_PATH / "events.csv"
    )

    df.columns = [
        "timestamp",
        "visitorid",
        "event",
        "itemid",
        "transactionid"
    ]

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms"
    )

    return df


def load_clean_events():
    """
    读取清洗后的行为数据
    """

    df = pd.read_csv(
        PROCESSED_DATA_PATH / "events_clean.csv"
    )

    # CSV读取后恢复时间类型
    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df