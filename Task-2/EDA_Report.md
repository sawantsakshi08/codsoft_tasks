# Task 2 — Exploratory Data Analysis Report

## Objective
Explore a sample retail sales dataset using descriptive statistics, trend analysis, relationships, visualizations, and potential outlier detection.

## Dataset overview
- Number of records: **39**
- Revenue is calculated as `Quantity × UnitPrice`.
- Total recorded revenue: **₹2,483,500.00** (illustrative currency for practice data).

## Key findings
- **Highest-revenue region:** North — ₹684,200.00.
- **Highest-revenue category:** Electronics — ₹1,809,000.00.
- Monthly revenue is summarized in `output/monthly_revenue.csv` and shown in `charts/monthly_revenue_trend.png`.
- IQR screening flagged **2** potential unusual record(s). An outlier is not automatically an error and should be checked in context.

## Charts included
Revenue by region, monthly revenue trend, revenue by category, revenue distribution, and quantity versus revenue.

## Recommendations
- Compare revenue with order count and profit before making business decisions.
- Investigate unusually high order values to check whether they are genuine.
- Review monthly changes alongside promotions and stock availability before drawing conclusions.

## Limitations
This is synthetic practice data, not real company sales. Results demonstrate EDA methods only.
