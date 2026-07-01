import pandas as pd

from src.preprocessing.clean_events import clean_events, save_clean


def test_clean_events_normalizes_and_sorts(tmp_path):
    raw_path = tmp_path / "events.csv"
    output_path = tmp_path / "processed" / "events_clean.csv"
    raw = pd.DataFrame(
        [
            [1704067200000, 2, "VIEW", 20, None],
            [1704067100000, 1, "view", 10, None],
            [1704067300000, 1, "bad_event", 10, None],
            [1704067200000, 2, "VIEW", 20, None],
            [1704067400000, None, "view", 30, None],
        ]
    )
    raw.to_csv(raw_path, index=False, header=False)

    cleaned = clean_events(raw_path)
    saved_path = save_clean(cleaned, output_path)

    assert saved_path.exists()
    assert cleaned["event"].tolist() == ["view", "view"]
    assert cleaned["visitorid"].tolist() == [1.0, 2.0]
    assert pd.api.types.is_datetime64_any_dtype(cleaned["timestamp"])
