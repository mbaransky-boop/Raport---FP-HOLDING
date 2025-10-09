"""
Generator nowoczesnego raportu finansowego dla FP HOLDING
Dark mode z animacjami i efektami wizualnymi
"""
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """
    Generator raportu finansowego - nowoczesna wersja dark mode
    """
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.analysis = analyzer.analysis
        
    def create_revenue_chart(self):
        """Wykres analizy korelacji przychodów i kosztów"""
        df = self.analyzer.df
        
        import numpy as np
        correlation = np.corrcoef(df['Obrót_netto'], df['Koszty_total'])[0, 1]
        z = np.polyfit(df['Obrót_netto'], df['Koszty_total'], 1)
        p = np.poly1d(z)
        
        fig = go.Figure()
        
        # Punkty danych z neonowymi kolorami
        colors_list = ['#FF006E' if profit < 0 else '#06FFA5' for profit in df['Zysk_Excel']]
        
        fig.add_trace(go.Scatter(
            x=df['Obrót_netto'].tolist(),
            y=df['Koszty_total'].tolist(),
            mode='markers',
            marker=dict(
                size=24, 
                color=colors_list, 
                line=dict(width=3, color='rgba(255,255,255,0.8)'),
                opacity=0.9
            ),
            text=df['Okres_str'].tolist(),
            hovertemplate='<b>%{text}</b><br>Przychód: %{x:,.0f} zł<br>Koszty: %{y:,.0f} zł<extra></extra>',
            name='Okresy rozliczeniowe'
        ))
        
        # Linia trendu - neonowy niebieski
        x_trend = np.linspace(df['Obrót_netto'].min(), df['Obrót_netto'].max(), 100)
        fig.add_trace(go.Scatter(
            x=x_trend.tolist(),
            y=p(x_trend).tolist(),
            mode='lines',
            line=dict(color='#3B82F6', width=4, dash='dash'),
            name=f'Trend regresji (r={correlation:.3f})',
            hovertemplate='Linia trendu<extra></extra>'
        ))
        
        # Linia break-even
        max_val = max(df['Obrót_netto'].max(), df['Koszty_total'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            line=dict(color='#8B5CF6', width=3, dash='dot'),
            name='Próg rentowności',
            hovertemplate='Break-even point<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text=f'Analiza Korelacji: Przychody vs Koszty<br><sub>r={correlation:.3f}</sub>',
                font=dict(size=20, color='#E8E8E8', family='Inter')
            ),
            xaxis_title='Przychód netto (PLN)',
            yaxis_title='Koszty operacyjne (PLN)',
            template='plotly_dark',
            height=550,
            showlegend=True,
            legend=dict(
                x=0.02, 
                y=0.98, 
                bgcolor='rgba(30,30,46,0.9)', 
                bordercolor='#3B82F6', 
                borderwidth=2,
                font=dict(color='#E8E8E8')
            ),
            font=dict(family='Inter', size=12, color='#E8E8E8'),
            paper_bgcolor='rgba(26,26,46,0.95)',
            plot_bgcolor='rgba(30,30,46,0.8)'
        )
        
        return fig.to_json()
    
    def create_trend_chart(self):
        """Wykres trendu czasowego z gradientami"""
        df = self.analyzer.df
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['Okres_str'].tolist(),
            y=df['Obrót_netto'].tolist(),
            name='Przychód netto',
            marker=dict(
                color=df['Obrót_netto'].tolist(),
                colorscale=[[0, '#10B981'], [1, '#06FFA5']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{x}</b><br>Przychód: %{y:,.0f} PLN<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=df['Okres_str'].tolist(),
            y=df['Koszty_total'].tolist(),
            name='Koszty operacyjne',
            marker=dict(
                color=df['Koszty_total'].tolist(),
                colorscale=[[0, '#F59E0B'], [1, '#EF4444']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{x}</b><br>Koszty: %{y:,.0f} PLN<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text='Trend Przychodów i Kosztów (14 okresów)',
                font=dict(size=20, color='#E8E8E8', family='Inter')
            ),
            xaxis_title='Okres rozliczeniowy',
            yaxis_title='Wartość (PLN)',
            barmode='group',
            template='plotly_dark',
            height=500,
            hovermode='x unified',
            font=dict(family='Inter', size=12, color='#E8E8E8'),
            paper_bgcolor='rgba(26,26,46,0.95)',
            plot_bgcolor='rgba(30,30,46,0.8)'
        )
        
        return fig.to_json()
    
    def create_profit_chart(self):
        """Wykres rentowności z neonowymi kolorami"""
        df = self.analyzer.df
        profit = df['Zysk_Excel']
        colors = ['#06FFA5' if p > 0 else '#FF006E' for p in profit]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Okres_str'].tolist(),
            y=profit.tolist(),
            marker=dict(
                color=colors,
                line=dict(width=2, color='rgba(255,255,255,0.3)')
            ),
            hovertemplate='<b>%{x}</b><br>Wynik: %{y:,.0f} PLN<extra></extra>',
            name='Wynik netto'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="#8B5CF6", line_width=3)
        
        fig.update_layout(
            title=dict(
                text='Rentowność: Wynik Finansowy Netto',
                font=dict(size=20, color='#E8E8E8', family='Inter')
            ),
            xaxis_title='Okres rozliczeniowy',
            yaxis_title='Wynik finansowy (PLN)',
            template='plotly_dark',
            height=500,
            font=dict(family='Inter', size=12, color='#E8E8E8'),
            paper_bgcolor='rgba(26,26,46,0.95)',
            plot_bgcolor='rgba(30,30,46,0.8)'
        )
        
        return fig.to_json()
    
    def create_zus_chart(self):
        """Wykres ZUS z efektem glow"""
        df = self.analyzer.df
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Okres_str'].tolist(),
            y=df['ZUS'].tolist(),
            mode='lines+markers',
            line=dict(color='#3B82F6', width=4, shape='spline'),
            marker=dict(size=12, color='#3B82F6', line=dict(width=3, color='#60A5FA')),
            hovertemplate='<b>%{x}</b><br>ZUS: %{y:,.0f} PLN<extra></extra>',
            name='Składki ZUS',
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        avg = df['ZUS'].mean()
        fig.add_hline(
            y=avg, 
            line_dash="dash", 
            line_color="#FF006E",
            line_width=3,
            annotation_text=f"Średnia: {avg:,.0f} PLN",
            annotation_position="top right",
            annotation_font=dict(color='#E8E8E8', size=14)
        )
        
        fig.update_layout(
            title=dict(
                text='Zobowiązania ZUS: Trend Okresowy',
                font=dict(size=20, color='#E8E8E8', family='Inter')
            ),
            xaxis_title='Okres rozliczeniowy',
            yaxis_title='Składki ZUS (PLN)',
            template='plotly_dark',
            height=500,
            font=dict(family='Inter', size=12, color='#E8E8E8'),
            paper_bgcolor='rgba(26,26,46,0.95)',
            plot_bgcolor='rgba(30,30,46,0.8)'
        )
        
        return fig.to_json()
    
    def create_cost_profit_analysis(self):
        """Wykres analizy relacji koszty-zyski dla managera"""
        df = self.analyzer.df
        
        fig = go.Figure()
        
        # Waterfall pokazujący jak koszty wpływają na zysk
        fig.add_trace(go.Waterfall(
            name="Analiza P&L",
            orientation="v",
            x=df['Okres_str'].tolist(),
            textposition="outside",
            text=[f"{val:,.0f}" for val in df['Zysk_Excel']],
            y=df['Zysk_Excel'].tolist(),
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#FF006E"}},
            increasing={"marker": {"color": "#06FFA5"}},
            totals={"marker": {"color": "#3B82F6"}}
        ))
        
        fig.update_layout(
            title=dict(
                text='Analiza Koszty-Zyski: Struktura Rentowności',
                font=dict(size=20, color='#E8E8E8', family='Inter')
            ),
            xaxis_title='Okres',
            yaxis_title='Zysk/Strata (PLN)',
            template='plotly_dark',
            height=500,
            showlegend=False,
            font=dict(family='Inter', size=12, color='#E8E8E8'),
            paper_bgcolor='rgba(26,26,46,0.95)',
            plot_bgcolor='rgba(30,30,46,0.8)'
        )
        
        return fig.to_json()
    
    def create_cost_breakdown_chart(self):
        """Wykres rozbicia kosztów dla managera"""
        df = self.analyzer.df
        
        # Średnie koszty w okresie
        avg_kwota_netto = df['Kwota_netto'].mean()
        avg_zus = df['ZUS'].mean()
        avg_pit = df['PIT'].mean()
        avg_koszt_prac = df['Koszt_pracowniczy'].mean()
        
        fig = go.Figure(data=[go.Pie(
            labels=['Produkty/Usługi', 'ZUS', 'PIT', 'Koszty Pracownicze'],
            values=[avg_kwota_netto, avg_zus, avg_pit, avg_koszt_prac],
            hole=.5,
            marker=dict(colors=['#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6']),
            textinfo='label+percent+value',
            texttemplate='<b>%{label}</b><br>%{value:,.0f} PLN<br>(%{percent})',
            hovertemplate='<b>%{label}</b><br>Średnio: %{value:,.0f} PLN<br>Udział: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text='Struktura Kosztów (Średnia Miesięczna)',
                font=dict(size=20, color='#E8E8E8', family='Inter')
            ),
            template='plotly_dark',
            height=500,
            font=dict(family='Inter', size=14, color='#E8E8E8'),
            paper_bgcolor='rgba(26,26,46,0.95)',
            showlegend=True,
            legend=dict(
                bgcolor='rgba(30,30,46,0.9)',
                bordercolor='#3B82F6',
                borderwidth=1,
                font=dict(color='#E8E8E8')
            )
        )
        
        return fig.to_json()
    
    def generate_html(self, output_path='reports/fp_holding_raport.html'):
        """Generuje nowoczesny dark mode raport"""
        
        revenue_chart = self.create_revenue_chart()
        trend_chart = self.create_trend_chart()
        profit_chart = self.create_profit_chart()
        zus_chart = self.create_zus_chart()
        cost_profit_chart = self.create_cost_profit_analysis()
        cost_breakdown_chart = self.create_cost_breakdown_chart()
        
        # KPI
        total_revenue = self.analysis['summary']['total_revenue']
        total_costs = self.analysis['summary']['total_costs']
        total_profit = self.analysis['summary']['total_profit']
        margin = self.analysis['summary']['margin']
        avg_revenue = self.analysis['summary']['avg_revenue']
        avg_costs = self.analysis['summary']['avg_costs']
        profitable_months = self.analysis['summary']['profitable_months']
        loss_months = self.analysis['summary']['loss_months']
        
        roi = (total_profit / total_costs * 100) if total_costs > 0 else 0
        breakeven_coverage = (avg_revenue / avg_costs * 100) if avg_costs > 0 else 0
        
        html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FP HOLDING - Financial Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(59, 130, 246, 0.4), 0 0 40px rgba(59, 130, 246, 0.2); }}
            50% {{ box-shadow: 0 0 30px rgba(59, 130, 246, 0.6), 0 0 60px rgba(59, 130, 246, 0.3); }}
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: #E8E8E8;
            line-height: 1.6;
            min-height: 100vh;
            padding: 30px 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: rgba(26, 26, 46, 0.95);
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 80px rgba(59, 130, 246, 0.1);
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.2);
        }}
        
        .header {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            padding: 60px;
            border-bottom: 3px solid #3B82F6;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(59,130,246,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }}
        
        .header h1 {{
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(135deg, #3B82F6, #8B5CF6, #06FFA5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
            letter-spacing: -1px;
            position: relative;
            animation: fadeIn 1s ease-out;
        }}
        
        .header .subtitle {{
            font-size: 1.4em;
            color: #A0AEC0;
            font-weight: 300;
            margin-bottom: 25px;
            position: relative;
        }}
        
        .header .meta {{
            font-size: 0.95em;
            color: #718096;
            border-top: 1px solid rgba(59, 130, 246, 0.3);
            padding-top: 25px;
            margin-top: 25px;
            font-family: 'JetBrains Mono', monospace;
            position: relative;
        }}
        
        .meta-badge {{
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin-right: 15px;
            border: 1px solid rgba(59, 130, 246, 0.4);
            font-size: 0.9em;
        }}
        
        .executive-summary {{
            background: linear-gradient(135deg, rgba(6, 255, 165, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
            border-left: 5px solid #06FFA5;
            padding: 50px 60px;
            margin: 0;
            animation: fadeIn 1.2s ease-out;
        }}
        
        .executive-summary h2 {{
            color: #06FFA5;
            font-size: 2em;
            margin-bottom: 25px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .executive-summary p {{
            font-size: 1.15em;
            line-height: 1.9;
            color: #CBD5E0;
            margin-bottom: 18px;
        }}
        
        .executive-summary .highlight {{
            background: rgba(30, 30, 46, 0.8);
            padding: 30px;
            border-radius: 16px;
            margin-top: 25px;
            border: 1px solid rgba(6, 255, 165, 0.3);
            box-shadow: 0 4px 20px rgba(6, 255, 165, 0.1);
        }}
        
        .critical-alert {{
            background: linear-gradient(135deg, rgba(255, 0, 110, 0.15) 0%, rgba(239, 68, 68, 0.15) 100%);
            border-left: 6px solid #FF006E;
            padding: 50px 60px;
            margin: 0;
            animation: fadeIn 1.4s ease-out, pulse 3s infinite;
        }}
        
        .critical-alert h2 {{
            color: #FF006E;
            font-size: 1.8em;
            margin-bottom: 25px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .critical-alert ul {{
            list-style: none;
            font-size: 1.2em;
            line-height: 2.2;
        }}
        
        .critical-alert li {{
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 0, 110, 0.2);
            transition: transform 0.3s;
        }}
        
        .critical-alert li:hover {{
            transform: translateX(10px);
        }}
        
        .critical-alert strong {{
            color: #FF006E;
            font-weight: 900;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .content {{
            padding: 60px;
        }}
        
        .section {{
            margin: 70px 0;
            animation: fadeIn 1.6s ease-out;
        }}
        
        .section h2 {{
            color: #3B82F6;
            font-size: 2.2em;
            margin-bottom: 20px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 3px solid #3B82F6;
            padding-bottom: 20px;
        }}
        
        .section-intro {{
            color: #A0AEC0;
            font-size: 1.1em;
            margin-bottom: 35px;
            font-style: italic;
            line-height: 1.8;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            margin: 50px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, rgba(30, 30, 46, 0.9) 0%, rgba(26, 26, 46, 0.9) 100%);
            padding: 40px;
            border-radius: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeIn 1.8s ease-out;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        }}
        
        .metric-card:hover {{
            transform: translateY(-10px) scale(1.02);
            border-color: #3B82F6;
            animation: glow 2s infinite;
        }}
        
        .metric-card.positive::before {{
            background: linear-gradient(90deg, #06FFA5, #10B981);
        }}
        
        .metric-card.negative::before {{
            background: linear-gradient(90deg, #FF006E, #EF4444);
        }}
        
        .metric-card.warning::before {{
            background: linear-gradient(90deg, #F59E0B, #EF4444);
        }}
        
        .metric-card h3 {{
            font-size: 0.9em;
            color: #A0AEC0;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .metric-card .value {{
            font-size: 3em;
            font-weight: 900;
            color: #E8E8E8;
            margin-bottom: 15px;
            line-height: 1;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .metric-card .subtitle {{
            font-size: 0.95em;
            color: #718096;
            font-weight: 400;
        }}
        
        .chart-container {{
            background: rgba(30, 30, 46, 0.8);
            padding: 40px;
            border-radius: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            margin: 40px 0;
            transition: all 0.3s;
            animation: fadeIn 2s ease-out;
        }}
        
        .chart-container:hover {{
            border-color: #3B82F6;
            box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
        }}
        
        .recommendations {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            padding: 50px;
            border-radius: 20px;
            border: 2px solid #3B82F6;
            margin: 50px 0;
            animation: fadeIn 2.2s ease-out;
        }}
        
        .recommendations h3 {{
            color: #3B82F6;
            font-size: 1.6em;
            margin-bottom: 30px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .recommendation-item {{
            background: rgba(30, 30, 46, 0.9);
            padding: 30px;
            margin: 20px 0;
            border-radius: 16px;
            border-left: 5px solid #3B82F6;
            transition: all 0.3s;
        }}
        
        .recommendation-item:hover {{
            transform: translateX(10px);
            border-left-width: 8px;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }}
        
        .recommendation-item h4 {{
            color: #E8E8E8;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .recommendation-item p {{
            color: #A0AEC0;
            line-height: 1.9;
        }}
        
        .recommendation-item.priority-high {{
            border-left-color: #FF006E;
        }}
        
        .recommendation-item.priority-medium {{
            border-left-color: #F59E0B;
        }}
        
        .footer {{
            background: linear-gradient(135deg, rgba(30, 30, 46, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
            color: #A0AEC0;
            padding: 50px 60px;
            text-align: center;
            border-top: 3px solid #3B82F6;
        }}
        
        .footer p {{
            margin: 10px 0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 8px 18px;
            border-radius: 25px;
            font-size: 0.85em;
            font-weight: 700;
            margin-left: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .badge.success {{ background: linear-gradient(135deg, #06FFA5, #10B981); color: #000; }}
        .badge.danger {{ background: linear-gradient(135deg, #FF006E, #EF4444); color: #FFF; }}
        .badge.warning {{ background: linear-gradient(135deg, #F59E0B, #EF4444); color: #FFF; }}
        .badge.info {{ background: linear-gradient(135deg, #3B82F6, #8B5CF6); color: #FFF; }}
        
        h3 {{
            color: #E8E8E8;
            margin: 50px 0 20px 0;
            font-size: 1.5em;
            font-weight: 700;
        }}
        
        /* Interactive Simulator Styles */
        .simulator-section {{
            background: linear-gradient(135deg, rgba(6, 255, 165, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
            padding: 60px;
            border-radius: 24px;
            border: 2px solid #06FFA5;
            margin: 60px 0;
            animation: fadeIn 2.4s ease-out;
        }}
        
        .simulator-section h2 {{
            color: #06FFA5;
            font-size: 2.2em;
            margin-bottom: 15px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-align: center;
        }}
        
        .simulator-intro {{
            text-align: center;
            color: #A0AEC0;
            font-size: 1.15em;
            margin-bottom: 50px;
            line-height: 1.8;
        }}
        
        .simulator-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 50px;
        }}
        
        @media (max-width: 1200px) {{
            .simulator-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .controls-panel {{
            background: rgba(30, 30, 46, 0.9);
            padding: 40px;
            border-radius: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
        }}
        
        .control-group {{
            margin-bottom: 35px;
        }}
        
        .control-label {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            color: #E8E8E8;
            font-size: 1.1em;
            font-weight: 600;
        }}
        
        .control-value {{
            color: #06FFA5;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2em;
            font-weight: 700;
        }}
        
        .slider {{
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.3), rgba(6, 255, 165, 0.3));
            outline: none;
            -webkit-appearance: none;
        }}
        
        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3B82F6, #06FFA5);
            cursor: pointer;
            box-shadow: 0 0 20px rgba(6, 255, 165, 0.6);
            transition: all 0.3s;
        }}
        
        .slider::-webkit-slider-thumb:hover {{
            transform: scale(1.3);
            box-shadow: 0 0 30px rgba(6, 255, 165, 0.9);
        }}
        
        .slider::-moz-range-thumb {{
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3B82F6, #06FFA5);
            cursor: pointer;
            box-shadow: 0 0 20px rgba(6, 255, 165, 0.6);
            border: none;
            transition: all 0.3s;
        }}
        
        .slider::-moz-range-thumb:hover {{
            transform: scale(1.3);
            box-shadow: 0 0 30px rgba(6, 255, 165, 0.9);
        }}
        
        .results-panel {{
            background: rgba(30, 30, 46, 0.9);
            padding: 40px;
            border-radius: 20px;
            border: 2px solid rgba(6, 255, 165, 0.3);
        }}
        
        .result-card {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 255, 165, 0.1) 100%);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 20px;
            border-left: 4px solid #3B82F6;
            transition: all 0.3s;
        }}
        
        .result-card:hover {{
            transform: translateX(5px);
            border-left-width: 6px;
        }}
        
        .result-card.positive {{
            border-left-color: #06FFA5;
        }}
        
        .result-card.negative {{
            border-left-color: #FF006E;
        }}
        
        .result-title {{
            color: #A0AEC0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
        }}
        
        .result-value {{
            color: #E8E8E8;
            font-size: 2.2em;
            font-weight: 900;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 8px;
        }}
        
        .result-change {{
            font-size: 0.95em;
            color: #718096;
        }}
        
        .result-change.positive {{
            color: #06FFA5;
        }}
        
        .result-change.negative {{
            color: #FF006E;
        }}
        
        .forecast-chart {{
            background: rgba(30, 30, 46, 0.8);
            padding: 40px;
            border-radius: 20px;
            border: 2px solid rgba(139, 92, 246, 0.3);
            margin-top: 40px;
        }}
        
        .reset-btn {{
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 1.1em;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 30px;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }}
        
        .reset-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5);
        }}
        
        .scenario-badges {{
            display: flex;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }}
        
        .scenario-btn {{
            background: rgba(59, 130, 246, 0.2);
            color: #E8E8E8;
            border: 2px solid #3B82F6;
            padding: 12px 25px;
            border-radius: 25px;
            font-size: 0.95em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .scenario-btn:hover {{
            background: rgba(59, 130, 246, 0.4);
            transform: scale(1.05);
        }}
        
        .scenario-btn.active {{
            background: linear-gradient(135deg, #3B82F6, #06FFA5);
            border-color: #06FFA5;
        }}
        
        /* Commission Calculator Styles */
        .commission-calculator {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
            padding: 50px;
            border-radius: 24px;
            border: 2px solid #8B5CF6;
            margin: 50px 0;
        }}
        
        .commission-calculator h2 {{
            color: #8B5CF6;
            font-size: 2em;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        .calc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-top: 40px;
        }}
        
        .calc-input-panel {{
            background: rgba(30, 30, 46, 0.9);
            padding: 35px;
            border-radius: 20px;
            border: 2px solid rgba(139, 92, 246, 0.3);
        }}
        
        .calc-result-panel {{
            background: rgba(30, 30, 46, 0.9);
            padding: 35px;
            border-radius: 20px;
            border: 2px solid rgba(6, 255, 165, 0.3);
        }}
        
        .calc-input-group {{
            margin-bottom: 30px;
        }}
        
        .calc-label {{
            display: block;
            color: #A0AEC0;
            font-size: 1em;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 600;
        }}
        
        .calc-input {{
            width: 100%;
            background: rgba(59, 130, 246, 0.1);
            border: 2px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 15px 20px;
            color: #E8E8E8;
            font-size: 1.3em;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            transition: all 0.3s;
        }}
        
        .calc-input:focus {{
            outline: none;
            border-color: #8B5CF6;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
        }}
        
        .calc-result {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, rgba(6, 255, 165, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
            border-radius: 16px;
            margin-bottom: 25px;
        }}
        
        .calc-result-label {{
            color: #A0AEC0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
        }}
        
        .calc-result-value {{
            color: #06FFA5;
            font-size: 3em;
            font-weight: 900;
            font-family: 'JetBrains Mono', monospace;
            text-shadow: 0 0 30px rgba(6, 255, 165, 0.5);
        }}
        
        .calc-breakdown {{
            background: rgba(59, 130, 246, 0.05);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #8B5CF6;
        }}
        
        .calc-breakdown-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(139, 92, 246, 0.2);
        }}
        
        .calc-breakdown-item:last-child {{
            border-bottom: none;
        }}
        
        .calc-tier {{
            background: rgba(139, 92, 246, 0.1);
            padding: 15px 20px;
            border-radius: 12px;
            margin: 10px 0;
            border-left: 4px solid #8B5CF6;
        }}
        
        .calc-tier.active {{
            background: rgba(6, 255, 165, 0.15);
            border-left-color: #06FFA5;
        }}
        
        @media (max-width: 1200px) {{
            .calc-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        ::-webkit-scrollbar {{
            width: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(26, 26, 46, 0.5);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            border-radius: 6px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #60A5FA, #A78BFA);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 FORUM PANORAMA - RAPORT ZARZĄDCZY</h1>
            <p class="subtitle">Analiza finansowa dla nowego managera | wrz.2024 – wrz.2025</p>
            <div class="meta">
                <span class="meta-badge">📅 {datetime.now().strftime('%d.%m.%Y | %H:%M')}</span>
                <span class="meta-badge">📈 13 okresów</span>
                <span class="meta-badge">🎯 Manager Edition</span>
            </div>
        </div>
        
        <div class="executive-summary">
            <h2>🎯 ONBOARDING DLA NOWEGO MANAGERA</h2>
            <p>
                <strong>Witamy w Forum Panorama!</strong> Ten raport został przygotowany specjalnie dla Ciebie,
                aby ułatwić start w nowej roli. Znajdziesz tu kompletną analizę finansową za ostatnie 13 miesięcy
                (wrz.2024 - wrz.2025), kluczowe wskaźniki oraz rekomendacje dla poprawy rentowności.
            </p>
            <div class="highlight">
                <p><strong>🎯 Twoje kluczowe cele:</strong></p>
                <p>
                    💰 Przychody (13 m-cy): <strong>{total_revenue:,.0f} PLN</strong><br>
                    📊 Wynik netto: <strong>{total_profit:,.0f} PLN</strong>
                    <span class="badge {'success' if total_profit > 0 else 'danger'}">
                        {'ZYSK' if total_profit > 0 else 'STRATA'}
                    </span><br>
                    📉 Marża: <strong>{margin:.2f}%</strong> 
                    <span class="badge warning">TARGET: +5%</span><br>
                    ✅ Rentowne okresy: <strong>{profitable_months}/{profitable_months + loss_months}</strong>
                    <span class="badge info">ZWIĘKSZ DO 100%</span>
                </p>
            </div>
        </div>
        
        <div class="critical-alert">
            <h2>⚠️ ZOBOWIĄZANIA KRYTYCZNE</h2>
            <ul>
                <li>💸 <strong>US VAT: 50,135 PLN</strong> – wymaga natychmiastowego uregulowania</li>
                <li>🏛️ <strong>ZUS (1. rata): 90,000 PLN</strong> – termin płatności priorytetowy</li>
                <li>💳 <strong>Suma zobowiązań: 816,730 PLN</strong> (US VAT + ZUS + kredyty)</li>
            </ul>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>II. KPI DASHBOARD</h2>
                <p class="section-intro">
                    Wskaźniki efektywności operacyjnej oraz kluczowe metryki finansowe
                </p>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>💰 Total Revenue</h3>
                        <div class="value">{total_revenue/1000000:.2f}M</div>
                        <div class="subtitle">Przychody netto<br>Avg: {avg_revenue:,.0f} PLN/mc</div>
                    </div>
                    
                    <div class="metric-card {'positive' if total_profit > 0 else 'negative'}">
                        <h3>📊 Net Profit/Loss</h3>
                        <div class="value">{total_profit/1000:.0f}K</div>
                        <div class="subtitle">{profitable_months} zyskowne | {loss_months} stratne</div>
                    </div>
                    
                    <div class="metric-card {'positive' if margin > 0 else 'negative'}">
                        <h3>📈 Net Margin</h3>
                        <div class="value">{margin:.1f}%</div>
                        <div class="subtitle">Rentowność sprzedaży</div>
                    </div>
                    
                    <div class="metric-card">
                        <h3>💸 Total Costs</h3>
                        <div class="value">{total_costs/1000000:.2f}M</div>
                        <div class="subtitle">Koszty operacyjne<br>Avg: {avg_costs:,.0f} PLN/mc</div>
                    </div>
                    
                    <div class="metric-card {'positive' if roi > 0 else 'negative'}">
                        <h3>🎯 ROI</h3>
                        <div class="value">{roi:.1f}%</div>
                        <div class="subtitle">Return on Investment</div>
                    </div>
                    
                    <div class="metric-card {'positive' if breakeven_coverage > 100 else 'warning'}">
                        <h3>⚖️ Cost Coverage</h3>
                        <div class="value">{breakeven_coverage:.0f}%</div>
                        <div class="subtitle">Przychód / Koszty</div>
                    </div>
                    
                    <div class="metric-card negative">
                        <h3>💳 Liabilities</h3>
                        <div class="value">817K</div>
                        <div class="subtitle">Zobowiązania bieżące</div>
                    </div>
                    
                    <div class="metric-card warning">
                        <h3>💡 Savings Potential</h3>
                        <div class="value">{sum(s['potential_savings'] for s in self.analysis.get('savings', [])):,.0f}</div>
                        <div class="subtitle">Szacunek roczny</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>III. DATA ANALYTICS</h2>
                
                <h3>3.1. Analiza Korelacji: Revenue vs Costs</h3>
                <p class="section-intro">
                    Scatter plot przedstawiający zależność między przychodami a kosztami operacyjnymi.
                    Niska korelacja wskazuje na wysokie koszty stałe.
                </p>
                <div class="chart-container">
                    <div id="revenue-chart"></div>
                </div>
                
                <h3>3.2. Trend Analysis: Revenue & Costs Dynamics</h3>
                <p class="section-intro">
                    Analiza trendów czasowych z identyfikacją sezonowości i stabilności finansowej.
                </p>
                <div class="chart-container">
                    <div id="trend-chart"></div>
                </div>
                
                <h3>3.3. Profitability Analysis: Monthly P&L</h3>
                <p class="section-intro">
                    Wynik finansowy netto w układzie czasowym (green = profit, pink = loss).
                </p>
                <div class="chart-container">
                    <div id="profit-chart"></div>
                </div>
                
                <h3>3.4. ZUS Obligations: Trend Overview</h3>
                <p class="section-intro">
                    Dynamika składek ZUS z wartością średnią jako benchmark.
                </p>
                <div class="chart-container">
                    <div id="zus-chart"></div>
                </div>
                
                <h3>3.5. 💼 Cost-Profit Analysis dla Managera</h3>
                <p class="section-intro">
                    Waterfall chart pokazujący strukturę rentowności - kluczowe narzędzie dla zarządzania kosztami.
                </p>
                <div class="chart-container">
                    <div id="cost-profit-chart"></div>
                </div>
                
                <h3>3.6. 📊 Rozbicie Kosztów Operacyjnych</h3>
                <p class="section-intro">
                    Struktura kosztów - zidentyfikuj największe możliwości optymalizacji.
                </p>
                <div class="chart-container">
                    <div id="cost-breakdown-chart"></div>
                </div>
            </div>
            
            <div class="commission-calculator">
                <h2>💰 PRZELICZNIK PROWIZJI OD WZROSTU</h2>
                <p style="text-align: center; color: #A0AEC0; margin-bottom: 30px; font-size: 1.1em;">
                    System motywacyjny dla managera - oblicz swoją prowizję na podstawie wzrostu przychodów
                </p>
                
                <div class="calc-grid">
                    <div class="calc-input-panel">
                        <h3 style="color: #8B5CF6; margin-top: 0;">📊 Wprowadź dane</h3>
                        
                        <div class="calc-input-group">
                            <label class="calc-label">Obecne przychody miesięczne (PLN)</label>
                            <input type="number" class="calc-input" id="current-revenue" 
                                   value="{avg_revenue:.0f}" step="1000">
                        </div>
                        
                        <div class="calc-input-group">
                            <label class="calc-label">Docelowe przychody miesięczne (PLN)</label>
                            <input type="number" class="calc-input" id="target-revenue" 
                                   value="{avg_revenue * 1.15:.0f}" step="1000">
                        </div>
                        
                        <div class="calc-breakdown">
                            <h4 style="color: #8B5CF6; margin-bottom: 15px;">📋 Progi prowizyjne:</h4>
                            <div class="calc-tier">
                                <strong>Tier 1:</strong> 0-10% wzrostu → 2% prowizji
                            </div>
                            <div class="calc-tier">
                                <strong>Tier 2:</strong> 10-20% wzrostu → 3% prowizji
                            </div>
                            <div class="calc-tier">
                                <strong>Tier 3:</strong> 20-30% wzrostu → 4% prowizji
                            </div>
                            <div class="calc-tier">
                                <strong>Tier 4:</strong> >30% wzrostu → 5% prowizji + bonus
                            </div>
                        </div>
                    </div>
                    
                    <div class="calc-result-panel">
                        <h3 style="color: #06FFA5; margin-top: 0;">💎 Twoja prowizja</h3>
                        
                        <div class="calc-result">
                            <div class="calc-result-label">Miesięczna prowizja</div>
                            <div class="calc-result-value" id="monthly-commission">0 PLN</div>
                        </div>
                        
                        <div class="calc-result">
                            <div class="calc-result-label">Roczna prowizja</div>
                            <div class="calc-result-value" id="annual-commission">0 PLN</div>
                        </div>
                        
                        <div class="calc-breakdown">
                            <h4 style="color: #06FFA5; margin-bottom: 15px;">📈 Szczegóły:</h4>
                            <div class="calc-breakdown-item">
                                <span>Wzrost przychodów:</span>
                                <strong id="revenue-growth">0%</strong>
                            </div>
                            <div class="calc-breakdown-item">
                                <span>Aktywny tier:</span>
                                <strong id="active-tier">-</strong>
                            </div>
                            <div class="calc-breakdown-item">
                                <span>Stawka prowizji:</span>
                                <strong id="commission-rate">0%</strong>
                            </div>
                            <div class="calc-breakdown-item">
                                <span>Przyrost miesięczny:</span>
                                <strong id="monthly-increase">0 PLN</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>IV. PLAN NAPRAWCZY DLA FORUM PANORAMA</h2>
                
                <div class="recommendations">
                    <h3>🎯 Action Plan - Priorytety dla Nowego Managera</h3>
                    
                    <div class="recommendation-item priority-high">
                        <h4>🔴 TYDZIEŃ 1-2: Immediate Actions</h4>
                        <p>
                            <strong>1. Analiza struktury kosztów:</strong> Przeprowadź szczegółowy audyt wszystkich 
                            kontraktów z dostawcami. Zidentyfikuj top 10 największych kosztów i przygotuj plan renegocjacji.
                            <strong>Target: -8% kosztów w 60 dni.</strong><br><br>
                            
                            <strong>2. Team Meeting & Goals:</strong> Spotkanie z zespołem - przedstaw cele finansowe,
                            system motywacyjny i KPI. Każdy pracownik musi znać swój wkład w osiągnięcie rentowności.
                            <strong>Target: 100% zespołu zaangażowane.</strong><br><br>
                            
                            <strong>3. Quick Wins - Menu Engineering:</strong> Analiza menu - usuń dania o najniższej 
                            marży, promuj high-margin items. Wprowadź "chef's recommendations" z 60%+ marżą.
                            <strong>Target: +5% średniego rachunku w 30 dni.</strong>
                        </p>
                    </div>
                    
                    <div class="recommendation-item priority-high">
                        <h4>🟠 MIESIĄC 1: Revenue Growth Initiatives</h4>
                        <p>
                            <strong>1. Marketing Blitz:</strong> Kampania 30-dniowa: social media, influencer partnerships,
                            Google Ads. Budget: 15k PLN. <strong>Expected ROI: 300% (45k przychodów).</strong><br><br>
                            
                            <strong>2. Upselling Program:</strong> Wdróż strukturę upselling dla kelnerów - bonus za sprzedaż
                            win premium, deserów, dodatków. <strong>Target: +12% średniego rachunku.</strong><br><br>
                            
                            <strong>3. Event Calendar:</strong> Zaplanuj 4 eventy tematyczne (degustacje, live music, 
                            business lunches). <strong>Target: +200 klientów/miesiąc.</strong>
                        </p>
                    </div>
                    
                    <div class="recommendation-item priority-medium">
                        <h4>🟡 MIESIĄC 2-3: Operational Excellence</h4>
                        <p>
                            <strong>1. Staff Optimization:</strong> Wprowadź elastyczny scheduling - więcej personelu 
                            w peak hours, mniej w slow periods. <strong>Target: -15% kosztów pracowniczych.</strong><br><br>
                            
                            <strong>2. Supplier Renegotiation:</strong> Zakończ renegocjacje - zmień dostawców jeśli 
                            konieczne. Priorytet: wino (30% kosztów), mięso (25%), warzywa (15%).
                            <strong>Target: -10% kosztów zakupu.</strong><br><br>
                            
                            <strong>3. Waste Reduction:</strong> Implementuj system zarządzania odpadami, daily inventory checks.
                            <strong>Target: -20% food waste = +8k PLN/miesiąc.</strong>
                        </p>
                    </div>
                    
                    <div class="recommendation-item priority-medium">
                        <h4>🟢 KWARTAŁ 2: Growth & Scale</h4>
                        <p>
                            <strong>1. Loyalty Program:</strong> Wdróż program lojalnościowy - zbieraj dane klientów,
                            personalizuj oferty. <strong>Target: 30% returning customers.</strong><br><br>
                            
                            <strong>2. Catering/Delivery Expansion:</strong> Rozszerz ofertę catering dla firm, 
                            dostawa premium. Nowy stream przychodów. <strong>Target: +50k PLN/miesiąc.</strong><br><br>
                            
                            <strong>3. Partnership Deals:</strong> Współpraca z hotelami, biurami, eventami w okolicy.
                            <strong>Target: +100 klientów korporacyjnych.</strong>
                        </p>
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, rgba(6, 255, 165, 0.1), rgba(59, 130, 246, 0.1)); 
                           padding: 40px; border-radius: 20px; margin-top: 40px; border: 2px solid #06FFA5;">
                    <h3 style="color: #06FFA5; text-align: center; margin-bottom: 20px;">
                        🎯 TWOJE CELE NA PIERWSZE 90 DNI
                    </h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                        <div style="text-align: center; padding: 20px; background: rgba(30,30,46,0.6); border-radius: 12px;">
                            <div style="font-size: 2em; color: #06FFA5; font-weight: 900;">+15%</div>
                            <div style="color: #A0AEC0;">Wzrost przychodów</div>
                        </div>
                        <div style="text-align: center; padding: 20px; background: rgba(30,30,46,0.6); border-radius: 12px;">
                            <div style="font-size: 2em; color: #06FFA5; font-weight: 900;">-12%</div>
                            <div style="color: #A0AEC0;">Redukcja kosztów</div>
                        </div>
                        <div style="text-align: center; padding: 20px; background: rgba(30,30,46,0.6); border-radius: 12px;">
                            <div style="font-size: 2em; color: #06FFA5; font-weight: 900;">+8%</div>
                            <div style="color: #A0AEC0;">Marża netto</div>
                        </div>
                        <div style="text-align: center; padding: 20px; background: rgba(30,30,46,0.6); border-radius: 12px;">
                            <div style="font-size: 2em; color: #06FFA5; font-weight: 900;">100%</div>
                            <div style="color: #A0AEC0;">Miesiące zyskowne</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="simulator-section">
                <h2>🚀 INTERACTIVE INVESTMENT SIMULATOR</h2>
                <p class="simulator-intro">
                    Przesuń suwaki, aby zobaczyć potencjalny wpływ optymalizacji na wyniki finansowe przedsiębiorstwa.
                    Symulator pokazuje realistyczne scenariusze rozwoju przy różnych założeniach strategicznych.
                </p>
                
                <div class="scenario-badges">
                    <button class="scenario-btn" onclick="applyScenario('conservative')">📊 Konserwatywny</button>
                    <button class="scenario-btn" onclick="applyScenario('moderate')">📈 Umiarkowany</button>
                    <button class="scenario-btn" onclick="applyScenario('aggressive')">🚀 Agresywny</button>
                    <button class="scenario-btn" onclick="applyScenario('breakeven')">⚖️ Break-even</button>
                </div>
                        </p>
                    </div>
                    
                    <div class="recommendation-item priority-high">
                        <h4>🟠 HIGH PRIORITY (1-3 months)</h4>
                        <p>
                            <strong>1. Cost Optimization:</strong> Redukcja kosztów o 10-15% poprzez renegocjację kontraktów
                            i eliminację marnotrawstwa.<br><br>
                            <strong>2. Revenue Growth:</strong> Strategia upselling/cross-selling. Target: +10-12% avg ticket.
                        </p>
                    </div>
                    
                    <div class="recommendation-item priority-medium">
                        <h4>🟡 MEDIUM (3-6 months)</h4>
                        <p>
                            <strong>1. ZUS Restructuring:</strong> Finalizacja układu ratalnego (-517k PLN) na 24-36 m-cy.<br><br>
                            <strong>2. HR Optimization:</strong> Analiza efektywności zespołu, outsourcing funkcji wsparcia.
                        </p>
                    </div>
                    
                    <div class="recommendation-item priority-medium">
                        <h4>🟢 LONG-TERM (6-12 months)</h4>
                        <p>
                            <strong>1. Diversification:</strong> Nowe produkty premium, ekspansja kanałowa.<br><br>
                            <strong>2. Tax Optimization:</strong> Kompleksowy przegląd struktury podatkowej z doradcą.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="simulator-section">
                <h2>🚀 INTERACTIVE INVESTMENT SIMULATOR</h2>
                <p class="simulator-intro">
                    Przesuń suwaki, aby zobaczyć potencjalny wpływ optymalizacji na wyniki finansowe przedsiębiorstwa.
                    Symulator pokazuje realistyczne scenariusze rozwoju przy różnych założeniach strategicznych.
                </p>
                
                <div class="scenario-badges">
                    <button class="scenario-btn" onclick="applyScenario('conservative')">📊 Konserwatywny</button>
                    <button class="scenario-btn" onclick="applyScenario('moderate')">📈 Umiarkowany</button>
                    <button class="scenario-btn" onclick="applyScenario('aggressive')">🚀 Agresywny</button>
                    <button class="scenario-btn" onclick="applyScenario('breakeven')">⚖️ Break-even</button>
                </div>
                
                <div class="simulator-grid">
                    <div class="controls-panel">
                        <h3 style="margin-top: 0; color: #3B82F6;">⚙️ Parametry Optymalizacji</h3>
                        
                        <div class="control-group">
                            <div class="control-label">
                                <span>📈 Wzrost przychodów</span>
                                <span class="control-value" id="revenue-value">+0%</span>
                            </div>
                            <input type="range" min="-20" max="50" value="0" step="1" class="slider" id="revenue-slider">
                            <small style="color: #718096; font-size: 0.85em;">
                                Wzrost sprzedaży poprzez marketing, upselling, nowe produkty
                            </small>
                        </div>
                        
                        <div class="control-group">
                            <div class="control-label">
                                <span>💰 Redukcja kosztów operacyjnych</span>
                                <span class="control-value" id="costs-value">-0%</span>
                            </div>
                            <input type="range" min="0" max="30" value="0" step="1" class="slider" id="costs-slider">
                            <small style="color: #718096; font-size: 0.85em;">
                                Optymalizacja procesów, renegocjacja umów, eliminacja marnotrawstwa
                            </small>
                        </div>
                        
                        <div class="control-group">
                            <div class="control-label">
                                <span>📊 Wzrost średniego rachunku</span>
                                <span class="control-value" id="ticket-value">+0%</span>
                            </div>
                            <input type="range" min="0" max="40" value="0" step="1" class="slider" id="ticket-slider">
                            <small style="color: #718096; font-size: 0.85em;">
                                Cross-selling, premium menu, dodatki, wyższa jakość obsługi
                            </small>
                        </div>
                        
                        <div class="control-group">
                            <div class="control-label">
                                <span>👥 Optymalizacja zatrudnienia</span>
                                <span class="control-value" id="labor-value">-0%</span>
                            </div>
                            <input type="range" min="0" max="25" value="0" step="1" class="slider" id="labor-slider">
                            <small style="color: #718096; font-size: 0.85em;">
                                Automatyzacja, outsourcing, efektywniejszy scheduling
                            </small>
                        </div>
                        
                        <div class="control-group">
                            <div class="control-label">
                                <span>🏛️ Redukcja zobowiązań ZUS</span>
                                <span class="control-value" id="zus-value">-0%</span>
                            </div>
                            <input type="range" min="0" max="20" value="0" step="1" class="slider" id="zus-slider">
                            <small style="color: #718096; font-size: 0.85em;">
                                Optymalizacja zatrudnienia, umowy B2B, restrukturyzacja
                            </small>
                        </div>
                        
                        <button class="reset-btn" onclick="resetSimulator()">🔄 RESET</button>
                    </div>
                    
                    <div class="results-panel">
                        <h3 style="margin-top: 0; color: #06FFA5;">📊 Prognoza Wyników (Miesięcznie)</h3>
                        
                        <div class="result-card">
                            <div class="result-title">Przychody Netto (Średnio)</div>
                            <div class="result-value" id="new-revenue">{avg_revenue:,.0f} PLN</div>
                            <div class="result-change" id="revenue-change">Bez zmian</div>
                        </div>
                        
                        <div class="result-card">
                            <div class="result-title">Koszty Operacyjne (Średnio)</div>
                            <div class="result-value" id="new-costs">{avg_costs:,.0f} PLN</div>
                            <div class="result-change" id="costs-change">Bez zmian</div>
                        </div>
                        
                        <div class="result-card" id="profit-card">
                            <div class="result-title">Wynik Netto (Średnio)</div>
                            <div class="result-value" id="new-profit">{total_profit/14:,.0f} PLN</div>
                            <div class="result-change" id="profit-change">Bez zmian</div>
                        </div>
                        
                        <div class="result-card">
                            <div class="result-title">Marża Netto</div>
                            <div class="result-value" id="new-margin">{margin:.2f}%</div>
                            <div class="result-change" id="margin-change">Bez zmian</div>
                        </div>
                        
                        <div class="result-card positive">
                            <div class="result-title">Potencjał Roczny</div>
                            <div class="result-value" id="annual-potential">0 PLN</div>
                            <div class="result-change positive">Dodatkowy zysk vs. obecny stan</div>
                        </div>
                    </div>
                </div>
                
                <div class="forecast-chart">
                    <h3 style="margin-top: 0; text-align: center;">📈 Projekcja 12-miesięczna</h3>
                    <div id="forecast-chart"></div>
                </div>
            </div>
            
            <div class="section">
                <h2>V. CONCLUSION</h2>
                <p style="font-size: 1.15em; line-height: 1.9; color: #CBD5E0;">
                    FP HOLDING wymaga natychmiastowych działań naprawczych w obszarze płynności finansowej
                    oraz optymalizacji struktury kosztowej. Wysoki udział kosztów stałych (niska korelacja
                    z przychodami) stanowi główne wyzwanie operacyjne.
                </p>
                <p style="font-size: 1.15em; line-height: 1.9; color: #CBD5E0; margin-top: 20px;">
                    Implementacja zaproponowanego planu może przynieść oszczędności rzędu 
                    <strong style="color: #06FFA5;">{sum(s['potential_savings'] for s in self.analysis.get('savings', [])):,.0f} PLN rocznie</strong>
                    oraz poprawić wskaźniki rentowności o 8-12 p.p. w perspektywie 12 miesięcy.
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>FP HOLDING - Financial Analytics Dashboard</strong></p>
            <p>Confidential Report | © {datetime.now().year} | All Rights Reserved</p>
            <p style="font-size: 0.85em; margin-top: 20px; color: #718096;">
                Data source: Accounting system sie.2024 – wrz.2025 | 14 billing periods<br>
                Generated with Python + Plotly | Modern Dark Theme
            </p>
        </div>
    </div>
    
    <script>
        // Render charts with dark theme
        Plotly.newPlot("revenue-chart", JSON.parse('{revenue_chart}'));
        Plotly.newPlot("trend-chart", JSON.parse('{trend_chart}'));
        Plotly.newPlot("profit-chart", JSON.parse('{profit_chart}'));
        Plotly.newPlot("zus-chart", JSON.parse('{zus_chart}'));
        Plotly.newPlot("cost-profit-chart", JSON.parse('{cost_profit_chart}'));
        Plotly.newPlot("cost-breakdown-chart", JSON.parse('{cost_breakdown_chart}'));
        
        // Responsive resize
        window.addEventListener('resize', function() {{
            Plotly.Plots.resize('revenue-chart');
            Plotly.Plots.resize('trend-chart');
            Plotly.Plots.resize('profit-chart');
            Plotly.Plots.resize('zus-chart');
            Plotly.Plots.resize('cost-profit-chart');
            Plotly.Plots.resize('cost-breakdown-chart');
        }});
        
        // Fade-in animations on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        document.querySelectorAll('.section, .metric-card, .chart-container').forEach(el => {{
            observer.observe(el);
        }});
        
        // Investment Simulator Logic
        const baseData = {{
            avgRevenue: {avg_revenue},
            avgCosts: {avg_costs},
            avgProfit: {total_profit/14},
            margin: {margin}
        }};
        
        let currentParams = {{
            revenueGrowth: 0,
            costReduction: 0,
            ticketIncrease: 0,
            laborReduction: 0,
            zusReduction: 0
        }};
        
        // Slider event listeners
        const sliders = {{
            revenue: document.getElementById('revenue-slider'),
            costs: document.getElementById('costs-slider'),
            ticket: document.getElementById('ticket-slider'),
            labor: document.getElementById('labor-slider'),
            zus: document.getElementById('zus-slider')
        }};
        
        sliders.revenue.addEventListener('input', (e) => {{
            currentParams.revenueGrowth = parseInt(e.target.value);
            document.getElementById('revenue-value').textContent = (currentParams.revenueGrowth >= 0 ? '+' : '') + currentParams.revenueGrowth + '%';
            updateSimulation();
        }});
        
        sliders.costs.addEventListener('input', (e) => {{
            currentParams.costReduction = parseInt(e.target.value);
            document.getElementById('costs-value').textContent = '-' + currentParams.costReduction + '%';
            updateSimulation();
        }});
        
        sliders.ticket.addEventListener('input', (e) => {{
            currentParams.ticketIncrease = parseInt(e.target.value);
            document.getElementById('ticket-value').textContent = '+' + currentParams.ticketIncrease + '%';
            updateSimulation();
        }});
        
        sliders.labor.addEventListener('input', (e) => {{
            currentParams.laborReduction = parseInt(e.target.value);
            document.getElementById('labor-value').textContent = '-' + currentParams.laborReduction + '%';
            updateSimulation();
        }});
        
        sliders.zus.addEventListener('input', (e) => {{
            currentParams.zusReduction = parseInt(e.target.value);
            document.getElementById('zus-value').textContent = '-' + currentParams.zusReduction + '%';
            updateSimulation();
        }});
        
        function updateSimulation() {{
            // Calculate new values
            const revenueMultiplier = 1 + (currentParams.revenueGrowth / 100) + (currentParams.ticketIncrease / 100);
            const costMultiplier = 1 - (currentParams.costReduction / 100) - (currentParams.laborReduction / 100 * 0.4) - (currentParams.zusReduction / 100 * 0.15);
            
            const newRevenue = baseData.avgRevenue * revenueMultiplier;
            const newCosts = baseData.avgCosts * costMultiplier;
            const newProfit = newRevenue - newCosts;
            const newMargin = (newProfit / newRevenue) * 100;
            
            const revenueChange = newRevenue - baseData.avgRevenue;
            const costsChange = newCosts - baseData.avgCosts;
            const profitChange = newProfit - baseData.avgProfit;
            const marginChange = newMargin - baseData.margin;
            const annualPotential = profitChange * 12;
            
            // Update UI
            document.getElementById('new-revenue').textContent = formatNumber(newRevenue) + ' PLN';
            document.getElementById('new-costs').textContent = formatNumber(newCosts) + ' PLN';
            document.getElementById('new-profit').textContent = formatNumber(newProfit) + ' PLN';
            document.getElementById('new-margin').textContent = newMargin.toFixed(2) + '%';
            document.getElementById('annual-potential').textContent = formatNumber(annualPotential) + ' PLN';
            
            // Update change indicators
            updateChangeIndicator('revenue-change', revenueChange, ' PLN/mc');
            updateChangeIndicator('costs-change', costsChange, ' PLN/mc');
            updateChangeIndicator('profit-change', profitChange, ' PLN/mc');
            updateChangeIndicator('margin-change', marginChange, ' p.p.');
            
            // Update profit card color
            const profitCard = document.getElementById('profit-card');
            if (newProfit > 0) {{
                profitCard.classList.add('positive');
                profitCard.classList.remove('negative');
            }} else {{
                profitCard.classList.add('negative');
                profitCard.classList.remove('positive');
            }}
            
            // Update forecast chart
            updateForecastChart(newRevenue, newCosts, newProfit);
        }}
        
        function updateChangeIndicator(elementId, change, unit) {{
            const element = document.getElementById(elementId);
            const sign = change >= 0 ? '+' : '';
            element.textContent = sign + formatNumber(change) + unit;
            
            if (change > 0) {{
                element.classList.add('positive');
                element.classList.remove('negative');
            }} else if (change < 0) {{
                element.classList.add('negative');
                element.classList.remove('positive');
            }} else {{
                element.classList.remove('positive', 'negative');
            }}
        }}
        
        function formatNumber(num) {{
            return Math.round(num).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ',');
        }}
        
        function updateForecastChart(avgRevenue, avgCosts, avgProfit) {{
            const months = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12'];
            
            // Add some variance to make it realistic
            const revenues = months.map((m, i) => avgRevenue * (1 + (Math.sin(i * 0.5) * 0.08)));
            const costs = months.map((m, i) => avgCosts * (1 + (Math.sin(i * 0.3) * 0.04)));
            const profits = revenues.map((r, i) => r - costs[i]);
            
            const trace1 = {{
                x: months,
                y: revenues,
                name: 'Przychody',
                type: 'scatter',
                mode: 'lines+markers',
                line: {{ color: '#06FFA5', width: 3, shape: 'spline' }},
                marker: {{ size: 10, color: '#06FFA5' }},
                fill: 'tozeroy',
                fillcolor: 'rgba(6, 255, 165, 0.1)'
            }};
            
            const trace2 = {{
                x: months,
                y: costs,
                name: 'Koszty',
                type: 'scatter',
                mode: 'lines+markers',
                line: {{ color: '#F59E0B', width: 3, shape: 'spline' }},
                marker: {{ size: 10, color: '#F59E0B' }},
                fill: 'tozeroy',
                fillcolor: 'rgba(245, 158, 11, 0.1)'
            }};
            
            const trace3 = {{
                x: months,
                y: profits,
                name: 'Zysk/Strata',
                type: 'bar',
                marker: {{
                    color: profits.map(p => p > 0 ? '#06FFA5' : '#FF006E')
                }}
            }};
            
            const layout = {{
                title: {{
                    text: 'Symulacja 12-miesięczna przy obecnych parametrach',
                    font: {{ size: 18, color: '#E8E8E8' }}
                }},
                xaxis: {{ 
                    title: 'Miesiąc',
                    color: '#E8E8E8',
                    gridcolor: 'rgba(255,255,255,0.1)'
                }},
                yaxis: {{ 
                    title: 'Wartość (PLN)',
                    color: '#E8E8E8',
                    gridcolor: 'rgba(255,255,255,0.1)'
                }},
                template: 'plotly_dark',
                paper_bgcolor: 'rgba(30, 30, 46, 0.5)',
                plot_bgcolor: 'rgba(30, 30, 46, 0.3)',
                font: {{ family: 'Inter', color: '#E8E8E8' }},
                showlegend: true,
                legend: {{
                    bgcolor: 'rgba(30, 30, 46, 0.9)',
                    bordercolor: '#3B82F6',
                    borderwidth: 1
                }},
                hovermode: 'x unified'
            }};
            
            Plotly.newPlot('forecast-chart', [trace1, trace2, trace3], layout, {{ responsive: true }});
        }}
        
        function resetSimulator() {{
            currentParams = {{
                revenueGrowth: 0,
                costReduction: 0,
                ticketIncrease: 0,
                laborReduction: 0,
                zusReduction: 0
            }};
            
            sliders.revenue.value = 0;
            sliders.costs.value = 0;
            sliders.ticket.value = 0;
            sliders.labor.value = 0;
            sliders.zus.value = 0;
            
            document.getElementById('revenue-value').textContent = '+0%';
            document.getElementById('costs-value').textContent = '-0%';
            document.getElementById('ticket-value').textContent = '+0%';
            document.getElementById('labor-value').textContent = '-0%';
            document.getElementById('zus-value').textContent = '-0%';
            
            updateSimulation();
        }}
        
        function applyScenario(scenario) {{
            // Remove active class from all buttons
            document.querySelectorAll('.scenario-btn').forEach(btn => btn.classList.remove('active'));
            
            switch(scenario) {{
                case 'conservative':
                    currentParams = {{ revenueGrowth: 5, costReduction: 8, ticketIncrease: 5, laborReduction: 5, zusReduction: 3 }};
                    event.target.classList.add('active');
                    break;
                case 'moderate':
                    currentParams = {{ revenueGrowth: 12, costReduction: 15, ticketIncrease: 12, laborReduction: 10, zusReduction: 8 }};
                    event.target.classList.add('active');
                    break;
                case 'aggressive':
                    currentParams = {{ revenueGrowth: 25, costReduction: 22, ticketIncrease: 20, laborReduction: 18, zusReduction: 15 }};
                    event.target.classList.add('active');
                    break;
                case 'breakeven':
                    // Calculate what's needed for break-even
                    const neededReduction = Math.ceil((Math.abs(baseData.avgProfit) / baseData.avgCosts) * 100);
                    currentParams = {{ revenueGrowth: 0, costReduction: Math.min(neededReduction, 30), ticketIncrease: 0, laborReduction: 0, zusReduction: 0 }};
                    event.target.classList.add('active');
                    break;
            }}
            
            // Update sliders
            sliders.revenue.value = currentParams.revenueGrowth;
            sliders.costs.value = currentParams.costReduction;
            sliders.ticket.value = currentParams.ticketIncrease;
            sliders.labor.value = currentParams.laborReduction;
            sliders.zus.value = currentParams.zusReduction;
            
            // Update displays
            document.getElementById('revenue-value').textContent = (currentParams.revenueGrowth >= 0 ? '+' : '') + currentParams.revenueGrowth + '%';
            document.getElementById('costs-value').textContent = '-' + currentParams.costReduction + '%';
            document.getElementById('ticket-value').textContent = '+' + currentParams.ticketIncrease + '%';
            document.getElementById('labor-value').textContent = '-' + currentParams.laborReduction + '%';
            document.getElementById('zus-value').textContent = '-' + currentParams.zusReduction + '%';
            
            updateSimulation();
        }}
        
        // Initialize forecast chart
        updateForecastChart(baseData.avgRevenue, baseData.avgCosts, baseData.avgProfit);
        
        // Commission Calculator Logic
        const currentRevenueInput = document.getElementById('current-revenue');
        const targetRevenueInput = document.getElementById('target-revenue');
        
        function calculateCommission() {{
            const currentRevenue = parseFloat(currentRevenueInput.value) || 0;
            const targetRevenue = parseFloat(targetRevenueInput.value) || 0;
            
            const increase = targetRevenue - currentRevenue;
            const growthPercent = (increase / currentRevenue) * 100;
            
            let commissionRate = 0;
            let tierName = 'Brak';
            
            if (growthPercent > 30) {{
                commissionRate = 5;
                tierName = 'Tier 4 (>30%)';
            }} else if (growthPercent > 20) {{
                commissionRate = 4;
                tierName = 'Tier 3 (20-30%)';
            }} else if (growthPercent > 10) {{
                commissionRate = 3;
                tierName = 'Tier 2 (10-20%)';
            }} else if (growthPercent > 0) {{
                commissionRate = 2;
                tierName = 'Tier 1 (0-10%)';
            }}
            
            const monthlyCommission = increase * (commissionRate / 100);
            const annualCommission = monthlyCommission * 12;
            
            // Update UI
            document.getElementById('monthly-commission').textContent = formatNumber(monthlyCommission) + ' PLN';
            document.getElementById('annual-commission').textContent = formatNumber(annualCommission) + ' PLN';
            document.getElementById('revenue-growth').textContent = growthPercent.toFixed(1) + '%';
            document.getElementById('active-tier').textContent = tierName;
            document.getElementById('commission-rate').textContent = commissionRate + '%';
            document.getElementById('monthly-increase').textContent = formatNumber(increase) + ' PLN';
            
            // Highlight active tier
            document.querySelectorAll('.calc-tier').forEach((tier, index) => {{
                tier.classList.remove('active');
                if (commissionRate === 2 && index === 0) tier.classList.add('active');
                if (commissionRate === 3 && index === 1) tier.classList.add('active');
                if (commissionRate === 4 && index === 2) tier.classList.add('active');
                if (commissionRate === 5 && index === 3) tier.classList.add('active');
            }});
        }}
        
        currentRevenueInput.addEventListener('input', calculateCommission);
        targetRevenueInput.addEventListener('input', calculateCommission);
        
        // Initial calculation
        calculateCommission();
    </script>
</body>
</html>
"""
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html, encoding='utf-8')
        
        print(f"✅ Nowoczesny raport: {output_path}")
        return str(output_file)
