from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "data" / "sales_dashboard_data.csv")
OUT = ROOT / "output"
CHARTS = ROOT / "charts"
OUT.mkdir(exist_ok=True); CHARTS.mkdir(exist_ok=True)

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly = df.groupby("Month", as_index=False)["Sales"].sum()
monthly["Month"] = pd.Categorical(monthly["Month"], categories=months, ordered=True)
monthly = monthly.sort_values("Month")
region = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
category = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)

for name, table in [("monthly_sales", monthly), ("sales_by_region", region), ("sales_by_category", category)]:
    table.to_csv(OUT / f"{name}.csv", index=False)

def save_chart(filename, draw):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    draw(ax)
    fig.tight_layout()
    fig.savefig(CHARTS / filename, dpi=150)
    plt.close(fig)

save_chart("sales_by_region.png", lambda ax: (ax.bar(region["Region"], region["Sales"]), ax.set(title="Total Sales by Region", xlabel="Region", ylabel="Sales (₹)")))
save_chart("monthly_sales_trend.png", lambda ax: (ax.plot(monthly["Month"].astype(str), monthly["Sales"], marker="o"), ax.set(title="Monthly Sales Trend", xlabel="Month", ylabel="Sales (₹)")))
save_chart("sales_by_category.png", lambda ax: (ax.bar(category["Category"], category["Sales"]), ax.set(title="Sales by Product Category", xlabel="Category", ylabel="Sales (₹)")))

fig, ax = plt.subplots(figsize=(7, 4))
totals = df.groupby("Category")["Sales"].sum()
ax.pie(totals.values, labels=totals.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Category Share of Total Sales")
fig.tight_layout(); fig.savefig(CHARTS / "category_share_pie.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df["Sales"], bins=10, edgecolor="black")
ax.set(title="Distribution of Sales Records", xlabel="Sales (₹)", ylabel="Number of records")
fig.tight_layout(); fig.savefig(CHARTS / "sales_distribution.png", dpi=150); plt.close(fig)

print("Dataset shape:", df.shape)
print("Total sales:", int(df["Sales"].sum()))
print("\nSales by region:\n", region.to_string(index=False))
print("\nSales by category:\n", category.to_string(index=False))
print("\nMonthly sales:\n", monthly.to_string(index=False))
print("Charts saved in charts/; summary CSVs saved in output/.")
