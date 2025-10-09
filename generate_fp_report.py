"""
Główny skrypt do generowania raportu finansowego FP HOLDING
"""
from src.fp_holding_analyzer import FPHoldingAnalyzer, FPHoldingReportGenerator
from pathlib import Path


def main():
    print("=" * 80)
    print("🚀 GENEROWANIE RAPORTU DLA FP HOLDING")
    print("=" * 80)
    
    # Ścieżka do pliku Excel
    excel_file = Path("/Users/michalbaranski/Desktop/Tabela kosztowa doraportu.xlsx")
    
    if not excel_file.exists():
        print(f"❌ Nie znaleziono pliku: {excel_file}")
        print("💡 Upewnij się że plik znajduje się na Pulpicie")
        return False
    
    # 1. Wczytaj i analizuj dane
    print("\n📊 KROK 1: Wczytywanie danych...")
    analyzer = FPHoldingAnalyzer(excel_file)
    
    if not analyzer.load_data():
        print("❌ Błąd podczas wczytywania danych")
        return False
    
    # 2. Analiza przychodów
    print("\n📈 KROK 2: Analiza przychodów...")
    revenue = analyzer.analyze_revenue_trends()
    print(f"   Całkowity obrót: {revenue['total']:,.0f} zł")
    print(f"   Trend: {revenue['trend_direction']}")
    
    # 3. Analiza kosztów
    print("\n💰 KROK 3: Analiza kosztów...")
    costs = analyzer.analyze_costs()
    print(f"   Całkowite koszty: {costs['total_costs_brutto']:,.0f} zł")
    print(f"   ZUS razem: {costs['total_zus']:,.0f} zł")
    
    # 4. Rentowność
    print("\n📊 KROK 4: Analiza rentowności...")
    profit = analyzer.calculate_profitability()
    print(f"   Zysk/Strata: {profit['total_profit']:,.0f} zł")
    print(f"   Marża: {profit['profit_margin']:.1f}%")
    print(f"   Rentowne miesiące: {profit['profitable_months']}/14")
    
    # 5. Oszczędności
    print("\n💡 KROK 5: Identyfikacja oszczędności...")
    savings = analyzer.find_savings_opportunities()
    print(f"   Znaleziono {len(savings)} możliwości oszczędności")
    
    # 6. Próg rentowności
    print("\n🎯 KROK 6: Obliczanie progu rentowności...")
    breakeven = analyzer.calculate_breakeven()
    print(f"   Próg rentowności (mies.): {breakeven['breakeven_monthly']:,.0f} zł")
    print(f"   Status: {breakeven['status']}")
    
    # 7. Plan naprawczy
    print("\n🚀 KROK 7: Tworzenie planu naprawczego...")
    recovery = analyzer.create_recovery_plan()
    print(f"   Działania natychmiastowe: {len(recovery['immediate'])}")
    print(f"   Działania krótkoterminowe: {len(recovery['short_term'])}")
    
    # 8. Generuj raport HTML
    print("\n📄 KROK 8: Generowanie raportu HTML...")
    report_gen = FPHoldingReportGenerator(analyzer)
    report_path = report_gen.generate_html_report()
    
    print("\n" + "=" * 80)
    print("✅ RAPORT WYGENEROWANY POMYŚLNIE!")
    print(f"📊 Lokalizacja: {report_path}")
    print("\n💡 Uruchom serwer lokalny aby zobaczyć raport:")
    print("   python3 run_server.py")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    main()
