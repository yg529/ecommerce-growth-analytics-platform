import pandas as pd

# 基础 KPI
def compute_basic_kpi(df):
    kpi = {}

    # 用户数
    kpi["uv"] = df["visitorid"].nunique()

    # 行为总量
    kpi["events"] = len(df)

    # 每用户行为数
    kpi["avg_events_per_user"] = kpi["events"] / kpi["uv"]

    return kpi

# DAU
def compute_dau(df):
    df = df.copy()
    df["date"] = df["timestamp"].dt.date

    dau = df.groupby("date")["visitorid"].nunique()

    return dau

# 转化率 CVR
def compute_cvr(df):
    users_view = set(df[df["event"] == "view"]["visitorid"])
    users_buy = set(df[df["event"] == "transaction"]["visitorid"])

    cvr = len(users_buy) / len(users_view) if len(users_view) > 0 else 0

    return cvr

# funnel KPI
def compute_funnel(df):
    view_users = set(df[df["event"] == "view"]["visitorid"])
    cart_users = set(df[df["event"] == "addtocart"]["visitorid"])
    buy_users = set(df[df["event"] == "transaction"]["visitorid"])

    funnel = {
        "view": len(view_users),
        "cart": len(cart_users),
        "buy": len(buy_users),

        "view_to_cart": len(cart_users) / len(view_users),
        "cart_to_buy": len(buy_users) / len(cart_users),
    }

    return funnel

# 商品 TOP 分析
def top_items(df, n=10):
    return df[df["event"] == "view"]["itemid"].value_counts().head(n)
