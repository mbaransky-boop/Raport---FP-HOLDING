"""Rozszerzona analiza danych sprzedażowych z rentownością i trendami"""
import pandas as pd
import numpy as np
from datetime import datetime


def summarize_sales(df: pd.DataFrame) -> dict:
    """Zwraca słownik z podstawowymi miarami: total_revenue, orders_count, avg_order_value"""
    if df.empty:
        return {"total_revenue": 0, "orders_count": 0, "avg_order_value": 0}

    # Zakładamy, że kolumna 'revenue' istnieje
    total = df['revenue'].sum()
    count = len(df)
    avg = total / count if count else 0
    return {"total_revenue": float(total), "orders_count": int(count), "avg_order_value": float(avg)}


def analyze_monthly_trends(df: pd.DataFrame) -> dict:
    """Analiza trendów miesięcznych z danymi szczegółowymi"""
    if df.empty:
        return {}
    
    # Konwertuj datę
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['month_year'] = df['date'].dt.strftime('%Y-%m')
    df['month_name'] = df['date'].dt.strftime('%B %Y')
    
    # Grupuj po miesiącach
    monthly = df.groupby(['month_year', 'month_name']).agg({
        'revenue': 'sum',
        'amount': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    monthly['avg_order_value'] = monthly['revenue'] / monthly['amount']
    monthly = monthly.sort_values('month_year')
    
    return {
        'monthly_data': monthly.to_dict('records'),
        'best_month': monthly.loc[monthly['revenue'].idxmax()].to_dict() if len(monthly) > 0 else {},
        'worst_month': monthly.loc[monthly['revenue'].idxmin()].to_dict() if len(monthly) > 0 else {},
        'trend_direction': 'up' if len(monthly) > 1 and monthly['revenue'].iloc[-1] > monthly['revenue'].iloc[0] else 'down'
    }


def analyze_profitability_from_excel(excel_path: str) -> dict:
    """Analiza rentowności z oryginalnego pliku Excel"""
    try:
        df = pd.read_excel(excel_path)
        
        # Filtruj dane miesięczne
        df_clean = df[df['Unnamed: 0'].notna() & df['OBRÓT BRUTTO'].notna()].copy()
        df_clean = df_clean[~df_clean['Unnamed: 0'].isin(['2024', '2025'])].copy()
        
        profitability_data = []
        
        for _, row in df_clean.iterrows():
            month = row['Unnamed: 0']
            if pd.isna(month):
                continue
                
            revenue_brutto = row['OBRÓT BRUTTO'] if pd.notna(row['OBRÓT BRUTTO']) else 0
            revenue_netto = row['OBRÓT NETTO'] if pd.notna(row['OBRÓT NETTO']) else 0
            costs_brutto = row['KOSZTY BRUTTO'] if pd.notna(row['KOSZTY BRUTTO']) else 0
            costs_netto = row['KOSZTY NETTO'] if pd.notna(row['KOSZTY NETTO']) else 0
            profit_brutto = row['TOTAL BRUTTO ZYSK/STRATA'] if pd.notna(row['TOTAL BRUTTO ZYSK/STRATA']) else 0
            profit_netto = row['TOTAL NETTO ZYSK/STRATA'] if pd.notna(row['TOTAL NETTO ZYSK/STRATA']) else 0
            
            margin_brutto = (profit_brutto / revenue_brutto * 100) if revenue_brutto > 0 else 0
            margin_netto = (profit_netto / revenue_netto * 100) if revenue_netto > 0 else 0
            
            profitability_data.append({
                'month': month,
                'revenue_brutto': revenue_brutto,
                'revenue_netto': revenue_netto,
                'costs_brutto': costs_brutto,
                'costs_netto': costs_netto,
                'profit_brutto': profit_brutto,
                'profit_netto': profit_netto,
                'margin_brutto': margin_brutto,
                'margin_netto': margin_netto
            })
        
        # Podsumowanie
        total_revenue_brutto = sum(d['revenue_brutto'] for d in profitability_data)
        total_costs_brutto = sum(d['costs_brutto'] for d in profitability_data)
        total_profit_brutto = sum(d['profit_brutto'] for d in profitability_data)
        
        avg_margin = (total_profit_brutto / total_revenue_brutto * 100) if total_revenue_brutto > 0 else 0
        
        return {
            'monthly_profitability': profitability_data,
            'summary': {
                'total_revenue_brutto': total_revenue_brutto,
                'total_costs_brutto': total_costs_brutto,
                'total_profit_brutto': total_profit_brutto,
                'average_margin': avg_margin,
                'profitable_months': len([d for d in profitability_data if d['profit_brutto'] > 0]),
                'loss_months': len([d for d in profitability_data if d['profit_brutto'] < 0])
            }
        }
        
    except Exception as e:
        return {'error': str(e)}


def comprehensive_analysis(df: pd.DataFrame, excel_path: str = None) -> dict:
    """Kompleksowa analiza łącząca dane sprzedażowe i rentowność"""
    basic_stats = summarize_sales(df)
    trends = analyze_monthly_trends(df)
    
    result = {
        'basic_stats': basic_stats,
        'trends': trends,
        'profitability': {}
    }
    
    if excel_path:
        result['profitability'] = analyze_profitability_from_excel(excel_path)
    
    return result