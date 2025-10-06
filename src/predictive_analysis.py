"""Moduł analizy predykcyjnej i prognozowania"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


def analyze_seasonality(monthly_data: List[Dict]) -> Dict:
    """Analiza sezonowości w danych sprzedażowych"""
    if len(monthly_data) < 6:
        return {"seasonality_detected": False, "message": "Za mało danych do analizy sezonowości"}
    
    df = pd.DataFrame(monthly_data)
    df['month_num'] = pd.to_datetime(df['month_year'] + '-01').dt.month
    
    # Grupuj po miesiącach kalendarzowych
    seasonal_pattern = df.groupby('month_num')['revenue'].mean().to_dict()
    
    # Znajdź najlepsze i najgorsze miesiące
    best_months = sorted(seasonal_pattern.items(), key=lambda x: x[1], reverse=True)[:3]
    worst_months = sorted(seasonal_pattern.items(), key=lambda x: x[1])[:3]
    
    month_names = {1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec',
                   7: 'Lipiec', 8: 'Sierpień', 9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'}
    
    return {
        "seasonality_detected": True,
        "seasonal_pattern": seasonal_pattern,
        "best_months": [(month_names[m], v) for m, v in best_months],
        "worst_months": [(month_names[m], v) for m, v in worst_months],
        "seasonal_variance": np.var(list(seasonal_pattern.values()))
    }


def calculate_trend_analysis(monthly_data: List[Dict]) -> Dict:
    """Oblicza trend i tempo zmian"""
    if len(monthly_data) < 3:
        return {"trend": "insufficient_data"}
    
    df = pd.DataFrame(monthly_data)
    df = df.sort_values('month_year')
    
    # Oblicz trend liniowy
    x = np.arange(len(df))
    revenue_trend = np.polyfit(x, df['revenue'], 1)[0]
    orders_trend = np.polyfit(x, df['amount'], 1)[0]
    avg_order_trend = np.polyfit(x, df['avg_order_value'], 1)[0]
    
    # Tempo zmian (miesięczne)
    revenue_change_rate = (df['revenue'].iloc[-1] - df['revenue'].iloc[0]) / len(df) / df['revenue'].iloc[0] * 100
    
    # Volatility (odchylenie standardowe)
    revenue_volatility = df['revenue'].std() / df['revenue'].mean() * 100
    
    return {
        "revenue_trend": revenue_trend,
        "revenue_trend_direction": "rosnący" if revenue_trend > 0 else "spadkowy",
        "orders_trend": orders_trend,
        "avg_order_trend": avg_order_trend,
        "monthly_change_rate": revenue_change_rate,
        "volatility": revenue_volatility,
        "trend_strength": "silny" if abs(revenue_change_rate) > 5 else "umiarkowany" if abs(revenue_change_rate) > 2 else "słaby"
    }


def forecast_next_months(monthly_data: List[Dict], months_ahead: int = 6) -> Dict:
    """Prognoza na następne miesiące"""
    if len(monthly_data) < 3:
        return {"forecast": [], "message": "Za mało danych do prognozy"}
    
    df = pd.DataFrame(monthly_data)
    df = df.sort_values('month_year')
    
    # Prosta prognoza liniowa
    x = np.arange(len(df))
    revenue_coef = np.polyfit(x, df['revenue'], 1)
    orders_coef = np.polyfit(x, df['amount'], 1)
    
    forecasts = []
    last_date = pd.to_datetime(df['month_year'].iloc[-1] + '-01')
    
    for i in range(1, months_ahead + 1):
        next_month = last_date + pd.DateOffset(months=i)
        month_index = len(df) + i - 1
        
        # Prognoza z trendem
        predicted_revenue = revenue_coef[0] * month_index + revenue_coef[1]
        predicted_orders = max(1, int(orders_coef[0] * month_index + orders_coef[1]))
        predicted_avg = predicted_revenue / predicted_orders if predicted_orders > 0 else 0
        
        # Dodaj element sezonowości jeśli jest wystarczająco danych
        seasonal_factor = 1.0
        if len(df) >= 6:
            month_num = next_month.month
            historical_same_month = df[pd.to_datetime(df['month_year'] + '-01').dt.month == month_num]
            if not historical_same_month.empty:
                avg_revenue = df['revenue'].mean()
                seasonal_factor = historical_same_month['revenue'].mean() / avg_revenue if avg_revenue > 0 else 1.0
        
        predicted_revenue *= seasonal_factor
        
        forecasts.append({
            "month": next_month.strftime('%B %Y'),
            "month_year": next_month.strftime('%Y-%m'),
            "predicted_revenue": max(0, predicted_revenue),
            "predicted_orders": predicted_orders,
            "predicted_avg_order": predicted_avg * seasonal_factor,
            "confidence": "wysoka" if i <= 3 else "średnia" if i <= 6 else "niska"
        })
    
    return {
        "forecasts": forecasts,
        "total_predicted_revenue": sum(f["predicted_revenue"] for f in forecasts),
        "forecast_period": f"{forecasts[0]['month']} - {forecasts[-1]['month']}"
    }


def identify_risk_factors(monthly_data: List[Dict], profitability_data: List[Dict] = None) -> List[Dict]:
    """Identyfikuje czynniki ryzyka w biznesie"""
    risks = []
    
    if len(monthly_data) < 2:
        return [{"risk": "Niewystarczające dane", "severity": "high", "description": "Za mało danych historycznych do analizy ryzyka"}]
    
    df = pd.DataFrame(monthly_data)
    df = df.sort_values('month_year')
    
    # Ryzyko spadku przychodów
    if len(df) >= 3:
        last_3_months = df.tail(3)
        if last_3_months['revenue'].is_monotonic_decreasing:
            risks.append({
                "risk": "Spadek przychodów",
                "severity": "high",
                "description": f"Przychody spadają przez {len(last_3_months)} miesięcy z rzędu",
                "impact": "Bezpośredni wpływ na rentowność"
            })
    
    # Ryzyko wysokiej zmienności
    revenue_cv = df['revenue'].std() / df['revenue'].mean()
    if revenue_cv > 0.2:
        risks.append({
            "risk": "Wysoka zmienność przychodów",
            "severity": "medium",
            "description": f"Współczynnik zmienności: {revenue_cv:.2f}",
            "impact": "Trudność w planowaniu i prognozowaniu"
        })
    
    # Ryzyko spadku średniej wartości zamówienia
    if df['avg_order_value'].iloc[-1] < df['avg_order_value'].mean() * 0.9:
        risks.append({
            "risk": "Spadek średniej wartości rachunku",
            "severity": "medium",
            "description": "Obecna średnia jest o >10% niższa od historycznej",
            "impact": "Wymaga zwiększenia liczby klientów dla utrzymania przychodów"
        })
    
    # Analiza rentowności jeśli dostępna
    if profitability_data:
        profit_df = pd.DataFrame(profitability_data)
        negative_months = len(profit_df[profit_df['profit_brutto'] < 0])
        if negative_months > len(profit_df) * 0.3:
            risks.append({
                "risk": "Częste straty miesięczne",
                "severity": "high",
                "description": f"{negative_months} z {len(profit_df)} miesięcy było stratnych",
                "impact": "Zagrożenie dla długoterminowej stabilności finansowej"
            })
    
    return risks


def generate_growth_scenarios(monthly_data: List[Dict]) -> Dict:
    """Generuje scenariusze wzrostu"""
    if len(monthly_data) < 3:
        return {"scenarios": []}
    
    df = pd.DataFrame(monthly_data)
    current_avg_revenue = df['revenue'].mean()
    current_avg_orders = df['amount'].mean()
    current_avg_order_value = df['avg_order_value'].mean()
    
    scenarios = [
        {
            "name": "Scenariusz Konserwatywny",
            "description": "Wzrost o 5% rocznie",
            "monthly_growth_rate": 0.4,  # ~5% rocznie
            "projected_annual_revenue": current_avg_revenue * 12 * 1.05,
            "key_actions": ["Utrzymanie obecnej jakości", "Optymalizacja kosztów", "Stabilna promocja"]
        },
        {
            "name": "Scenariusz Umiarkowany", 
            "description": "Wzrost o 15% rocznie",
            "monthly_growth_rate": 1.2,  # ~15% rocznie
            "projected_annual_revenue": current_avg_revenue * 12 * 1.15,
            "key_actions": ["Nowe pozycje menu", "Program lojalnościowy", "Marketing cyfrowy"]
        },
        {
            "name": "Scenariusz Agresywny",
            "description": "Wzrost o 30% rocznie", 
            "monthly_growth_rate": 2.3,  # ~30% rocznie
            "projected_annual_revenue": current_avg_revenue * 12 * 1.30,
            "key_actions": ["Rozszerzenie godzin", "Eventy i imprezy", "Partnerstwa biznesowe", "Catering"]
        }
    ]
    
    return {"scenarios": scenarios, "current_annual_projection": current_avg_revenue * 12}


def comprehensive_predictive_analysis(monthly_data: List[Dict], profitability_data: List[Dict] = None) -> Dict:
    """Kompleksowa analiza predykcyjna"""
    return {
        "seasonality": analyze_seasonality(monthly_data),
        "trends": calculate_trend_analysis(monthly_data),
        "forecast": forecast_next_months(monthly_data, 6),
        "risks": identify_risk_factors(monthly_data, profitability_data),
        "growth_scenarios": generate_growth_scenarios(monthly_data),
        "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }