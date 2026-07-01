from src.core.data_loader import load_clean_events
from src.analytics.retention import retention_analysis

df = load_clean_events()

matrix = retention_analysis(df)

assert matrix.iloc[:, 0].eq(1).all()

print("Retention tests passed.")