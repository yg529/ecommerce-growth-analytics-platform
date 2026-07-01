# RetailRocket Growth Analytics Platform

基于 RetailRocket 电商用户行为数据集的增长分析项目，覆盖数据清洗、KPI 总览、转化漏斗、Cohort 留存、RFM 用户分层、商品转化分析、Streamlit Dashboard 和自动化 Markdown/PDF 报告。

这个项目适合作为数据分析、产品分析、商业分析实习/初级岗位的作品集项目。当前重点是可复现的数据分析流程和可解释的业务指标，不定位为生产级系统。

## 功能状态

| 模块 | 状态 | 说明 |
| --- | --- | --- |
| 数据清洗 | 已完成 | 读取 `events.csv`，完成时间转换、去重、缺失值处理、事件标准化和排序 |
| KPI 总览 | 已完成 | UV、事件数、商品数、购买用户数、购买转化率 |
| 漏斗分析 | 已完成 | 按用户行为顺序计算 View -> Add to Cart -> Transaction |
| 留存分析 | 已完成 | Cohort 留存矩阵和热力图 |
| RFM 分析 | 已完成 | RetailRocket 没有金额字段，Monetary 使用交易次数代理 |
| 商品分析 | 已完成 | 商品浏览、加购、购买、转化率和分层 |
| Streamlit Dashboard | 已完成 | 多模块交互式看板 |
| 自动报告 | 已完成 | 输出 Markdown，并导出基础 PDF |
| 类目分析 / 路径分析 | 未完成 | 数据集包含相关数据，但当前版本未纳入主流程 |

## 数据来源

数据集：RetailRocket Ecommerce Dataset  
下载地址：https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

当前仓库不提交原始数据和清洗后数据。下载后请放置：

```text
1_data/
  raw/
    events.csv
```

## 快速开始

```powershell
py -m pip install -r requirements.txt
py src/preprocessing/clean_events.py
py -m streamlit run 4_app/app.py
```

清洗脚本会生成：

```text
1_data/
  processed/
    events_clean.csv
```

## 运行测试

```powershell
py -m pytest
```

测试使用小型内存样本，不依赖本地 Kaggle 数据文件。

## 项目结构

```text
.
├── 2_notebooks/          # 探索和结果展示
├── 4_app/                # Streamlit Dashboard
├── src/
│   ├── analytics/        # 漏斗、留存、RFM、商品分析
│   ├── core/             # 配置、数据加载、校验、日志
│   ├── insights/         # 规则化业务洞察
│   ├── pipeline/         # Dashboard 内的一键分析流程
│   ├── preprocessing/    # 数据清洗
│   ├── report/           # Markdown/PDF 报告
│   └── visualization/    # 图表函数
├── tests/                # pytest 单元测试
├── requirements.txt
└── README.md
```

## 简历表述建议

可以写：

> 基于 RetailRocket 用户行为数据构建电商增长分析 Dashboard，完成数据清洗、KPI 指标、转化漏斗、Cohort 留存、RFM 用户分层和商品转化分析，并通过 Streamlit 输出交互式看板与自动化分析报告。

不建议写“企业级平台”或“生产级 BI 系统”，除非后续补充部署、权限、调度、监控和数据仓库层。

## 已知限制

- RetailRocket 数据没有订单金额字段，因此 RFM 的 Monetary 使用交易次数代理。
- PDF 报告是基础文本导出，不包含完整图表排版。
- 当前主流程只使用 `events.csv`，尚未整合 `item_properties.csv` 和 `category_tree.csv`。
- Dashboard 依赖本地清洗后的 `events_clean.csv`，首次运行前必须先执行清洗脚本。
