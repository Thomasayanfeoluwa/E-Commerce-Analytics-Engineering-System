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

def 