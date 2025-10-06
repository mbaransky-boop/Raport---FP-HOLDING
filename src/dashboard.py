"""Generator raportów w formacie HTML Dashboard"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import pandas as pd
from datetime import datetime
from analysis_extended import comprehensive_analysis
from charts import (
    create_monthly_revenue_chart, 
    create_profitability_chart,
    create_avg_order_value_chart,
    create_orders_count_chart
)
    create_avg_order_value_chart,
    create_orders_count_chart
)


def generate_dashboard_report(csv_path: str, excel_path: str, output_path: str, template_dir: str = None):
    """Generuje kompletny dashboard z wykresami i analizą rentowności"""
    
    # Wczytaj dane CSV
    df = pd.read_csv(csv_path)
    
    # Wykonaj kompleksową analizę
    analysis = comprehensive_analysis(df, excel_path)
    
    # Generuj wykresy
    charts = {}
    
    if analysis['trends'].get('monthly_data'):
        charts['monthly_revenue'] = create_monthly_revenue_chart(analysis['trends']['monthly_data'])
        charts['avg_order_value'] = create_avg_order_value_chart(analysis['trends']['monthly_data'])
        charts['orders_count'] = create_orders_count_chart(analysis['trends']['monthly_data'])
    
    if analysis['profitability'].get('monthly_profitability'):
        charts['profitability'] = create_profitability_chart(analysis['profitability']['monthly_profitability'])
    
    # Przygotuj dane dla szablonu
    template_data = {
        'title': 'Sales Dashboard - Analiza Rozliczenia',
        'summary': analysis['basic_stats'],
        'trends': analysis['trends'],
        'profitability': analysis['profitability'],
        'charts': charts,
        'analysis_period': _get_analysis_period(analysis['trends']),
        'generation_date': datetime.now().strftime('%d %B %Y, %H:%M')
    }
    
    # Renderuj szablon
    output_path = Path(output_path)
    template_dir = Path(template_dir) if template_dir else Path(__file__).resolve().parents[1] / 'reports' / 'templates'

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('dashboard.html.j2')
    rendered = template.render(**template_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding='utf-8')
    
    return str(output_path)


def _get_analysis_period(trends: dict) -> str:
    """Określ okres analizy na podstawie danych"""
    if not trends.get('monthly_data'):
        return "Brak danych"
    
    monthly_data = trends['monthly_data']
    if len(monthly_data) == 0:
        return "Brak danych"
    
    first_month = monthly_data[0]['month_name']
    last_month = monthly_data[-1]['month_name']
    
    if len(monthly_data) == 1:
        return first_month
    
    return f"{first_month} - {last_month}"