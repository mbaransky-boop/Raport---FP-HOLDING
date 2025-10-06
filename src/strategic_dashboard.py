"""Rozszerzony generator raportów strategicznych z prognozami"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import pandas as pd
from datetime import datetime
from analysis_extended import comprehensive_analysis
from predictive_analysis import comprehensive_predictive_analysis
from recommendations import generate_strategic_recommendations, create_action_plan, generate_executive_summary
from charts import (
    create_monthly_revenue_chart, 
    create_profitability_chart,
    create_avg_order_value_chart,
    create_orders_count_chart
)


def generate_strategic_report(csv_path: str, excel_path: str, output_path: str, template_dir: str = None):
    """Generuje kompletny raport strategiczny z prognozami i rekomendacjami"""
    
    # Wczytaj dane CSV
    df = pd.read_csv(csv_path)
    
    # Wykonaj podstawową analizę
    basic_analysis = comprehensive_analysis(df, excel_path)
    
    # Wykonaj analizę predykcyjną
    predictive_analysis = comprehensive_predictive_analysis(
        basic_analysis['trends'].get('monthly_data', []),
        basic_analysis['profitability'].get('monthly_profitability', [])
    )
    
    # Generuj rekomendacje strategiczne
    recommendations = generate_strategic_recommendations(predictive_analysis)
    
    # Utwórz plan działań
    action_plan = create_action_plan(recommendations, predictive_analysis.get('forecast', {}))
    
    # Podsumowanie wykonawcze
    executive_summary = generate_executive_summary(predictive_analysis, recommendations)
    
    # Generuj wykresy
    charts = {}
    if basic_analysis['trends'].get('monthly_data'):
        charts['monthly_revenue'] = create_monthly_revenue_chart(basic_analysis['trends']['monthly_data'])
        charts['avg_order_value'] = create_avg_order_value_chart(basic_analysis['trends']['monthly_data'])
        charts['orders_count'] = create_orders_count_chart(basic_analysis['trends']['monthly_data'])
    
    if basic_analysis['profitability'].get('monthly_profitability'):
        charts['profitability'] = create_profitability_chart(basic_analysis['profitability']['monthly_profitability'])
    
    # Przygotuj dane dla szablonu
    template_data = {
        'title': 'Strategiczny Raport Biznesowy - Forum Panorama',
        'summary': basic_analysis['basic_stats'],
        'trends': basic_analysis['trends'],
        'profitability': basic_analysis['profitability'],
        'predictive': predictive_analysis,
        'recommendations': recommendations,
        'action_plan': action_plan,
        'executive_summary': executive_summary,
        'charts': charts,
        'analysis_period': _get_analysis_period(basic_analysis['trends']),
        'generation_date': datetime.now().strftime('%d %B %Y, %H:%M'),
        'forecast_period': predictive_analysis.get('forecast', {}).get('forecast_period', 'N/A')
    }
    
    # Renderuj szablon
    output_path = Path(output_path)
    template_dir = Path(template_dir) if template_dir else Path(__file__).resolve().parents[1] / 'reports' / 'templates'

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('strategic_report.html.j2')
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