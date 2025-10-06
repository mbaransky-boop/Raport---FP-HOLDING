import pandas as pd
from sales_reports.src.analysis import summarize_sales


def test_summarize_empty():
    df = pd.DataFrame(columns=['revenue'])
    res = summarize_sales(df)
    assert res['total_revenue'] == 0
    assert res['orders_count'] == 0
    assert res['avg_order_value'] == 0


def test_summarize_basic():
    df = pd.DataFrame({'revenue': [10, 20, 30]})
    res = summarize_sales(df)
    assert res['total_revenue'] == 60
    assert res['orders_count'] == 3
    assert res['avg_order_value'] == 20
