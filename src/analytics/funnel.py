def reached_stage(events, stages):
    """
    判断用户是否按顺序完成指定阶段
    """
    stage_index = 0

    for event in events:
        def reached_stage(events, stages):
            stage_index = 0

            for event in events:
                if event == stages[stage_index]:
                    stage_index += 1

                    if stage_index == len(stages):
                        return True

            return False

        if event == stages[stage_index]:
            stage_index += 1

    return stage_index == len(stages)


# 生成行为序列
def build_user_sequence(df):
    return (
        df
        .sort_values(["visitorid", "timestamp"])
        .groupby("visitorid")["event"]
        .apply(list)
    )


# 统计漏斗
def build_funnel(user_sequences, stages):
    """
    stages: 例如 ["view", "addtocart", "transaction"]
    """

    funnel = {}

    for i in range(len(stages)):
        current_stages = stages[: i + 1]

        count = 0

        for events in user_sequences:
            if reached_stage(events, current_stages):
                count += 1

        funnel[current_stages[-1]] = count

    return funnel


# 计算转化率
def compute_conversion_rate(funnel):
    stages = list(funnel.keys())

    result = {}

    for i in range(len(stages) - 1):
        current = funnel[stages[i]]
        nxt = funnel[stages[i + 1]]

        result[f"{stages[i]}_to_{stages[i+1]}"] = (
            nxt / current if current else 0
        )

    result[f"{stages[0]}_to_{stages[-1]}"] = (
        funnel[stages[-1]] / funnel[stages[0]]
        if funnel[stages[0]] else 0
    )

    return result


# 主函数
def funnel_analysis(df, stages=["view", "addtocart", "transaction"]):

    sequences = build_user_sequence(df)

    # 清洗空序列
    sequences = [s for s in sequences if len(s) > 0]

    # funnel count
    funnel = build_funnel(sequences, stages)

    # conversion rate
    rates = compute_conversion_rate(funnel)

    # =========================
    # 计算
    # =========================
    drop_off = {}

    stage_names = list(funnel.keys())

    for i in range(len(stage_names) - 1):
        current = stage_names[i]
        nxt = stage_names[i + 1]

        drop = funnel[current] - funnel[nxt]
        drop_rate = drop / funnel[current] if funnel[current] else 0

        drop_off[f"{current}_to_{nxt}"] = {
            "drop_users": int(drop),
            "drop_rate": round(drop_rate, 4)
        }

    # =========================
    # 自动洞察
    # =========================
    insights = []

    for k, v in drop_off.items():
        if v["drop_rate"] > 0.9:
            insights.append(f"{k} 流失严重（>{v['drop_rate']*100:.1f}%）")
        elif v["drop_rate"] > 0.5:
            insights.append(f"{k} 有明显流失")

    return {
        "funnel": funnel,
        "conversion_rate": rates,
        "drop_off": drop_off,
        "insights": insights
    }