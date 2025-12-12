# Data Architecture Repository 

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Airflow](https://img.shields.io/badge/airflow-2.7-green)
![Databricks](https://img.shields.io/badge/databricks-DLT-red)
![ClickHouse](https://img.shields.io/badge/clickhouse-23.8-yellow)
![dbt](https://img.shields.io/badge/dbt-1.6-orange)

## Overview

This repository hosts a comprehensive collection of modern data architecture implementations, spanning from traditional machine learning to autonomous agents. It serves as a reference implementation for constructing scalable, production-grade data platforms.

## Key Features

### 📊 Machine Learning & Kaggle
*   **20 Complete Solutions**: Deep-dive implementations for diverse Kaggle competitions (Housing, Titanic, Store Sales, etc.).
*   **Production Code**: Includes `train.py` for model training and `eda.py` for exploratory analysis.
*   **Theory**: Detailed theoretical breakdowns and mathematical foundations in `THEORY.md`.

### 🏗️ Data Engineering
*   **Orchestration**: Domain-driven Airflow DAGs (Finance, Marketing, HR) with custom operators.
*   **Transformation**: Full dbt Core project with Marts, Snapshots, and Seeds.
*   **Database**: Robust SQL schemas for Staging, Archive, and Data Warehouse layers.

### 🚀 Big Data & Lakehouse
*   **Databricks**: Delta Live Tables (DLT) pipelines implementing Medallion Architecture (Bronze/Silver/Gold).
*   **Spark**: Scalable distributed data processing jobs.
*   **Connectors**: Object-oriented Ingestion connectors for 25+ APIs and Databases.

### ⚡ Real-Time Analytics
*   **ClickHouse**: OLAP schemas optimized for high-speed queries.
*   **Materialized Views**: Real-time aggregation logic.

### 🤖 Generative AI & Agents
*   **Prompt Engineering**: A business prompt library for various use cases.
*   **RAG**: Retrieval-Augmented Generation chains.
*   **Autonomous Agents**: Recursive Planner-Executor graph architectures.

## Repository Structure

```text
data-architecture-journey/
├── competitions/           # 20 Machine Learning Projects
├── src/
│   ├── agents/             # Agent logic, roles, and tools
│   ├── databricks/         # Delta Live Tables pipelines
│   ├── database/           # SQL DDLs for Staging and Data Warehouse
│   ├── elt/                # dbt Project (Models, Macros)
│   ├── genai/              # Prompt templates and LLM chains
│   ├── lakehouse/          # Ingestion connectors and Spark transformations
│   ├── olap/               # ClickHouse Schemas and Views
│   └── workflows/          # Airflow DAGs and custom plugins
├── tests/                  # Unit tests
└── README.md               # Project documentation
```

## Getting Started

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/thanhauco/data-architecture-journey.git
    cd data-architecture-journey
    ```

2.  **Explore**:
    *   Navigate to `competitions/` for ML projects.
    *   Check `src/` for the engineering components.

---
**Author**: Thanh Vu