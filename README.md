RetailRocket 增长分析平台
RetailRocket Growth Analytics Platform

# 项目简介
本项目基于 RetailRocket 电商用户行为数据集，构建一个端到端的用户增长分析与商业决策支持系统。
实现从 数据处理 → 指标体系 → 用户分析 → 可视化BI → 自动化报告输出 的完整数据分析闭环。
该项目模拟真实互联网公司增长分析场景，可用于产品、运营与数据分析决策支持。

# 项目亮点
1.企业级数据分析工程化结构（非Notebook）
2.完整用户增长分析体系（KPI / Funnel / Retention / RFM）
3.模块化设计（可扩展 analytics / metrics / visualization / pipeline）
4.Streamlit 交互式BI数据大屏
5.自动化分析流程（Pipeline一键运行）
6.自动生成业务分析报告（PDF）
7.内置业务洞察模块（Business Insight Engine）

# 技术栈
Python 3.11
Pandas / NumPy
Streamlit
Plotly / Matplotlib / Seaborn
Scikit-learn（用户分群）
ReportLab（PDF报告生成）

# 项目结构
data-analysis-retailrocket/
│
├── 4_app/                 # Streamlit 可视化大屏
├── src/                   # 核心分析代码
│   ├── core/              # 数据加载 / 配置 / 工具
│   ├── preprocessing/     # 数据清洗
│   ├── metrics/           # KPI指标体系
│   ├── analytics/         # 核心分析模块
│   ├── visualization/     # 可视化模块
│   ├── insights/          # 业务洞察
│
├── 5_pipeline/            # 自动化流程
├── 1_data/                # 原始数据
├── 6_outputs/             # 输出结果（图表/报告）
├── tests/                 # 单元测试
├── requirements.txt
├── run.bat
└── README.md

# 核心功能模块
1️.KPI指标体系
UV / PV
购买用户数
转化率
加购率
2️.漏斗分析（Funnel Analysis）
View → Add to Cart → Purchase
转化率计算
流失分析
3️.留存分析（Retention Analysis）
Cohort留存矩阵
留存热力图
用户生命周期分析
4️.RFM用户分层
Recency / Frequency / Monetary
用户价值分层（高价值 / 沉睡 / 流失用户）
5️.商品分析（Item Analysis）
热门商品排行
高转化商品
商品行为分析
6️.BI数据大屏
KPI总览
Funnel可视化
留存热力图
RFM用户分群
7️.自动化报告系统
自动生成业务分析报告
支持PDF导出
一键下载
8.商业价值

本项目模拟真实电商增长分析场景，可用于：

用户增长分析
电商运营决策支持
产品优化分析
数据驱动业务决策
用户流失分析
项目运行方式
1️.安装依赖
pip install -r requirements.txt
2️.启动项目
streamlit run 4_app/app.py
或一键启动
run.bat

# 项目定位
本项目定位为：企业级电商用户增长分析平台（Growth Analytics System）
适用于：
数据分析岗位（校招 / 实习 / 初级）
产品分析岗位
数据科学入门项目展示

# 作者说明
本项目用于数据分析能力展示，涵盖数据处理、指标体系构建、用户行为分析及商业洞察生成的完整流程。