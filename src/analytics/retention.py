import pandas as pd
from src.core.validation import validate_events

# 准备数据
def prepare_retention_data(df):
    """
    数据准备
    """

    validate_events(df)

    df = df.copy()

    df["date"] = df["timestamp"].dt.normalize()

    return df

# 计算每个用户的首次访问日期
def build_cohort(df):
    """
    获取每个用户首次访问日期
    """

    first_visit = (
        df.groupby("visitorid")["date"]
          .min()
          .rename("cohort_date")
    )

    return first_visit

# 把首次访问日期合并回原始数据
def add_cohort(df):
    """
    给每条行为增加 cohort_date
    """

    first_visit = build_cohort(df)

    df = df.merge(
        first_visit,
        on="visitorid",
        how="left"
    )

    return df

# 计算留存天数
def calculate_retention_day(df):
    """
    计算距离首次访问多少天
    """

    df["retention_day"] = (
        df["date"] - df["cohort_date"]
    ).dt.days
    df = df[
        df["retention_day"] >= 0
        ]

    return df

# 去重
def deduplicate_daily_user(df):
    """
    每个用户每天只保留一条记录
    """

    return df.drop_duplicates(
        subset=[
            "visitorid",
            "cohort_date",
            "retention_day"
        ]
    )

# 统计每天回来多少用户
def build_retention_count(df):
    """
    统计各 Cohort 每天留存人数
    """

    retention = (
        df.groupby(
            ["cohort_date", "retention_day"]
        )["visitorid"]
        .nunique()
        .reset_index(name="users")
    )

    return retention

# 计算 Cohort
def cohort_size(retention):
    """
    每个 Cohort 的初始用户数
    """

    cohort = (
        retention[
            retention["retention_day"] == 0
        ][
            ["cohort_date", "users"]
        ]
        .rename(columns={
            "users": "cohort_size"
        })
    )

    return cohort

# 计算留存率
def calculate_retention_rate(retention):
    """
    计算留存率
    """

    cohort = cohort_size(retention)

    retention = retention.merge(
        cohort,
        on="cohort_date"
    )

    retention["retention_rate"] = (
        retention["users"]
        / retention["cohort_size"]
    )

    return retention

# 生成矩阵
def build_retention_matrix(retention):
    """
    生成留存矩阵
    """
    matrix = (
        retention
        .pivot(
            index="cohort_date",
            columns="retention_day",
            values="retention_rate"
        )
        .fillna(0)
    )

    return matrix

# 封装
def retention_analysis(
    df,
    max_day=30
):
    """
    留存分析主函数
    """
    validate_events(df)

    df = prepare_retention_data(df)

    df = add_cohort(df)

    df = calculate_retention_day(df)

    df = deduplicate_daily_user(df)

    retention = build_retention_count(df)

    retention = calculate_retention_rate(retention)
    retention = retention[
        retention["retention_day"] <= max_day
        ]

    matrix = build_retention_matrix(retention)

    matrix.index.name = "cohort_date"

    matrix.columns.name = "day"

    return matrix