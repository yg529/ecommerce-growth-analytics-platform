from collections.abc import Iterable

import pandas as pd


DEFAULT_STAGES = ["view", "addtocart", "transaction"]
RATE_ALIASES = {
    "view_to_addtocart": "view_to_cart",
    "addtocart_to_transaction": "cart_to_buy",
    "view_to_transaction": "view_to_buy",
}


def reached_stage(events: Iterable[str], stages: list[str]) -> bool:
    """Return True when the event sequence reaches every stage in order."""
    if not stages:
        return True

    stage_index = 0

    for event in events:
        if event == stages[stage_index]:
            stage_index += 1
            if stage_index == len(stages):
                return True

    return False


def build_user_sequence(df: pd.DataFrame) -> pd.Series:
    """Build ordered event sequences for each visitor."""
    return (
        df.sort_values(["visitorid", "timestamp"])
        .groupby("visitorid")["event"]
        .apply(list)
    )


def build_funnel(user_sequences: Iterable[list[str]], stages: list[str]) -> dict:
    """Count users who reached each funnel stage in order."""
    funnel = {}

    for index, stage in enumerate(stages):
        current_stages = stages[: index + 1]
        funnel[stage] = sum(
            reached_stage(events, current_stages)
            for events in user_sequences
        )

    return funnel


def compute_conversion_rate(funnel: dict) -> dict:
    """Calculate step and end-to-end conversion rates."""
    stages = list(funnel.keys())
    result = {}

    for index in range(len(stages) - 1):
        current_stage = stages[index]
        next_stage = stages[index + 1]
        current_count = funnel[current_stage]
        next_count = funnel[next_stage]
        key = f"{current_stage}_to_{next_stage}"
        result[key] = next_count / current_count if current_count else 0

    if len(stages) >= 2:
        first_stage = stages[0]
        last_stage = stages[-1]
        key = f"{first_stage}_to_{last_stage}"
        result[key] = (
            funnel[last_stage] / funnel[first_stage]
            if funnel[first_stage]
            else 0
        )

    for source_key, alias in RATE_ALIASES.items():
        if source_key in result:
            result[alias] = result[source_key]

    return result


def compute_drop_off(funnel: dict) -> dict:
    """Calculate user loss between adjacent funnel stages."""
    drop_off = {}
    stages = list(funnel.keys())

    for index in range(len(stages) - 1):
        current_stage = stages[index]
        next_stage = stages[index + 1]
        current_count = funnel[current_stage]
        next_count = funnel[next_stage]
        drop_users = current_count - next_count
        drop_rate = drop_users / current_count if current_count else 0

        drop_off[f"{current_stage}_to_{next_stage}"] = {
            "drop_users": int(drop_users),
            "drop_rate": round(drop_rate, 4),
        }

    return drop_off


def build_funnel_insights(drop_off: dict) -> list[str]:
    """Generate lightweight rule-based funnel comments."""
    insights = []

    for key, value in drop_off.items():
        drop_rate = value["drop_rate"]
        if drop_rate > 0.9:
            insights.append(f"{key} has severe drop-off ({drop_rate:.1%}).")
        elif drop_rate > 0.5:
            insights.append(f"{key} has meaningful drop-off.")

    return insights


def funnel_analysis(
    df: pd.DataFrame,
    stages: list[str] | None = None,
) -> dict:
    """Run ordered user funnel analysis."""
    stages = stages or DEFAULT_STAGES
    sequences = [
        sequence
        for sequence in build_user_sequence(df)
        if len(sequence) > 0
    ]

    funnel = build_funnel(sequences, stages)
    rates = compute_conversion_rate(funnel)
    drop_off = compute_drop_off(funnel)

    return {
        "funnel": funnel,
        "conversion_rate": rates,
        "drop_off": drop_off,
        "insights": build_funnel_insights(drop_off),
    }
