# RetailRocket Growth Analytics Platform

## Project Spec（项目开发文档）

---

# 一、项目目标

构建一个基于 RetailRocket 电商用户行为数据集的数据分析平台。

本项目不仅完成传统的数据分析，还按照企业数据分析项目标准完成：

* 数据清洗（Data Cleaning）
* 指标体系（KPI）
* 用户行为分析（User Behavior）
* 漏斗分析（Funnel）
* 留存分析（Retention）
* 用户价值分析（RFM）
* 商品分析（Item Analysis）
* 类目分析（Category Analysis）
* 业务洞察（Business Insights）
* Streamlit 可视化平台
* 自动化 Pipeline
* 单元测试
* GitHub 展示
* 简历包装

最终目标：

**达到互联网数据分析岗位（校招 / 初中级）项目标准。**

---

# 二、数据来源

RetailRocket Ecommerce Dataset

https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

主要数据：

events.csv

item_properties.csv

category_tree.csv

数据规模：

* 约275万条用户行为数据
* 约140万浏览行为
* 数万加购行为
* 数万交易行为

---

# 三、项目目录

```
data-analysis-retailrocket/

├── 1_data/
│
├── 2_notebooks/
│
├── src/
│      ├── core/
│      ├── preprocessing/
│      ├── analytics/
│      ├── metrics/
│      ├── visualization/
│      ├── insights/
│
├── tests/
│
├── 4_app/
│
├── 5_pipeline/
│
├── 6_outputs/
│
├── README.md
│
└── PROJECT_SPEC.md
```

---

# 四、开发规范

遵循企业开发流程：

```
Data

↓

Preprocessing

↓

Analytics

↓

Visualization

↓

Insights

↓

Outputs

↓

Dashboard
```

Notebook 不写业务逻辑。

Notebook 只负责：

* 调用分析模块
* 展示结果
* 简单实验

所有业务代码统一放入 src。

---

# 五、模块规范

每个 Analytics 模块统一采用如下结构：

```
prepare_data()

↓

calculate_xxx()

↓

build_xxx()

↓

analysis()
```

例如：

Retention

```
prepare_data()

↓

build_cohort()

↓

calculate_retention()

↓

build_matrix()

↓

retention_analysis()
```

所有模块保持统一风格。

---

# 六、已完成模块

## ① 项目结构

完成。

采用模块化开发。

---

## ② Config

完成。

统一管理：

* 数据目录
* 输出目录
* Funnel Stage
* Path

---

## ③ Data Loader

完成。

统一读取：

* Raw Data
* Processed Data

自动转换：

timestamp → datetime

Notebook 禁止直接 read_csv。

---

## ④ 数据清洗

完成。

包括：

* 时间转换
* 去重
* 缺失值处理
* Event 标准化
* 排序

输出：

events_clean.csv

---

## ⑤ KPI 指标体系

完成。

定义：

* PV
* UV
* 加购率
* 转化率
* 下单用户数

统一管理指标计算。

---

## ⑥ 用户行为分析

完成。

包括：

* 行为数量
* 行为占比
* 用户行为统计

---

## ⑦ Funnel

完成。

包括：

浏览

↓

加购

↓

成交

计算：

* View → Cart
* Cart → Buy
* View → Buy

完成可视化。

---

## ⑧ Retention

完成基础版本。

已实现：

* Cohort
* 留存矩阵

待完成：

* Heatmap
* Business Insight

---

# 七、待开发模块

按照下面顺序完成。

---

## Phase 2

### Retention Heatmap

输出：

retention_heatmap.png

---

### RFM 用户价值分析

包括：

Recency

Frequency

Monetary

用户价值分层。

---

### Item Analysis

包括：

Top 商品

热门商品

成交商品

转化商品

---

### Category Analysis

包括：

一级类目

类目贡献

类目转化率

---

### Business Insight

自动生成：

业务分析结论。

例如：

Day1 留存偏低。

建议：

优化首日激活。

---

## Phase 3

工程化。

包括：

Pipeline

Logger

Tests

Dashboard

---

## Phase 4

项目交付。

包括：

README

GitHub

Demo

简历包装

模拟面试

---

# 八、代码规范

统一：

PEP8

统一命名：

snake_case

所有函数：

必须写 Docstring。

所有模块：

必须写注释。

禁止 Notebook 中出现大量业务逻辑。

---

# 九、开发原则

项目目标：

不是完成 Notebook。

而是完成一个：

**企业级数据分析项目。**

所有开发遵循：

可维护

可扩展

可复用

模块化

工程化

业务导向

---

# 十、当前开发进度

```
██████████████████████████████

EDA                       ✅

Cleaning                  ✅

KPI                       ✅

User Behavior             ✅

Funnel                    ✅

Retention                 🚧

Retention Heatmap         ⬜

RFM                       ⬜

Item Analysis             ⬜

Category Analysis         ⬜

Business Insight          ⬜

Pipeline                  ⬜

Dashboard                 ⬜

README                    ⬜

Resume                    ⬜
```

---

# 十一、最终项目定位

项目名称：

**RetailRocket Growth Analytics Platform**

定位：

企业级电商用户增长分析平台。

项目能力覆盖：

* Python
* Pandas
* 数据清洗
* KPI体系
* 漏斗分析
* 留存分析
* 用户价值分析
* 商品分析
* 可视化
* Streamlit Dashboard
* 自动化 Pipeline
* GitHub 工程化开发

目标：

作为数据分析岗位核心项目，用于：

* 校招
* 实习
* 初中级数据分析岗位面试
