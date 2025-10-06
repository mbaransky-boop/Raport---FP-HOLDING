# Sales Reports Generator

Projekt do generowania raportów i analizy danych sprzedażowych.

Cel:
- Wczytywanie danych sprzedażowych (CSV)
- Analiza i agregacja (przychód, liczba zamówień, średnia wartość)
- Generowanie raportów HTML (z wykresami)

Szybki start

1. Stwórz virtualenv i zainstaluj wymagania:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Uruchom CLI przykład:

```bash
python -m sales_reports.src.cli --input data/sample_sales.csv --output reports/report.html
```

Struktura:
- `src/` - kod źródłowy
- `data/` - przykładowe dane
- `reports/` - wygenerowane raporty i szablony
- `tests/` - testy jednostkowe

# Raport---FP-HOLDING
