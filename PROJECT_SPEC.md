# Project Spec

## Objective

Build a reproducible growth analytics project for RetailRocket ecommerce behavior data.

The current version focuses on:

- Event data cleaning
- KPI overview
- Ordered user funnel analysis
- Cohort retention analysis
- RFM user segmentation
- Item conversion and segmentation
- Streamlit dashboard
- Markdown/PDF report generation
- Unit tests for core analytics logic

## Data

Dataset: RetailRocket Ecommerce Dataset  
Source: https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

Current pipeline uses `events.csv` only.

Expected local layout:

```text
1_data/
  raw/
    events.csv
  processed/
    events_clean.csv
```

Raw and processed data files are ignored by Git.

## Main Flow

```text
events.csv
  -> src/preprocessing/clean_events.py
  -> 1_data/processed/events_clean.csv
  -> analytics modules
  -> Streamlit dashboard / report output
```

## Implemented Modules

| Area | Module | Status |
| --- | --- | --- |
| Cleaning | `src/preprocessing/clean_events.py` | Done |
| Data loading | `src/core/data_loader.py` | Done |
| Validation | `src/core/validation.py` | Done |
| Overview KPI | `src/analytics/overview.py` | Done |
| Funnel | `src/analytics/funnel.py` | Done |
| Retention | `src/analytics/retention.py` | Done |
| RFM | `src/analytics/rfm.py` | Done |
| Item analysis | `src/analytics/item_analysis.py` | Done |
| Insights | `src/insights/business_insight.py` | Done |
| Dashboard | `4_app/app.py` | Done |
| Report | `src/report/` | Done |
| Tests | `tests/` | Done |

## Known Limitations

- Monetary in RFM is a transaction-count proxy because the dataset has no order amount.
- PDF export is a basic text report, not a designed BI report.
- Category and item-property analysis are not included in the current main flow.
- There is no scheduled orchestration, database layer or deployment configuration yet.

## Future Improvements

- Add category analysis using `category_tree.csv`.
- Use `item_properties.csv` to enrich item segmentation.
- Add screenshots and a small sampled dataset for demo purposes.
- Add CI with pytest.
- Add Streamlit Cloud deployment instructions.
