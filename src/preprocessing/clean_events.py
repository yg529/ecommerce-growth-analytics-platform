import pandas as pd
import os

# 读取数据 + 统一字段
def load_raw_events(path):
    df = pd.read_csv(path)
    df.columns = ["timestamp", "visitorid", "event", "itemid", "transactionid"]
    return df


# 时间字段转换
def convert_time(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


# 去重
def drop_duplicates(df):
    return df.drop_duplicates()


# 处理缺失值
def handle_missing(df):
    return df.dropna(subset=["visitorid", "event", "itemid"])


# event标准化
def normalize_event(df):
    df["event"] = df["event"].str.lower()
    valid_events = ["view", "addtocart", "transaction"]
    return df[df["event"].isin(valid_events)]


# 排序
def sort_events(df):
    return df.sort_values(["visitorid", "timestamp"])


# 主清洗流程
def clean_events(path):
    df = load_raw_events(path)
    df = convert_time(df)
    df = drop_duplicates(df)
    df = handle_missing(df)
    df = normalize_event(df)
    df = sort_events(df)
    return df


# 保存
def save_clean(df, output_path):
    # 自动创建目录（关键）
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)


# pipeline入口
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_path = os.path.join(BASE_DIR, "1_data", "raw", "events.csv")
    PROCESSED_PATH = "1_data/processed"
    output_path = os.path.join(BASE_DIR, "1_data", "processed", "events_clean.csv")

    df = clean_events(raw_path)
    save_clean(df, output_path)

    print("cleaning done:", df.shape)