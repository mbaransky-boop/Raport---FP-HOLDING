"""Podstawowa analiza danych sprzedażowych"""
import pandas as pd


def summarize_sales(df: pd.DataFrame) -> dict:
    """Zwraca słownik z podstawowymi miarami: total_revenue, orders_count, avg_order_value"""
    if df.empty:
        return {"total_revenue": 0, "orders_count": 0, "avg_order_value": 0}

    # Zakładamy, że kolumna 'revenue' istnieje
    total = df['revenue'].sum()
    count = len(df)
    avg = total / count if count else 0
    return {"total_revenue": float(total), "orders_count": int(count), "avg_order_value": float(avg)}
