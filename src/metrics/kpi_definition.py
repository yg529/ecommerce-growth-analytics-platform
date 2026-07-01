import pandas as pd


def compute_basic_kpi(df: pd.DataFrame) -> dict:
    """Compute core traffic and buyer metrics."""
    uv = df["visitorid"].nunique()
    events = len(df)
    buyers = df.loc[df["event"] == "transaction", "visitorid"].nunique()

    return {
        "uv": uv,
        "events": events,
        "buyers": buyers,
        "avg_events_per_user": events / uv if uv else 0,
        "buyer_conversion_rate": buyers / uv if uv else 0,
    }


def compute_dau(df: pd.DataFrame) -> pd.Series:
    """Compute daily active users."""
    daily = df.copy()
    daily["date"] = daily["timestamp"].dt.date
    return daily.groupby("date")["visitorid"].nunique()


def compute_cvr(df: pd.DataFrame) -> float:
    """Compute buyer conversion rate among users with at least one view."""
    users_view = set(df.loc[df["event"] == "view", "visitorid"])
    users_buy = set(df.loc[df["event"] == "transaction", "visitorid"])
    return len(users_buy) / len(users_view) if users_view else 0


def compute_event_funnel(df: pd.DataFrame) -> dict:
    """Compute event-level user counts and simple set-based conversion rates."""
    view_users = set(df.loc[df["event"] == "view", "visitorid"])
    cart_users = set(df.loc[df["event"] == "addtocart", "visitorid"])
    buy_users = set(df.loc[df["event"] == "transaction", "visitorid"])

    return {
        "view": len(view_users),
        "cart": len(cart_users),
        "buy": len(buy_users),
        "view_to_cart": len(cart_users) / len(view_users) if view_users else 0,
        "cart_to_buy": len(buy_users) / len(cart_users) if cart_users else 0,
    }


def top_items(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Return top viewed items."""
    return df.loc[df["event"] == "view", "itemid"].value_counts().head(n)
