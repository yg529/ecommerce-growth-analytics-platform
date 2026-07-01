import pandas as pd
import numpy as np


def prepare_rfm_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    过滤交易数据并准备RFM分析数据
    """

    df = df.copy()

    # 只保留交易
    df = df[df["event"] == "transaction"]

    # 时间转换（防止没转）
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 金额字段（RetailRocket没有直接金额，用1代替行为价值）
    df["amount"] = 1

    return df


def build_rfm(df: pd.DataFrame, reference_date=None) -> pd.DataFrame:
    """
    构建 RFM 表
    """

    if reference_date is None:
        reference_date = df["timestamp"].max()

    rfm = df.groupby("visitorid").agg(
        recency=("timestamp", lambda x: (reference_date - x.max()).days),
        frequency=("visitorid", "count"),
        monetary=("amount", "sum")
    ).reset_index()

    return rfm


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    给RFM打分（1-5分）
    """

    rfm = rfm.copy()

    # R 越小越好
    rfm["R_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1])

    # F 越大越好
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])

    # M 越大越好
    rfm["M_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])

    rfm["RFM_score"] = (
        rfm["R_score"].astype(int) +
        rfm["F_score"].astype(int) +
        rfm["M_score"].astype(int)
    )

    return rfm


def segment_users(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    用户分层
    """

    def label(row):
        if row["RFM_score"] >= 12:
            return "Champions"
        elif row["RFM_score"] >= 9:
            return "Loyal Users"
        elif row["RFM_score"] >= 6:
            return "Potential Users"
        else:
            return "At Risk"

    rfm["segment"] = rfm.apply(label, axis=1)

    return rfm


def rfm_analysis(df: pd.DataFrame) -> dict:
    """
    RFM 主流程
    """

    df = prepare_rfm_data(df)

    rfm = build_rfm(df)

    rfm = score_rfm(rfm)

    rfm = segment_users(rfm)

    summary = rfm["segment"].value_counts().to_dict()

    return {
        "rfm_table": rfm,
        "summary": summary
    }