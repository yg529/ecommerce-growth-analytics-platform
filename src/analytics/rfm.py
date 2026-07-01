import numpy as np
import pandas as pd


RFM_COLUMNS = [
    "visitorid",
    "recency",
    "frequency",
    "monetary",
    "R_score",
    "F_score",
    "M_score",
    "RFM_score",
    "segment",
]


def prepare_rfm_data(df: pd.DataFrame) -> pd.DataFrame:
    """Keep transaction events and add a proxy amount column."""
    transactions = df[df["event"] == "transaction"].copy()

    if transactions.empty:
        return transactions.assign(amount=pd.Series(dtype="int64"))

    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

    # RetailRocket has no transaction amount. Count each purchase as one unit.
    transactions["amount"] = 1
    return transactions


def build_rfm(
    df: pd.DataFrame,
    reference_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Build recency, frequency and monetary proxy metrics."""
    if df.empty:
        return pd.DataFrame(columns=["visitorid", "recency", "frequency", "monetary"])

    if reference_date is None:
        reference_date = df["timestamp"].max()

    return (
        df.groupby("visitorid")
        .agg(
            recency=("timestamp", lambda x: (reference_date - x.max()).days),
            frequency=("visitorid", "count"),
            monetary=("amount", "sum"),
        )
        .reset_index()
    )


def _quantile_score(series: pd.Series, higher_is_better: bool) -> pd.Series:
    """Return a robust 1-5 score for small or highly duplicated samples."""
    if series.empty:
        return pd.Series(dtype="int64")

    if series.nunique(dropna=True) <= 1:
        return pd.Series(np.full(len(series), 3), index=series.index, dtype="int64")

    ranks = series.rank(method="first", ascending=True)
    bins = min(5, len(series))
    raw = pd.qcut(ranks, q=bins, labels=False, duplicates="drop") + 1

    max_raw = int(raw.max())
    if max_raw <= 1:
        score = pd.Series(np.full(len(series), 3), index=series.index)
    else:
        score = 1 + ((raw - 1) * 4 / (max_raw - 1)).round()

    score = score.astype("int64")
    if not higher_is_better:
        score = 6 - score

    return score


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """Score R, F and M on a 1-5 scale."""
    if rfm.empty:
        return pd.DataFrame(columns=RFM_COLUMNS)

    scored = rfm.copy()
    scored["R_score"] = _quantile_score(scored["recency"], higher_is_better=False)
    scored["F_score"] = _quantile_score(scored["frequency"], higher_is_better=True)
    scored["M_score"] = _quantile_score(scored["monetary"], higher_is_better=True)
    scored["RFM_score"] = (
        scored["R_score"] + scored["F_score"] + scored["M_score"]
    )
    return scored


def segment_users(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign coarse user value segments from RFM score."""
    if rfm.empty:
        return pd.DataFrame(columns=RFM_COLUMNS)

    segmented = rfm.copy()

    def label(row: pd.Series) -> str:
        if row["RFM_score"] >= 12:
            return "Champions"
        if row["RFM_score"] >= 9:
            return "Loyal Users"
        if row["RFM_score"] >= 6:
            return "Potential Users"
        return "At Risk"

    segmented["segment"] = segmented.apply(label, axis=1)
    return segmented


def rfm_analysis(df: pd.DataFrame) -> dict:
    """Run RFM analysis using transaction count as the monetary proxy."""
    transactions = prepare_rfm_data(df)
    rfm = build_rfm(transactions)
    rfm = score_rfm(rfm)
    rfm = segment_users(rfm)

    return {
        "rfm_table": rfm,
        "summary": rfm["segment"].value_counts().to_dict() if not rfm.empty else {},
        "monetary_note": "RetailRocket has no amount field; monetary uses transaction count.",
    }
