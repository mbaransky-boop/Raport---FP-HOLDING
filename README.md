# 📊 FP HOLDING - Financial Analytics Dashboard

Nowoczesny, interaktywny raport finansowy z dark mode UI i symulatorem inwestycyjnym.

## ✨ Główne funkcje

### 📈 Interaktywny Dashboard
- **Dark Mode UI** z neonowymi akcentami i animacjami
- **8 KPI Cards** z real-time updates
- **4 interaktywne wykresy Plotly** (korelacja, trendy, rentowność, ZUS)
- **Professional styling** gotowy do prezentacji inwestorskiej

### 🚀 Investment Simulator
- **5 interaktywnych suwaków** do optymalizacji parametrów:
  - 📈 Wzrost przychodów (-20% do +50%)
  - 💰 Redukcja kosztów (0% do 30%)
  - 📊 Wzrost średniego rachunku (0% do 40%)
  - 👥 Optymalizacja zatrudnienia (0% do 25%)
  - 🏛️ Redukcja ZUS (0% do 20%)

- **4 gotowe scenariusze**:
  - 📊 Konserwatywny
  - 📈 Umiarkowany
  - 🚀 Agresywny
  - ⚖️ Break-even (auto-kalkulacja)

- **Real-time forecast**: Projekcja 12-miesięczna z dynamicznym wykresem

## 🚀 Szybki start

### 1. Instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/mbaransky-boop/Raport---FP-HOLDING.git
cd Raport---FP-HOLDING

# Zainstaluj zależności
pip install -r requirements.txt
```

### 2. Generowanie raportu

```bash
# Wygeneruj raport HTML
python3 generate_report.py
```

### 3. Podgląd w przeglądarce

```bash
# Uruchom lokalny serwer
python3 -m http.server 8000

# Otwórz w przeglądarce:
# http://localhost:8000/reports/fp_holding_raport.html
```

## 📁 Struktura projektu

```
Raport---FP-HOLDING/
├── src/
│   ├── fp_holding_analyzer.py    # Analiza danych Excel
│   └── report_generator.py       # Generator HTML z symulatorem
├── data/
│   └── cleaned_cost_table.csv    # Dane finansowe
├── reports/
│   └── fp_holding_raport.html    # Wygenerowany raport
├── generate_report.py            # Main script
├── requirements.txt              # Zależności Python
└── README.md                     # Ta dokumentacja
```

## 🎨 Technologie

- **Python 3.9+**
- **Pandas** - analiza danych
- **Plotly** - interaktywne wykresy
- **openpyxl** - odczyt Excel
- **NumPy** - obliczenia numeryczne

## 📊 Funkcje analizy

### Automatyczna analiza:
- ✅ Walidacja danych Excel (100% accuracy)
- ✅ Obliczanie KPI (przychody, koszty, zysk, marża)
- ✅ Analiza korelacji przychodów i kosztów
- ✅ Identyfikacja miesięcy zyskownych/stratnych
- ✅ Wykrywanie możliwości oszczędności
- ✅ Plan naprawczy (8 działań priorytetowych)

### Dashboard KPI:
- 💰 Total Revenue
- 📊 Net Profit/Loss
- 📈 Net Margin
- 💸 Total Costs
- 🎯 ROI
- ⚖️ Cost Coverage
- 💳 Liabilities
- 💡 Savings Potential

## 🎯 Jak używać symulatora

1. **Otwórz raport** w przeglądarce
2. **Przewiń do sekcji** "INTERACTIVE INVESTMENT SIMULATOR"
3. **Przesuń suwaki** - wyniki aktualizują się natychmiastowo
4. **Wypróbuj scenariusze** - kliknij jeden z gotowych buttonów
5. **Obserwuj wykres** - projekcja 12-miesięczna na dole
6. **Reset** - przywróć wartości bazowe

## 📈 Przykładowe wyniki symulacji

| Scenariusz | Wzrost przychodów | Redukcja kosztów | Potencjał roczny |
|------------|-------------------|------------------|------------------|
| Konserwatywny | +5% | -8% | ~+150k PLN |
| Umiarkowany | +12% | -15% | ~+500k PLN |
| Agresywny | +25% | -22% | ~+1.2M PLN |

## 🔧 Konfiguracja

Ścieżka do pliku Excel w `src/fp_holding_analyzer.py`:

```python
excel_path = "/Users/YOUR_USERNAME/Desktop/Tabela kosztowa doraportu.xlsx"
```

## 📝 Notatki

- **Dane źródłowe**: Excel z 14 miesięcy (sie.2024 - wrz.2025)
- **Format raportu**: HTML5 z JavaScript
- **Responsywność**: Full responsive design
- **Przeglądarka**: Wymaga nowoczesnej przeglądarki (Chrome, Firefox, Safari, Edge)

## 🤝 Autor

Michał Barański | FP HOLDING
Generated with: Python + Plotly + AI Assistance

## 📄 Licencja

Confidential - For internal use only

---

**Made with ❤️ for professional financial reporting**
