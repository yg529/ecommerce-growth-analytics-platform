import plotly.graph_objects as go


def plot_funnel(funnel_dict: dict, drop_off: dict | None = None):
    """Create a Plotly funnel chart with drop-off annotations."""
    stages = list(funnel_dict.keys())
    values = list(funnel_dict.values())

    fig = go.Figure()
    fig.add_trace(
        go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            opacity=0.9,
            marker={"color": "#4C78A8"},
        )
    )

    if drop_off:
        annotations = []
        for index in range(len(stages) - 1):
            current_stage = stages[index]
            next_stage = stages[index + 1]
            key = f"{current_stage}_to_{next_stage}"

            if key in drop_off:
                item = drop_off[key]
                annotations.append(
                    {
                        "x": 0.5,
                        "y": index,
                        "xref": "paper",
                        "yref": "y",
                        "text": f"drop {item['drop_rate'] * 100:.1f}%",
                        "showarrow": False,
                        "font": {
                            "color": "red" if item["drop_rate"] > 0.5 else "orange",
                            "size": 12,
                        },
                    }
                )
        fig.update_layout(annotations=annotations)

    fig.update_layout(
        title="User Funnel with Drop-off Analysis",
        height=550,
        margin={"l": 60, "r": 60, "t": 60, "b": 40},
    )
    return fig
