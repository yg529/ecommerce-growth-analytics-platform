# DUA
import pandas as pd

def compute_dau(df):
    df = df.copy()
    df["date"] = df["timestamp"].dt.date

    dau = df.groupby("date")["visitorid"].nunique().reset_index()
    dau.columns = ["date", "dau"]

    return dau

# 用户行为分布
def user_activity_longtail(df):
    user_cnt = df.groupby("visitorid").size().sort_values(ascending=False)

    return user_cnt

# 用户分层
def user_segmentation(df):
    user_cnt = df.groupby("visitorid").size()

    def label(x):
        if x <= 3:
            return "low_active"
        elif x <= 20:
            return "mid_active"
        else:
            return "high_active"

    segments = user_cnt.apply(label).value_counts()

    return segments

# 行为结构分析
def event_distribution(df):
    return df["event"].value_counts(normalize=True)

# 用户 TOP 分析
def top_users(df, n=10):
    return df["visitorid"].value_counts().head(n)

# 主函数
def user_behavior_analysis(df):
    result = {}

    result["dau"] = compute_dau(df)
    result["user_distribution"] = user_activity_longtail(df)
    result["segments"] = user_segmentation(df)
    result["event_ratio"] = event_distribution(df)
    result["top_users"] = top_users(df)

    return result