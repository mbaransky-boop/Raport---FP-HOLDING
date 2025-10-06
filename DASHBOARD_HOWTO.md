# 🚀 Automatyczny Generator Dashboardu

## Jak używać nowego systemu

### 1. Pojedynczy plik Excel → Dashboard z wykresami

```bash
cd "/Users/michalbaranski/PANORAMA VS STUDIO CODE"
source sales_reports/.venv/bin/activate
export PYTHONPATH="$(pwd)"

python sales_reports/excel_to_dashboard.py "TWOJ_PLIK.xlsx" "dashboard.html"
```

### 2. Przykłady użycia

```bash
# Podstawowe użycie
python sales_reports/excel_to_dashboard.py "ROZLICZENIE.xlsx"

# Z własną nazwą wyjścia
python sales_reports/excel_to_dashboard.py "ROZLICZENIE.xlsx" "moj_raport.html"

# Z pełnymi ścieżkami
python sales_reports/excel_to_dashboard.py "/path/to/file.xlsx" "/path/to/output.html"
```

## 🎯 Co otrzymujesz

### Dashboard zawiera:
- **📊 KPI Cards:** Przychód, średnia wartość, marża, zysk
- **📈 Wykresy interaktywne:**
  - Trend miesięcznych przychodów
  - Analiza rentowności (przychody vs koszty + marża)
  - Średnia wartość rachunku w czasie
  - Liczba rachunków miesięcznie
- **🔍 Kluczowe spostrzeżenia:** Najlepszy/najsłabszy miesiąc, trendy
- **💼 Szczegóły rentowności:** Z oryginalnych danych Excel

### Funkcje automatyczne:
- ✅ Konwersja Excel → CSV
- ✅ Analiza rentowności z kosztami/VAT
- ✅ Generowanie wykresów (matplotlib)
- ✅ Responsive HTML dashboard
- ✅ Osadzone wykresy (base64)
- ✅ Automatyczne czyszczenie plików tymczasowych

## 📋 Wymagania pliku Excel

Plik musi zawierać kolumny:
- `Unnamed: 0` - nazwy miesięcy
- `OBRÓT BRUTTO` - przychody brutto
- `OBRÓT NETTO` - przychody netto
- `KOSZTY BRUTTO` - koszty brutto
- `KOSZTY NETTO` - koszty netto
- `ILOŚĆ RACHUNKÓW` - liczba transakcji
- `TOTAL BRUTTO ZYSK/STRATA` - zysk/strata brutto
- `TOTAL NETTO ZYSK/STRATA` - zysk/strata netto

## 🎨 Dostępne szablony

1. **dashboard.html.j2** - Kompletny dashboard z wykresami
2. **report.html.j2** - Prosty raport (oryginalny)

## ⚡ Szybkie polecenia

```bash
# Ustaw raz na sesję
cd "/Users/michalbaranski/PANORAMA VS STUDIO CODE"
source sales_reports/.venv/bin/activate
export PYTHONPATH="$(pwd)"

# Potem używaj szybko
python sales_reports/excel_to_dashboard.py "FILE.xlsx"
```

## 🔧 Rozszerzenia

System można łatwo rozszerzyć o:
- Więcej typów wykresów
- Export do PDF
- Automatyczne wysyłanie email
- Integracja z bazami danych
- Monitoring w czasie rzeczywistym

---
*Instrukcja utworzona automatycznie - 6 października 2025*