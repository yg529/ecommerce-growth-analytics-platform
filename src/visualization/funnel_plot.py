import plotly.graph_objects as go


def plot_funnel(funnel_dict, drop_off=None):
    """
    BI级 Funnel + Drop-off 标注
    """

    stages = list(funnel_dict.keys())
    values = list(funnel_dict.values())

    fig = go.Figure()

    # =========================
    # Funnel 主图
    # =========================
    fig.add_trace(
        go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            opacity=0.9,
            marker=dict(
                color="#4C78A8"
            )
        )
    )

    # =========================
    # Drop-off 标注（关键升级）
    # =========================
    if drop_off:

        annotations = []

        for i in range(len(stages) - 1):

            s1 = stages[i]
            s2 = stages[i + 1]

            if f"{s1}_to_{s2}" in drop_off:

                d = drop_off[f"{s1}_to_{s2}"]

                text = f"↓ {d['drop_rate']*100:.1f}% loss"

                annotations.append(
                    dict(
                        x=0.5,
                        y=i,
                        xref="paper",
                        yref="y",
                        text=text,
                        showarrow=False,
                        font=dict(
                            color="red" if d["drop_rate"] > 0.5 else "orange",
                            size=12
                        )
                    )
                )

        fig.update_layout(annotations=annotations)

    # =========================
    # Layout
    # =========================
    fig.update_layout(
        title="User Funnel with Drop-off Analysis",
        height=550,
        margin=dict(l=60, r=60, t=60, b=40)
    )

    return fig