import pytest
from src import analytics


def test_monthly_revenue_not_empty():
    df = analytics.monthly_revenue()
    assert not df.empty
    assert "revenue" in df.columns
    assert (df["revenue"] >= 0).all()

def test_average_order_value_positive():
    df = analytics.average_order_value()
    assert df["aov"].iloc[0] > 0

def test_repeat_purchase_rate_bounded():
    df = analytics.repeat_purchase_rate()
    rate = df["repeat_rate"].iloc[0]
    assert 0 <= rate <= 1

def test_product_ranking_has_results():
    df = analytics.product_ranking()
    assert len(df) > 0
    assert df["revenue"].is_monotonic_decreasing