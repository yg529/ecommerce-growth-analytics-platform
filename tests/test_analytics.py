import pandas as pd

from src.analytics.funnel import funnel_analysis
from src.analytics.item_analysis import classify_items
from src.analytics.retention import retention_analysis
from src.analytics.rfm import rfm_analysis


def sample_events():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-01 00:05:00",
                    "2024-01-01 00:10:00",
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-01-01",
                ],
                format="mixed",
            ),
            "visitorid": [1, 1, 1, 2, 2, 2, 3],
            "event": [
                "view",
                "addtocart",
                "transaction",
                "view",
                "view",
                "transaction",
                "view",
            ],
            "itemid": [10, 10, 10, 20, 20, 20, 30],
            "transactionid": [None, None, 1001, None, None, 1002, None],
        }
    )


def test_funnel_counts_ordered_stages():
    result = funnel_analysis(sample_events())

    assert result["funnel"] == {
        "view": 3,
        "addtocart": 1,
        "transaction": 1,
    }
    assert result["conversion_rate"]["view_to_addtocart"] == 1 / 3
    assert result["conversion_rate"]["view_to_cart"] == 1 / 3


def test_retention_matrix_day_zero_is_one():
    matrix = retention_analysis(sample_events(), max_day=3)

    assert not matrix.empty
    assert matrix[0].eq(1).all()


def test_rfm_handles_missing_amount_and_segments_buyers():
    result = rfm_analysis(sample_events())

    assert result["summary"]
    assert set(["recency", "frequency", "monetary", "segment"]).issubset(
        result["rfm_table"].columns
    )
    assert result["rfm_table"]["monetary"].min() == 1


def test_item_classification_has_finite_conversion():
    seg = classify_items(sample_events())

    assert set(seg["category"]).issubset({"high_value", "potential", "long_tail"})
    assert seg["view_to_buy"].notna().all()
    assert seg["view_to_buy"].replace([float("inf"), float("-inf")], pd.NA).notna().all()
