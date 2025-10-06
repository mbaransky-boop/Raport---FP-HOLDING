#!/usr/bin/env python3
"""Automatyczny generator raportu strategicznego z pliku Excel"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Dodaj ścieżkę do modułów src
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from dashboard import generate_dashboard
from strategic_dashboard import generate_strategic_report


def excel_to_csv(excel_path: str) -> str:
    """Konwertuj Excel na CSV z obsługą różnych formatów dat"""
    
    # Wczytaj plik Excel z różnymi wariantami nazw arkuszy
    try:
        # Próbuj wczytać pierwszy arkusz
        df = pd.read_excel(excel_path, sheet_name=0)
    except Exception as e:
        print(f"Błąd podczas wczytywania Excel: {e}")
        return None
    
    print(f"Wczytano {len(df)} wierszy z pliku Excel")
    print(f"Kolumny: {list(df.columns)}")
    
    # Sprawdź czy mamy wymagane kolumny
    required_columns = ['Data', 'Kwota', 'Status']
    missing_columns = []
    
    for col in required_columns:
        if col not in df.columns:
            # Sprawdź podobne nazwy kolumn
            similar_cols = [c for c in df.columns if col.lower() in c.lower()]
            if similar_cols:
                print(f"Kolumna '{col}' nie znaleziona, ale znaleziono podobne: {similar_cols}")
                # Użyj pierwszej podobnej kolumny
                df = df.rename(columns={similar_cols[0]: col})
            else:
                missing_columns.append(col)
    
    if missing_columns:
        print(f"BŁĄD: Brakuje kolumn: {missing_columns}")
        print(f"Dostępne kolumny: {list(df.columns)}")
        return None
    
    # Konwertuj kolumnę Date na właściwy format
    try:
        # Sprawdź różne formaty dat
        if df['Data'].dtype == 'object':
            # Spróbuj różnych formatów
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=True)
        else:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        
        # Usuń wiersze z nieprawidłowymi datami
        before_cleaning = len(df)
        df = df.dropna(subset=['Data'])
        after_cleaning = len(df)
        
        if after_cleaning < before_cleaning:
            print(f"Usunięto {before_cleaning - after_cleaning} wierszy z nieprawidłowymi datami")
            
    except Exception as e:
        print(f"Błąd podczas konwersji dat: {e}")
        return None
    
    # Konwertuj kwoty na numeryczne
    try:
        if df['Kwota'].dtype == 'object':
            # Usuń przecinki i inne znaki
            df['Kwota'] = df['Kwota'].astype(str).str.replace(',', '.').str.replace(' ', '')
            df['Kwota'] = pd.to_numeric(df['Kwota'], errors='coerce')
        
        # Usuń wiersze z nieprawidłowymi kwotami
        before_cleaning = len(df)
        df = df.dropna(subset=['Kwota'])
        after_cleaning = len(df)
        
        if after_cleaning < before_cleaning:
            print(f"Usunięto {before_cleaning - after_cleaning} wierszy z nieprawidłowymi kwotami")
            
    except Exception as e:
        print(f"Błąd podczas konwersji kwot: {e}")
        return None
    
    # Stwórz ścieżkę do pliku CSV
    csv_path = str(Path(excel_path).with_suffix('.csv'))
    
    # Zapisz do CSV
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Zapisano {len(df)} wierszy do {csv_path}")
        return csv_path
    except Exception as e:
        print(f"Błąd podczas zapisywania CSV: {e}")
        return None


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Użycie: python excel_to_dashboard.py ścieżka_do_pliku.xlsx [--strategic]")
        print("  --strategic : generuje zaawansowany raport strategiczny z prognozami")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    strategic_mode = len(sys.argv) == 3 and sys.argv[2] == '--strategic'
    
    excel_path = Path(excel_file)
    
    if not excel_path.exists():
        print(f"Plik {excel_file} nie istnieje!")
        sys.exit(1)
    
    print(f"Przetwarzanie pliku: {excel_file}")
    if strategic_mode:
        print("🔮 Tryb strategiczny: generowanie prognozy i rekomendacji")
    
    # Konwertuj Excel na CSV
    csv_path = excel_to_csv(str(excel_path))
    if not csv_path:
        print("Nie udało się przekonwertować pliku Excel")
        sys.exit(1)
    
    # Wybierz typ raportu
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if strategic_mode:
        # Wygeneruj raport strategiczny
        output_path = f"reports/strategic_report_{timestamp}.html"
        try:
            result_path = generate_strategic_report(csv_path, str(excel_path), output_path)
            print(f"\n✅ Raport strategiczny wygenerowany pomyślnie!")
            print(f"🔮 Zawiera prognozy, analizę ryzyka i rekomendacje")
            print(f"📊 Ścieżka do raportu: {result_path}")
            print(f"🌐 Otwórz plik w przeglądarce aby zobaczyć pełną analizę")
            
        except Exception as e:
            print(f"❌ Błąd podczas generowania raportu strategicznego: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        # Wygeneruj standardowy raport
        output_path = f"reports/dashboard_{timestamp}.html"
        try:
            result_path = generate_dashboard(csv_path, str(excel_path), output_path)
            print(f"\n✅ Raport standardowy wygenerowany pomyślnie!")
            print(f"📊 Ścieżka do raportu: {result_path}")
            print(f"🌐 Otwórz plik w przeglądarce aby zobaczyć wyniki")
            print(f"\n💡 Wskazówka: Użyj --strategic dla zaawansowanej analizy z prognozami")
            
        except Exception as e:
            print(f"❌ Błąd podczas generowania raportu: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()