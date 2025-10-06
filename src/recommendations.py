"""Moduł generowania rekomendacji strategicznych"""
from typing import Dict, List
import pandas as pd


def analyze_performance_gaps(monthly_data: List[Dict], profitability_data: List[Dict] = None) -> List[Dict]:
    """Identyfikuje luki w wydajności"""
    gaps = []
    
    if not monthly_data:
        return gaps
    
    df = pd.DataFrame(monthly_data)
    
    # Gap 1: Niska średnia wartość zamówienia
    avg_order_value = df['avg_order_value'].mean()
    if avg_order_value < 250:  # Benchmark dla restauracji premium
        gaps.append({
            "gap": "Niska średnia wartość rachunku",
            "current_value": avg_order_value,
            "target_value": 280,
            "potential_impact": "Wzrost przychodów o 12-15%",
            "priority": "high"
        })
    
    # Gap 2: Niestabilne przychody
    revenue_cv = df['revenue'].std() / df['revenue'].mean()
    if revenue_cv > 0.15:
        gaps.append({
            "gap": "Wysoka zmienność przychodów",
            "current_value": revenue_cv,
            "target_value": 0.10,
            "potential_impact": "Lepsza przewidywalność cash flow",
            "priority": "medium"
        })
    
    # Gap 3: Analiza rentowności
    if profitability_data:
        profit_df = pd.DataFrame(profitability_data)
        avg_margin = profit_df['margin_brutto'].mean()
        if avg_margin < 15:  # Benchmark dla gastronomii
            gaps.append({
                "gap": "Niska marża zysku",
                "current_value": avg_margin,
                "target_value": 20,
                "potential_impact": "Poprawa stabilności finansowej",
                "priority": "high"
            })
    
    return gaps


def generate_strategic_recommendations(analysis_data: Dict) -> List[Dict]:
    """Generuje strategiczne rekomendacje na podstawie analizy"""
    recommendations = []
    
    # Rekomendacje bazujące na trendach
    trends = analysis_data.get('trends', {})
    if trends.get('revenue_trend_direction') == 'spadkowy':
        recommendations.append({
            "category": "Odwrócenie trendu spadkowego",
            "title": "Program ratunkowy przychodów",
            "description": "Natychmiastowe działania dla zatrzymania spadku",
            "actions": [
                "Analiza competitive intelligence - co robią konkurenci?",
                "Ankieta satysfakcji klientów (NPS)",
                "Review menu i cen vs konkurencja",
                "Kampania reaktywacyjna dla stałych klientów",
                "Tymczasowe promocje dla zwiększenia ruchu"
            ],
            "timeline": "1-2 miesiące",
            "expected_impact": "Zatrzymanie spadku, stabilizacja na obecnym poziomie",
            "priority": "critical"
        })
    
    # Rekomendacje sezonowość
    seasonality = analysis_data.get('seasonality', {})
    if seasonality.get('seasonality_detected'):
        worst_months = [month for month, _ in seasonality.get('worst_months', [])]
        recommendations.append({
            "category": "Strategia sezonowa",
            "title": "Program na słabe miesiące",
            "description": f"Specjalne działania na {', '.join(worst_months[:2])}",
            "actions": [
                "Eventy tematyczne w słabe miesiące",
                "Menu sezonowe z lokalnych składników",
                "Partnerstwa z hotelami na catering",
                "Promocje dla grup biznesowych",
                "Wigilie firmowe / imprezy prywatne"
            ],
            "timeline": "Przed sezonem słabym",
            "expected_impact": "Wzrost o 15-25% w słabe miesiące",
            "priority": "high"
        })
    
    # Rekomendacje wzrostu średniej wartości
    recommendations.append({
        "category": "Wzrost AOV",
        "title": "Zwiększenie średniej wartości rachunku",
        "description": "Strategia upselling i cross-selling",
        "actions": [
            "Szkolenie kelnerów w sprzedaży dodatków",
            "Menu degustacyjne z winami",
            "Desery premium i kawa specialty",
            "Pakiety biznesowe (lunch + sala konferencyjna)",
            "Program lojalnościowy z progami wydatków"
        ],
        "timeline": "2-3 miesiące implementacji",
        "expected_impact": "Wzrost AOV o 20-30 PLN",
        "priority": "high"
    })
    
    # Rekomendacje operacyjne
    recommendations.append({
        "category": "Optymalizacja operacyjna", 
        "title": "Poprawa efektywności kosztowej",
        "description": "Zarządzanie kosztami bez utraty jakości",
        "actions": [
            "Analiza kosztów składników vs marże na daniach",
            "Renegocjacja umów z dostawcami",
            "Optymalizacja grafików pracy (demand planning)",
            "Redukcja food waste przez lepsze prognozowanie",
            "Energy management - LED, smart termostaty"
        ],
        "timeline": "3-6 miesięcy",
        "expected_impact": "Redukcja kosztów o 5-8%",
        "priority": "medium"
    })
    
    # Rekomendacje marketingowe
    recommendations.append({
        "category": "Marketing i pozycjonowanie",
        "title": "Wzmocnienie marki Forum Panorama",
        "description": "Kapitalizacja na unikatowej lokalizacji",
        "actions": [
            "Content marketing - widoki Krakowa na social media",
            "Partnerstwo z influencerami lifestyle/travel",
            "Oferta fotograficzna (sesje na dachu)",
            "Eventy biznesowe i networking",
            "Współpraca z przewodnikami turystycznymi"
        ],
        "timeline": "Stały proces, 6-12 miesięcy",
        "expected_impact": "Wzrost rozpoznawalności i liczby klientów",
        "priority": "medium"
    })
    
    return recommendations


def create_action_plan(recommendations: List[Dict], forecast_data: Dict) -> Dict:
    """Tworzy szczegółowy plan działań"""
    
    # Sortuj rekomendacje według priorytetu
    priority_order = {"critical": 1, "high": 2, "medium": 3, "low": 4}
    sorted_recommendations = sorted(recommendations, key=lambda x: priority_order.get(x.get('priority', 'low'), 4))
    
    # Plan 90-dniowy
    quarter_plan = {
        "Miesiąc 1 (Natychmiastowe)": [],
        "Miesiąc 2-3 (Krótkoterminowe)": [],
        "Kwartał 2-4 (Długoterminowe)": []
    }
    
    for rec in sorted_recommendations:
        timeline = rec.get('timeline', '')
        if 'natychmiast' in timeline.lower() or rec.get('priority') == 'critical':
            quarter_plan["Miesiąc 1 (Natychmiastowe)"].append(rec)
        elif '1-2 mies' in timeline or '2-3 mies' in timeline:
            quarter_plan["Miesiąc 2-3 (Krótkoterminowe)"].append(rec)
        else:
            quarter_plan["Kwartał 2-4 (Długoterminowe)"].append(rec)
    
    # Oszacowanie budżetu
    budget_estimation = {
        "Marketing i promocja": "15,000 - 25,000 PLN/miesiąc",
        "Szkolenia personelu": "5,000 - 8,000 PLN jednorazowo",
        "Modernizacja operacyjna": "20,000 - 40,000 PLN jednorazowo",
        "Eventy i partnerstwa": "10,000 - 15,000 PLN/miesiąc"
    }
    
    # Metryki do śledzenia
    kpis = [
        "Miesięczne przychody brutto",
        "Średnia wartość rachunku (AOV)",
        "Liczba klientów miesięcznie", 
        "Marża zysku brutto",
        "Net Promoter Score (NPS)",
        "Occupancy rate (wypełnienie miejsc)",
        "Cost per acquisition (CPA)"
    ]
    
    return {
        "quarterly_plan": quarter_plan,
        "budget_estimation": budget_estimation,
        "success_metrics": kpis,
        "total_recommendations": len(recommendations),
        "critical_actions": len([r for r in recommendations if r.get('priority') == 'critical'])
    }


def generate_executive_summary(analysis_data: Dict, recommendations: List[Dict]) -> Dict:
    """Generuje podsumowanie wykonawcze"""
    
    trends = analysis_data.get('trends', {})
    forecast = analysis_data.get('forecast', {})
    risks = analysis_data.get('risks', [])
    
    # Kluczowe wskaźniki
    current_situation = "stabilna"
    if trends.get('revenue_trend_direction') == 'spadkowy':
        current_situation = "wymagająca interwencji"
    elif trends.get('monthly_change_rate', 0) > 5:
        current_situation = "rosnąca"
    
    # Prognoza finansowa
    forecasted_revenue = forecast.get('total_predicted_revenue', 0)
    forecast_period = forecast.get('forecast_period', 'N/A')
    
    # Priorytety strategiczne
    critical_recs = [r for r in recommendations if r.get('priority') == 'critical']
    high_recs = [r for r in recommendations if r.get('priority') == 'high']
    
    return {
        "situation_assessment": current_situation,
        "trend_direction": trends.get('revenue_trend_direction', 'unknown'),
        "trend_strength": trends.get('trend_strength', 'unknown'),
        "forecasted_revenue_6m": forecasted_revenue,
        "forecast_period": forecast_period,
        "high_risk_factors": len([r for r in risks if r.get('severity') == 'high']),
        "critical_recommendations": len(critical_recs),
        "high_priority_recommendations": len(high_recs),
        "key_focus_areas": [
            "Stabilizacja przychodów" if current_situation == "wymagająca interwencji" else "Wzrost i ekspansja",
            "Optymalizacja średniej wartości rachunku",
            "Zarządzanie sezonowością",
            "Wzmocnienie pozycji konkurencyjnej"
        ]
    }