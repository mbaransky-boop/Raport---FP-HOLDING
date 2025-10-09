#!/usr/bin/env python3
"""
Główny skrypt generujący raport FP HOLDING
"""
import sys
from pathlib import Path

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from fp_holding_analyzer import FPHoldingAnalyzer
from report_generator import ReportGenerator

def main():
    print("=" * 80)
    print("🚀 GENEROWANIE RAPORTU FP HOLDING")
    print("=" * 80)
    
    # Ścieżka do pliku Excel
    excel_file = "/Users/michalbaranski/Desktop/Tabela kosztowa doraportu.xlsx"
    
    if not Path(excel_file).exists():
        print(f"❌ Nie znaleziono: {excel_file}")
        return 1
    
    # Analiza
    print("\n📊 Analizuję dane...")
    analyzer = FPHoldingAnalyzer(excel_file)
    
    analyzer.load_and_clean().validate().analyze().find_savings().create_recovery_plan()
    
    # Raport
    print("\n📝 Tworzę raport HTML...")
    report_gen = ReportGenerator(analyzer)
    report_path = report_gen.generate_html()
    
    print("\n" + "=" * 80)
    print("✅ SUKCES!")
    print(f"📊 Raport: {report_path}")
    print("\n💡 Uruchom serwer:")
    print("   python3 -m http.server 8000")
    print("\n   Potem otwórz:")
    print("   http://localhost:8000/reports/fp_holding_raport.html")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
