from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_FILE = PROJECT_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
CHARTS_DIR = PROJECT_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE, parse_dates=["OrderDate"])
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
region = df.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
category = df.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
monthly = df.groupby("Month", as_index=False)["Revenue"].sum()
q1, q3 = df["Revenue"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["Revenue"] < lower) | (df["Revenue"] > upper)].copy()

for name, data in [("revenue_by_region", region), ("revenue_by_category", category),
                   ("monthly_revenue", monthly), ("potential_outliers", outliers)]:
    data.to_csv(OUTPUT_DIR / f"{name}.csv", index=False, date_format="%Y-%m-%d")

fig, ax = plt.subplots(figsize=(9, 5)); ax.bar(region["Region"], region["Revenue"])
ax.set(title="Total Revenue by Region", xlabel="Region", ylabel="Revenue"); fig.tight_layout()
fig.savefig(CHARTS_DIR / "revenue_by_region.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5)); ax.plot(monthly["Month"], monthly["Revenue"], marker="o")
ax.set(title="Monthly Revenue Trend", xlabel="Month", ylabel="Revenue"); ax.tick_params(axis="x", rotation=45)
fig.tight_layout(); fig.savefig(CHARTS_DIR / "monthly_revenue_trend.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5)); ax.bar(category["Category"], category["Revenue"])
ax.set(title="Total Revenue by Product Category", xlabel="Category", ylabel="Revenue"); fig.tight_layout()
fig.savefig(CHARTS_DIR / "revenue_by_category.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5)); ax.hist(df["Revenue"], bins=12)
ax.set(title="Distribution of Order Revenue", xlabel="Revenue", ylabel="Number of Orders"); fig.tight_layout()
fig.savefig(CHARTS_DIR / "revenue_distribution.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5))
for label, part in df.groupby("Category"): ax.scatter(part["Quantity"], part["Revenue"], label=label)
ax.set(title="Order Quantity vs Revenue", xlabel="Quantity", ylabel="Revenue"); ax.legend(); fig.tight_layout()
fig.savefig(CHARTS_DIR / "quantity_vs_revenue.png", dpi=150); plt.close(fig)

print("Dataset shape:", df.shape)
print("Total revenue:", round(df["Revenue"].sum(), 2))
print("\nRevenue by region:\n", region.to_string(index=False))
print("\nRevenue by category:\n", category.to_string(index=False))
print("\nPotential outliers:\n", outliers[["OrderDate", "Region", "Product", "Revenue"]].to_string(index=False))
print("\nSaved charts in charts/ and summary CSV files in output/.")
