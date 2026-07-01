"""
Validation utilities for RetailRocket event data.
"""

import pandas as pd

REQUIRED_COLUMNS = [
    "timestamp",
    "visitorid",
    "event",
    "itemid",
]


def validate_events(df: pd.DataFrame) -> bool:
    """
    Validate event data before analysis.

    Checks:
    --------
    1. DataFrame is not empty.
    2. Required columns exist.
    3. Timestamp column is datetime.
    4. Event values are valid.
    5. Required columns contain no missing values.
    6. Duplicate rows do not exist.

    Parameters
    ----------
    df : pd.DataFrame
        Event dataset.

    Returns
    -------
    bool
        True if validation passes.

    Raises
    ------
    ValueError
        If data validation fails.
    TypeError
        If timestamp is not datetime.
    """

    # ① DataFrame 是否为空
    if df.empty:
        raise ValueError("DataFrame is empty.")

    # ② 是否缺少字段
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # ③ timestamp 是否为 datetime
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        raise TypeError(
            "Column 'timestamp' must be datetime64."
        )

    # ④ 是否存在缺失值
    missing_values = df[REQUIRED_COLUMNS].isnull().sum()

    if missing_values.any():
        raise ValueError(
            f"Missing values detected:\n{missing_values[missing_values > 0]}"
        )

    # ⑤ event 是否合法
    valid_events = {
        "view",
        "addtocart",
        "transaction",
    }

    invalid_events = set(df["event"].unique()) - valid_events

    if invalid_events:
        raise ValueError(
            f"Unknown event types: {invalid_events}"
        )

    # ⑥ 是否存在完全重复的数据
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicated rows."
        )

    return True