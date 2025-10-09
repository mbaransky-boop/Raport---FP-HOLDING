"""
FP HOLDING Financial Analyzer
Analizator danych finansowych z Excela zgodnie z rzeczywistą strukturą i kolorami.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List


class FPHoldingAnalyzer:
    """Analizator finansowy dla FP HOLDING wykorzystujący rzeczywistą strukturę Excela"""
    
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self.analysis = {}
        
    def load_and_clean(self):
        """
        Ładuje i czyści dane z Excela ZACHOWUJĄC gotową kolumnę ZYSK.
        
        Struktura Excela (kolory mają znaczenie!):
        - ZIELONE (przychód): B, C, D (Obrót brutto, Obrót netto, VAT)
        - POMARAŃCZOWE (koszty): E, F, G, H, I, J (Koszta brutto, Kwota netto, VAT, ZUS, PIT, Koszt pracowniczy)
        - ŻÓŁTE (zysk): K (ZYSK/Stra BRUTTO) - gotowa formuła =C-F-H-I-J
        """
        print(f"📊 Ładuję dane z: {self.excel_path}")
        
        # Wczytaj dane od września 2024 (pomijamy sierpień 2024)
        df = pd.read_excel(self.excel_path, nrows=14)
        
        # Usuń pierwszy wiersz (sierpień 2024) - skupiamy się na wrz.2024 - wrz.2025
        df = df.iloc[1:].reset_index(drop=True)
        
        print(f"✅ Wczytano {len(df)} miesięcy danych (wrz.2024 - wrz.2025)")
        print(f"📋 Kolumny: {list(df.columns)}")
        
        # KLUCZOWE: Użyj gotowej kolumny ZYSK zamiast obliczać od nowa!
        self.df = df.copy()
        
        # Zmień nazwy kolumn dla wygody (zachowując semantykę)
        self.df.columns = [
            'Okres',  # A - data
            'Obrót_brutto',  # B - ZIELONY (przychód)
            'Obrót_netto',   # C - ZIELONY (przychód)
            'VAT_przychód',  # D - ZIELONY (przychód)
            'Koszta_brutto', # E - POMARAŃCZOWY (koszt)
            'Kwota_netto',   # F - POMARAŃCZOWY (koszt)
            'VAT_koszt',     # G - POMARAŃCZOWY (koszt, formuła =E-F)
            'ZUS',           # H - POMARAŃCZOWY (koszt)
            'PIT',           # I - POMARAŃCZOWY (koszt)
            'Koszt_pracowniczy', # J - POMARAŃCZOWY (koszt)
            'Zysk_Excel',    # K - ŻÓŁTY (zysk, formuła =C-F-H-I-J)
            'Średni_rachunek', # L
            'Ilość_rachunków'  # M
        ]
        
        # Konwersja dat - formatuj ładnie z polskimi nazwami miesięcy
        import locale
        try:
            locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')
        except:
            pass  # Jeśli nie ma polskiej lokalizacji, użyj angielskiej
        
        self.df['Okres_str'] = pd.to_datetime(self.df['Okres']).dt.strftime('%b %Y')
        
        # Sumuj RZECZYWISTE koszty zgodnie z formułą Excela
        self.df['Koszty_total'] = (
            self.df['Kwota_netto'] + 
            self.df['ZUS'] + 
            self.df['PIT'] + 
            self.df['Koszt_pracowniczy']
        )
        
        # Weryfikacja: czy nasz liczony zysk = zysk z Excela?
        self.df['Zysk_obliczony'] = (
            self.df['Obrót_netto'] - 
            self.df['Koszty_total']
        )
        
        # Pokaż różnicę (powinna być bliska 0)
        self.df['Różnica_zysk'] = abs(self.df['Zysk_Excel'] - self.df['Zysk_obliczony'])
        max_diff = self.df['Różnica_zysk'].max()
        
        if max_diff > 1:
            print(f"⚠️  UWAGA: Maksymalna różnica w zysku: {max_diff:.2f} zł")
        else:
            print(f"✅ Weryfikacja zysku OK (max różnica: {max_diff:.2f} zł)")
        
        print(f"\n📊 Podsumowanie danych:")
        print(f"  • Okres: {self.df['Okres_str'].iloc[0]} - {self.df['Okres_str'].iloc[-1]}")
        print(f"  • Przychód netto: {self.df['Obrót_netto'].sum():,.2f} zł")
        print(f"  • Koszty total: {self.df['Koszty_total'].sum():,.2f} zł")
        print(f"  • Zysk (Excel): {self.df['Zysk_Excel'].sum():,.2f} zł")
        
        return self
        
    def validate(self):
        """Walidacja danych"""
        print("\n🔍 Walidacja danych...")
        
        issues = []
        
        # Sprawdź braki
        null_counts = self.df.isnull().sum()
        if null_counts.any():
            issues.append(f"Brakujące wartości: {null_counts[null_counts > 0].to_dict()}")
        
        # Sprawdź ujemne przychody
        if (self.df['Obrót_netto'] < 0).any():
            neg_revenue = self.df[self.df['Obrót_netto'] < 0]
            issues.append(f"Ujemne przychody w miesiącach: {neg_revenue['Okres_str'].tolist()}")
        
        # Sprawdź ekstremalnie wysokie koszty
        avg_costs = self.df['Koszty_total'].mean()
        high_costs = self.df[self.df['Koszty_total'] > avg_costs * 2]
        if not high_costs.empty:
            print(f"⚠️  Miesiące z kosztami >200% średniej:")
            for _, row in high_costs.iterrows():
                print(f"    {row['Okres_str']}: {row['Koszty_total']:,.0f} zł")
        
        if issues:
            print(f"⚠️  Znalezione problemy: {len(issues)}")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("✅ Dane poprawne")
        
        return self
        
    def analyze(self):
        """Główna analiza finansowa"""
        print("\n📈 Analiza finansowa...")
        
        # Podstawowe metryki
        total_revenue = self.df['Obrót_netto'].sum()
        total_costs = self.df['Koszty_total'].sum()
        total_profit = self.df['Zysk_Excel'].sum()  # Używamy GOTOWEGO zysku!
        
        # Miesięczne średnie
        avg_revenue = self.df['Obrót_netto'].mean()
        avg_costs = self.df['Koszty_total'].mean()
        avg_profit = self.df['Zysk_Excel'].mean()
        
        # Marża
        margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Miesiące z zyskiem vs stratą
        profitable_months = (self.df['Zysk_Excel'] > 0).sum()
        loss_months = (self.df['Zysk_Excel'] < 0).sum()
        
        # Najlepszy i najgorszy miesiąc
        best_month = self.df.loc[self.df['Zysk_Excel'].idxmax()]
        worst_month = self.df.loc[self.df['Zysk_Excel'].idxmin()]
        
        # Trendy (ostatnie 3 vs pierwsze 3 miesiące)
        recent_avg = self.df.tail(3)['Zysk_Excel'].mean()
        initial_avg = self.df.head(3)['Zysk_Excel'].mean()
        trend = "rosnący" if recent_avg > initial_avg else "spadający"
        
        self.analysis = {
            'summary': {
                'total_revenue': total_revenue,
                'total_costs': total_costs,
                'total_profit': total_profit,
                'avg_revenue': avg_revenue,
                'avg_costs': avg_costs,
                'avg_profit': avg_profit,
                'margin': margin,
                'profitable_months': profitable_months,
                'loss_months': loss_months,
                'trend': trend
            },
            'best_month': {
                'period': best_month['Okres_str'],
                'profit': best_month['Zysk_Excel'],
                'revenue': best_month['Obrót_netto'],
                'costs': best_month['Koszty_total']
            },
            'worst_month': {
                'period': worst_month['Okres_str'],
                'profit': worst_month['Zysk_Excel'],
                'revenue': worst_month['Obrót_netto'],
                'costs': worst_month['Koszty_total']
            },
            'costs_breakdown': {
                'kwota_netto': self.df['Kwota_netto'].sum(),
                'zus': self.df['ZUS'].sum(),
                'pit': self.df['PIT'].sum(),
                'koszt_pracowniczy': self.df['Koszt_pracowniczy'].sum()
            }
        }
        
        # Breakeven
        if avg_revenue > 0:
            breakeven_revenue = avg_costs
            current_revenue = avg_revenue
            breakeven_gap = current_revenue - breakeven_revenue
            
            self.analysis['breakeven'] = {
                'monthly_breakeven': breakeven_revenue,
                'current_revenue': current_revenue,
                'gap': breakeven_gap,
                'current_margin': margin,
                'status': 'above' if breakeven_gap > 0 else 'below'
            }
        
        print(f"✅ Analiza ukończona")
        print(f"  • Całkowity przychód: {total_revenue:,.0f} zł")
        print(f"  • Całkowite koszty: {total_costs:,.0f} zł")
        print(f"  • Całkowity zysk: {total_profit:,.0f} zł")
        print(f"  • Marża: {margin:.2f}%")
        print(f"  • Miesiące z zyskiem: {profitable_months}/{len(self.df)}")
        
        return self
        
    def find_savings(self):
        """Identyfikacja możliwości oszczędności"""
        print("\n💡 Szukam możliwości oszczędności...")
        
        savings_opportunities = []
        
        # 1. ZUS - sprawdź wysokie płatności
        avg_zus = self.df['ZUS'].mean()
        high_zus = self.df[self.df['ZUS'] > avg_zus * 1.3]
        if not high_zus.empty:
            potential_zus_savings = (high_zus['ZUS'].mean() - avg_zus) * len(high_zus)
            savings_opportunities.append({
                'category': 'ZUS',
                'description': 'Wysokie płatności ZUS w niektórych miesiącach',
                'potential_savings': potential_zus_savings,
                'action': 'Sprawdź możliwość preferencyjnego ZUS lub optymalizacji podstawy'
            })
        
        # 2. Koszty pracownicze - sprawdź fluktuacje
        avg_employee = self.df['Koszt_pracowniczy'].mean()
        high_employee = self.df[self.df['Koszt_pracowniczy'] > avg_employee * 1.5]
        if not high_employee.empty:
            potential_employee_savings = (high_employee['Koszt_pracowniczy'].mean() - avg_employee) * 0.2
            savings_opportunities.append({
                'category': 'Koszty pracownicze',
                'description': 'Wysokie wahania kosztów pracowniczych',
                'potential_savings': potential_employee_savings * 12,
                'action': 'Optymalizacja zatrudnienia - rozważ outsourcing lub część etatu'
            })
        
        # 3. Kwota netto (główny koszt) - miesiące z ekstremalnie wysokimi kosztami
        avg_kwota_netto = self.df['Kwota_netto'].mean()
        high_kwota = self.df[self.df['Kwota_netto'] > avg_kwota_netto * 1.5]
        if not high_kwota.empty:
            potential_kwota_savings = (high_kwota['Kwota_netto'].mean() - avg_kwota_netto) * 0.15
            savings_opportunities.append({
                'category': 'Kwota netto (główne koszty)',
                'description': f'{len(high_kwota)} miesiące z kosztami >150% średniej',
                'potential_savings': potential_kwota_savings * 12,
                'action': 'Renegocjacja umów z dostawcami, bulk pricing'
            })
        
        # 4. Średni rachunek - optymalizacja
        if 'Średni_rachunek' in self.df.columns:
            avg_receipt = self.df['Średni_rachunek'].mean()
            if avg_receipt > 0:
                upsell_potential = avg_receipt * 0.1 * self.df['Ilość_rachunków'].sum()
                savings_opportunities.append({
                    'category': 'Optymalizacja przychodów',
                    'description': 'Zwiększenie średniego rachunku o 10%',
                    'potential_savings': upsell_potential,
                    'action': 'Upselling, cross-selling, pakiety'
                })
        
        self.analysis['savings'] = savings_opportunities
        
        total_potential = sum(s['potential_savings'] for s in savings_opportunities)
        print(f"✅ Znaleziono {len(savings_opportunities)} możliwości oszczędności")
        print(f"  • Potencjalne oszczędności roczne: {total_potential:,.0f} zł")
        
        return self
        
    def create_recovery_plan(self):
        """Tworzy plan naprawczy"""
        print("\n🎯 Tworzę plan naprawczy...")
        
        # Pobierz kluczowe dane
        avg_profit = self.analysis['summary']['avg_profit']
        margin = self.analysis['summary']['margin']
        loss_months = self.analysis['summary']['loss_months']
        
        recovery_plan = {
            'immediate': [],  # 0-30 dni
            'short_term': [],  # 1-3 miesiące
            'medium_term': [],  # 3-6 miesięcy
            'long_term': []  # 6-12 miesięcy
        }
        
        # IMMEDIATE (0-30 dni)
        if loss_months > 0:
            recovery_plan['immediate'].append({
                'action': 'Analiza miesięcy stratnych',
                'description': f'{loss_months} miesięcy ze stratą - zidentyfikuj przyczyny',
                'impact': 'Wysokie',
                'effort': 'Niskie'
            })
        
        recovery_plan['immediate'].append({
            'action': 'Cash flow emergency check',
            'description': 'Sprawdź zobowiązania US VAT (-50k), ZUS rata (-90k)',
            'impact': 'Krytyczne',
            'effort': 'Niskie'
        })
        
        # SHORT TERM (1-3 miesiące)
        if margin < 20:
            recovery_plan['short_term'].append({
                'action': 'Redukcja kosztów o 10%',
                'description': 'Renegocjacja umów, eliminacja marnotrawstwa',
                'impact': 'Wysokie',
                'effort': 'Średnie'
            })
        
        recovery_plan['short_term'].append({
            'action': 'Zwiększenie średniego rachunku',
            'description': 'Upselling, cross-selling - cel +10% do średniego rachunku',
            'impact': 'Średnie',
            'effort': 'Niskie'
        })
        
        # MEDIUM TERM (3-6 miesięcy)
        recovery_plan['medium_term'].append({
            'action': 'Optymalizacja zatrudnienia',
            'description': 'Analiza kosztów pracowniczych - outsourcing, automatyzacja',
            'impact': 'Wysokie',
            'effort': 'Wysokie'
        })
        
        recovery_plan['medium_term'].append({
            'action': 'Restrukturyzacja ZUS',
            'description': 'Układ ratalny ZUS (-517k) - rozłóż na 24 miesiące',
            'impact': 'Średnie',
            'effort': 'Średnie'
        })
        
        # LONG TERM (6-12 miesięcy)
        recovery_plan['long_term'].append({
            'action': 'Dywersyfikacja przychodów',
            'description': 'Nowe źródła przychodów, produkty premium',
            'impact': 'Wysokie',
            'effort': 'Wysokie'
        })
        
        recovery_plan['long_term'].append({
            'action': 'Optymalizacja podatkowa',
            'description': 'Przegląd struktury podatkowej z doradcą',
            'impact': 'Średnie',
            'effort': 'Średnie'
        })
        
        self.analysis['recovery_plan'] = recovery_plan
        
        total_actions = sum(len(v) for v in recovery_plan.values())
        print(f"✅ Plan naprawczy gotowy: {total_actions} działań")
        
        return self
        
    def export_to_csv(self, output_path: str):
        """Eksportuje oczyszczone dane do CSV"""
        export_df = self.df[[
            'Okres_str', 
            'Obrót_brutto', 
            'Obrót_netto', 
            'VAT_przychód',
            'Koszta_brutto',
            'Kwota_netto',
            'ZUS',
            'PIT',
            'Średni_rachunek',
            'Ilość_rachunków',
            'Zysk_Excel'  # Eksportuj GOTOWY zysk z Excela!
        ]].copy()
        
        export_df.columns = [
            'Okres', 
            'Obrót brutto', 
            'Obrót netto', 
            'VAT',
            'Koszta brutto',
            'Kwota netto',
            'ZUS',
            'PIT',
            'Średni rachunek',
            'Ilość rachunków',
            'Zysk'
        ]
        
        export_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✅ Dane wyeksportowane do: {output_path}")
        
        return self
