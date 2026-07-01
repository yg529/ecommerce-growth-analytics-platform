def build_overview(df):
    """
    Dashboard 总览指标
    """

    total_users = df["visitorid"].nunique()
    total_events = len(df)
    total_items = df["itemid"].nunique()

    buyers = df[df["event"] == "transaction"]["visitorid"].nunique()

    conversion_rate = buyers / total_users if total_users else 0

    overview = {
        "total_users": total_users,
        "total_events": total_events,
        "total_items": total_items,
        "buyers": buyers,
        "conversion_rate": round(conversion_rate, 6)
    }

    return overview