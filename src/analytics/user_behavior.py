import pandas as pd


def compute_dau(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.copy()
    daily["date"] = daily["timestamp"].dt.date
    dau = daily.groupby("date")["visitorid"].nunique().reset_index()
    dau.columns = ["date", "dau"]
    return dau


def user_activity_longtail(df: pd.DataFrame) -> pd.Series:
    return df.groupby("visitorid").size().sort_values(ascending=False)


def user_segmentation(df: pd.DataFrame) -> pd.Series:
    user_counts = df.groupby("visitorid").size()

    def label(count: int) -> str:
        if count <= 3:
            return "low_active"
        if count <= 20:
            return "mid_active"
        return "high_active"

    return user_counts.apply(label).value_counts()


def event_distribution(df: pd.DataFrame) -> pd.Series:
    return df["event"].value_counts(normalize=True)


def top_users(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df["visitorid"].value_counts().head(n)


def user_behavior_analysis(df: pd.DataFrame) -> dict:
    return {
        "dau": compute_dau(df),
        "user_distribution": user_activity_longtail(df),
        "segments": user_segmentation(df),
        "event_ratio": event_distribution(df),
        "top_users": top_users(df),
    }
