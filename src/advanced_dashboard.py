#!/usr/bin/env python3
"""
Zaawansowany Dashboard Sprzedaży FP-HOLDING
Nowoczesne wykresy, analiza trendów i raportowanie
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AdvancedSalesDashboard:
    def __init__(self, csv_path, excel_path):
        self.csv_path = csv_path
        self.excel_path = excel_path
        self.df_monthly = None
        self.df_daily = None
        self.load_data()
        
    def load_data(self):
        """Ładowanie i przygotowanie danych"""
        # Dane miesięczne z CSV
        self.df_monthly = pd.read_csv(self.csv_path)
        self.df_monthly['date'] = pd.to_datetime(self.df_monthly['date'], errors='coerce')
        
        # Dane dzienne z Excela
        try:
            df_excel = pd.read_excel(self.excel_path, sheet_name=0)
            self.extract_daily_data(df_excel)
        except Exception as e:
            print(f"Błąd przy ładowaniu Excela: {e}")
            self.df_daily = pd.DataFrame()
    
    def extract_daily_data(self, df_excel):
        """Wyciąganie dziennych danych z Excela"""
        daily_data = []
        
        for i in range(len(df_excel)):
            if pd.notna(df_excel.iloc[i, 3]) and 'do' in str(df_excel.iloc[i, 3]):
                date_range = str(df_excel.iloc[i, 3])
                amount = df_excel.iloc[i, 4]
                
                if pd.notna(amount) and isinstance(amount, (int, float, str)):
                    try:
                        # Parsowanie daty początku
                        if 'do' in date_range:
                            start_date = date_range.split(' do ')[0]
                            date_obj = pd.to_datetime(start_date, format='%d.%m.%Y %H:%M')
                            
                            # Konwersja kwoty
                            if isinstance(amount, str):
                                amount_clean = amount.replace(' ', '').replace(',', '.')
                                amount_float = float(amount_clean)
                            else:
                                amount_float = float(amount)
                            
                            daily_data.append({
                                'date': date_obj.date(),
                                'amount': amount_float,
                                'day_of_week': date_obj.strftime('%A'),
                                'week_number': date_obj.isocalendar()[1]
                            })
                    except:
                        continue
        
        self.df_daily = pd.DataFrame(daily_data)
        if not self.df_daily.empty:
            self.df_daily['date'] = pd.to_datetime(self.df_daily['date'])
            self.df_daily = self.df_daily.sort_values('date')
    
    def calculate_trends(self):
        """Obliczanie trendów i statystyk"""
        trends = {}
        
        # Trendy miesięczne
        if not self.df_monthly.empty:
            monthly_valid = self.df_monthly[self.df_monthly['revenue'] > 0]
            if len(monthly_valid) > 1:
                trends['monthly_growth'] = (
                    (monthly_valid['revenue'].iloc[-1] - monthly_valid['revenue'].iloc[-2]) / 
                    monthly_valid['revenue'].iloc[-2] * 100
                )
                trends['avg_monthly_revenue'] = monthly_valid['revenue'].mean()
                trends['total_revenue'] = monthly_valid['revenue'].sum()
        
        # Trendy dzienne
        if not self.df_daily.empty:
            trends['avg_daily_revenue'] = self.df_daily['amount'].mean()
            trends['max_daily_revenue'] = self.df_daily['amount'].max()
            trends['min_daily_revenue'] = self.df_daily['amount'].min()
            
            # Trend wzrostowy/spadkowy
            if len(self.df_daily) > 7:
                recent_week = self.df_daily.tail(7)['amount'].mean()
                previous_week = self.df_daily.iloc[-14:-7]['amount'].mean() if len(self.df_daily) > 14 else recent_week
                trends['weekly_trend'] = ((recent_week - previous_week) / previous_week * 100) if previous_week > 0 else 0
        
        return trends
    
    def create_monthly_chart(self):
        """Wykres miesięcznych przychodów"""
        if self.df_monthly.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Wykres słupkowy
        fig.add_trace(go.Bar(
            x=self.df_monthly['customer'],
            y=self.df_monthly['revenue'],
            name='Przychody miesięczne',
            marker_color='rgb(55, 83, 109)',
            text=self.df_monthly['revenue'].round(2),
            textposition='auto',
        ))
        
        # Linia trendu
        fig.add_trace(go.Scatter(
            x=self.df_monthly['customer'],
            y=self.df_monthly['revenue'],
            mode='lines+markers',
            name='Trend',
            line=dict(color='rgb(255, 65, 54)', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title={
                'text': '<b>Przychody Miesięczne - Analiza Trendów</b>',
                'x': 0.5,
                'font': {'size': 20}
            },
            xaxis_title='Miesiąc',
            yaxis_title='Przychód (zł)',
            template='plotly_white',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_daily_chart(self):
        """Wykres dziennych sprzedaży"""
        if self.df_daily.empty:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Dzienna Sprzedaż - Wrzesień 2025', 'Analiza Tygodniowa'),
            vertical_spacing=0.12
        )
        
        # Wykres dzienny
        fig.add_trace(
            go.Scatter(
                x=self.df_daily['date'],
                y=self.df_daily['amount'],
                mode='lines+markers',
                name='Dzienna sprzedaż',
                line=dict(color='rgb(46, 204, 113)', width=2),
                marker=dict(size=6),
                fill='tonexty'
            ),
            row=1, col=1
        )
        
        # Średnia ruchoma (7 dni)
        if len(self.df_daily) >= 7:
            self.df_daily['moving_avg'] = self.df_daily['amount'].rolling(window=7).mean()
            fig.add_trace(
                go.Scatter(
                    x=self.df_daily['date'],
                    y=self.df_daily['moving_avg'],
                    mode='lines',
                    name='Średnia 7-dniowa',
                    line=dict(color='rgb(231, 76, 60)', width=3, dash='dash')
                ),
                row=1, col=1
            )
        
        # Analiza tygodniowa
        weekly_data = self.df_daily.groupby('week_number')['amount'].agg(['sum', 'mean', 'count']).reset_index()
        fig.add_trace(
            go.Bar(
                x=[f'Tydzień {w}' for w in weekly_data['week_number']],
                y=weekly_data['sum'],
                name='Suma tygodniowa',
                marker_color='rgb(155, 89, 182)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=800,
            title_text="<b>Analiza Dziennej Sprzedaży</b>",
            title_x=0.5,
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    def create_performance_metrics(self):
        """Metryki wydajności"""
        trends = self.calculate_trends()
        
        # Tworzenie kart metryk
        fig = go.Figure()
        
        metrics = [
            {'title': 'Avg Daily', 'value': f"{trends.get('avg_daily_revenue', 0):,.0f} zł", 'color': 'blue'},
            {'title': 'Max Daily', 'value': f"{trends.get('max_daily_revenue', 0):,.0f} zł", 'color': 'green'},
            {'title': 'Total Revenue', 'value': f"{trends.get('total_revenue', 0):,.0f} zł", 'color': 'purple'},
            {'title': 'Weekly Trend', 'value': f"{trends.get('weekly_trend', 0):+.1f}%", 'color': 'orange'}
        ]
        
        return trends, metrics
    
    def create_day_of_week_analysis(self):
        """Analiza sprzedaży według dni tygodnia"""
        if self.df_daily.empty:
            return go.Figure()
        
        day_stats = self.df_daily.groupby('day_of_week')['amount'].agg(['mean', 'sum', 'count']).reset_index()
        
        # Sortowanie według kolejności dni tygodnia
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_names_pl = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
        
        day_stats['day_order'] = day_stats['day_of_week'].apply(lambda x: day_order.index(x) if x in day_order else 999)
        day_stats = day_stats.sort_values('day_order')
        day_stats['day_pl'] = day_names_pl[:len(day_stats)]
        
        fig = go.Figure()
        
        # Wykres słupkowy
        fig.add_trace(go.Bar(
            x=day_stats['day_pl'],
            y=day_stats['mean'],
            name='Średnia dzienna',
            marker_color='rgb(52, 152, 219)',
            text=day_stats['mean'].round(0),
            textposition='auto'
        ))
        
        fig.update_layout(
            title={
                'text': '<b>Analiza Sprzedaży wg Dni Tygodnia</b>',
                'x': 0.5,
                'font': {'size': 18}
            },
            xaxis_title='Dzień tygodnia',
            yaxis_title='Średnia sprzedaż (zł)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def generate_dashboard_html(self, output_path='reports/advanced_dashboard.html'):
        """Generowanie kompletnego dashboardu HTML"""
        
        # Tworzenie wykresów
        monthly_chart = self.create_monthly_chart()
        daily_chart = self.create_daily_chart()
        day_analysis = self.create_day_of_week_analysis()
        trends, metrics = self.create_performance_metrics()
        
        # HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard Sprzedaży FP-HOLDING</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    background: linear-gradient(45deg, #2c3e50, #3498db);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5rem;
                    font-weight: 300;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                    font-size: 1.1rem;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .metric-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 25px;
                    border-radius: 12px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease;
                }}
                .metric-card:hover {{
                    transform: translateY(-5px);
                }}
                .metric-value {{
                    font-size: 2rem;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .metric-title {{
                    font-size: 0.9rem;
                    opacity: 0.9;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .chart-container {{
                    margin-bottom: 30px;
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                }}
                .insights {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    margin-top: 30px;
                    border-left: 5px solid #3498db;
                }}
                .insights h3 {{
                    color: #2c3e50;
                    margin-top: 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏢 Dashboard Sprzedaży FP-HOLDING</h1>
                    <p>Zaawansowana analiza sprzedaży i trendów - Wrzesień 2025</p>
                    <p>Ostatnia aktualizacja: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{trends.get('avg_daily_revenue', 0):,.0f} zł</div>
                        <div class="metric-title">Średnia Dzienna</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{trends.get('max_daily_revenue', 0):,.0f} zł</div>
                        <div class="metric-title">Najwyższy Dzień</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{trends.get('total_revenue', 0):,.0f} zł</div>
                        <div class="metric-title">Łączny Przychód</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{trends.get('weekly_trend', 0):+.1f}%</div>
                        <div class="metric-title">Trend Tygodniowy</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div id="monthly-chart"></div>
                </div>
                
                <div class="chart-container">
                    <div id="daily-chart"></div>
                </div>
                
                <div class="chart-container">
                    <div id="day-analysis"></div>
                </div>
                
                <div class="insights">
                    <h3>📊 Kluczowe Insights</h3>
                    <ul>
                        <li><strong>Najlepszy dzień:</strong> {self.df_daily.loc[self.df_daily['amount'].idxmax(), 'date'].strftime('%d.%m.%Y') if not self.df_daily.empty else 'Brak danych'} 
                            ({trends.get('max_daily_revenue', 0):,.0f} zł)</li>
                        <li><strong>Trend tygodniowy:</strong> 
                            {'📈 Wzrost' if trends.get('weekly_trend', 0) > 0 else '📉 Spadek' if trends.get('weekly_trend', 0) < 0 else '➡️ Stabilny'} 
                            ({trends.get('weekly_trend', 0):+.1f}%)</li>
                        <li><strong>Średnia dzienna:</strong> {trends.get('avg_daily_revenue', 0):,.0f} zł</li>
                        <li><strong>Zakres dzienny:</strong> {trends.get('min_daily_revenue', 0):,.0f} - {trends.get('max_daily_revenue', 0):,.0f} zł</li>
                    </ul>
                </div>
            </div>
            
            <script>
                {monthly_chart.to_html(include_plotlyjs=False, div_id="monthly-chart")}
                {daily_chart.to_html(include_plotlyjs=False, div_id="daily-chart")}
                {day_analysis.to_html(include_plotlyjs=False, div_id="day-analysis")}
            </script>
        </body>
        </html>
        """
        
        # Zapisanie pliku
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard wygenerowany: {output_path}")
        return output_path

def main():
    """Główna funkcja generująca dashboard"""
    csv_path = './data/rozliczenie_data.csv'
    excel_path = './data/Zestawienie sprzedaży  Rozliczenia .xls'
    
    # Tworzenie dashboardu
    dashboard = AdvancedSalesDashboard(csv_path, excel_path)
    output_path = dashboard.generate_dashboard_html()
    
    print(f"🎉 Nowoczesny dashboard gotowy!")
    print(f"📂 Lokalizacja: {output_path}")
    print(f"🌐 Otwórz w przeglądarce aby zobaczyć interaktywne wykresy")

if __name__ == "__main__":
    main()