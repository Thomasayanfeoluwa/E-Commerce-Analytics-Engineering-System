import matplotlib.pyplot as plt
from src import analytics


def plot_monthly_revenue():
    df = analytics.monthly_revenue()
    plt.figure(figsize=(10, 5))
    plt.plot(df["month"], df["revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("reports/figures/monthly_revenue.png")
    plt.close()

def plot_top_products():
    df = analytics.product_ranking().head(10)
    plt.figure(figsize=(10, 5))
    plt.barh(df["product_name"], df["revenue"])
    plt.title("Top 10 Products by Revenue")
    plt.tight_layout()
    plt.savefig("reports/figures/top_products.png")
    plt.close()