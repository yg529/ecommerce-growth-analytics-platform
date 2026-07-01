from pathlib import Path

# 项目根目录（自动定位）
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "1_data"
RAW_DATA_PATH = DATA_DIR / "raw" / "events.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed"

# 输出目录
OUTPUT_DIR = BASE_DIR / "6_outputs"

FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"

REPORT_DIR = OUTPUT_DIR / "reports"