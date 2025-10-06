"""Moduł do generowania wykresów dla raportów sprzedażowych"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import base64
import io
from datetime import datetime
import seaborn as sns

# Ustaw style
plt.style.use('default')
sns.set_palette("husl")


def create_monthly_revenue_chart(monthly_data: list) -> str:
    """Wykres miesięcznych przychodów"""
    if not monthly_data:
        return ""
    
    df = pd.DataFrame(monthly_data)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Konwertuj miesiące na daty
    df['date'] = pd.to_datetime(df['month_year'] + '-01')
    
    ax.plot(df['date'], df['revenue'], marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax.fill_between(df['date'], df['revenue'], alpha=0.3, color='#2E86AB')
    
    ax.set_title('Miesięczne Przychody', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Miesiąc', fontsize=12)
    ax.set_ylabel('Przychód (PLN)', fontsize=12)
    
    # Formatowanie osi
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return _save_plot_as_base64(fig)


def create_profitability_chart(profitability_data: list) -> str:
    """Wykres rentowności miesięcznej"""
    if not profitability_data:
        return ""
    
    df = pd.DataFrame(profitability_data)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Wykres 1: Przychody vs Koszty
    months = range(len(df))
    width = 0.35
    
    ax1.bar([m - width/2 for m in months], df['revenue_brutto'], width, 
            label='Przychody Brutto', color='#A23B72', alpha=0.8)
    ax1.bar([m + width/2 for m in months], df['costs_brutto'], width,
            label='Koszty Brutto', color='#F18F01', alpha=0.8)
    
    ax1.set_title('Przychody vs Koszty (Brutto)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Kwota (PLN)', fontsize=12)
    ax1.set_xticks(months)
    ax1.set_xticklabels(df['month'], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Wykres 2: Marża
    colors = ['#28A745' if margin > 0 else '#DC3545' for margin in df['margin_brutto']]
    ax2.bar(months, df['margin_brutto'], color=colors, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    ax2.set_title('Marża Zysku (Brutto)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Marża (%)', fontsize=12)
    ax2.set_xlabel('Miesiąc', fontsize=12)
    ax2.set_xticks(months)
    ax2.set_xticklabels(df['month'], rotation=45)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return _save_plot_as_base64(fig)


def create_avg_order_value_chart(monthly_data: list) -> str:
    """Wykres średniej wartości rachunku"""
    if not monthly_data:
        return ""
    
    df = pd.DataFrame(monthly_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Konwertuj miesiące na daty
    df['date'] = pd.to_datetime(df['month_year'] + '-01')
    
    ax.bar(df['date'], df['avg_order_value'], color='#F39237', alpha=0.8, width=20)
    
    # Dodaj linię trendu
    z = np.polyfit(range(len(df)), df['avg_order_value'], 1)
    p = np.poly1d(z)
    ax.plot(df['date'], p(range(len(df))), "r--", alpha=0.8, linewidth=2, label='Trend')
    
    ax.set_title('Średnia Wartość Rachunku', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Miesiąc', fontsize=12)
    ax.set_ylabel('Średnia wartość (PLN)', fontsize=12)
    
    # Formatowanie
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    return _save_plot_as_base64(fig)


def create_orders_count_chart(monthly_data: list) -> str:
    """Wykres liczby rachunków miesięcznie"""
    if not monthly_data:
        return ""
    
    df = pd.DataFrame(monthly_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df['date'] = pd.to_datetime(df['month_year'] + '-01')
    
    ax.bar(df['date'], df['amount'], color='#6C5B7B', alpha=0.8, width=20)
    
    ax.set_title('Liczba Rachunków Miesięcznie', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Miesiąc', fontsize=12)
    ax.set_ylabel('Liczba rachunków', fontsize=12)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return _save_plot_as_base64(fig)


def _save_plot_as_base64(fig) -> str:
    """Konwertuje wykres matplotlib na base64 string"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    
    plot_data = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    
    encoded = base64.b64encode(plot_data).decode()
    return f"data:image/png;base64,{encoded}"


# Import numpy dla trendu
import numpy as np