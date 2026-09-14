from src import analytics
analytics.monthly_revenue().to_csv("data/processed/monthly_revenue.csv", index=False)
analytics.average_order_value().to_csv("data/processed/aov.csv", index=False)
# etc.