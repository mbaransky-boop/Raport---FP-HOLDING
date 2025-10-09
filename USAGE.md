# 📖 Instrukcja użytkowania - FP HOLDING Financial Dashboard

## 🚀 Szybki start (3 kroki)

### Krok 1: Wygeneruj raport
```bash
cd Raport---FP-HOLDING
python3 generate_report.py
```

Otrzymasz:
```
✅ SUKCES!
📊 Raport: reports/fp_holding_raport.html
```

### Krok 2: Uruchom serwer
```bash
python3 -m http.server 8000
```

### Krok 3: Otwórz w przeglądarce
```
http://localhost:8000/reports/fp_holding_raport.html
```

---

## 🎨 Nawigacja po raporcie

### Sekcje raportu:

1. **📊 HEADER** (góra strony)
   - Tytuł i data wygenerowania
   - Metadane: okres, liczba okresów, status

2. **I. EXECUTIVE SUMMARY**
   - Streszczenie zarządcze
   - Kluczowe metryki finansowe
   - Highlight box z wynikami

3. **⚠️ ZOBOWIĄZANIA KRYTYCZNE**
   - US VAT: 50,135 PLN
   - ZUS (1. rata): 90,000 PLN
   - Suma: 816,730 PLN

4. **II. KPI DASHBOARD**
   - 8 interaktywnych kart:
     - 💰 Total Revenue
     - 📊 Net Profit/Loss
     - 📈 Net Margin
     - 💸 Total Costs
     - 🎯 ROI
     - ⚖️ Cost Coverage
     - 💳 Liabilities
     - 💡 Savings Potential

5. **III. DATA ANALYTICS**
   - 4 interaktywne wykresy Plotly:
     - 3.1. Korelacja przychodów vs koszty
     - 3.2. Trend przychodów i kosztów
     - 3.3. Rentowność miesięczna
     - 3.4. Zobowiązania ZUS

6. **🚀 INTERACTIVE SIMULATOR** ⭐
   - Panel kontrolny (lewo)
   - Panel wyników (prawo)
   - Wykres projekcji 12-miesięcznej (dół)

7. **IV. STRATEGIC RECOMMENDATIONS**
   - Plan działań naprawczych
   - Priorytety (Critical → Long-term)

8. **V. CONCLUSION**
   - Podsumowanie i wnioski końcowe

---

## 🎯 Jak używać Interactive Simulator

### Panel kontrolny (5 suwaków):

#### 1. 📈 Wzrost przychodów
- **Zakres**: -20% do +50%
- **Przykład**: +15% = wzrost sprzedaży o 15%
- **Wpływ na**: Przychody, Marża, Zysk

#### 2. 💰 Redukcja kosztów operacyjnych
- **Zakres**: 0% do 30%
- **Przykład**: -10% = redukcja kosztów o 10%
- **Wpływ na**: Koszty, Marża, Zysk

#### 3. 📊 Wzrost średniego rachunku
- **Zakres**: 0% do 40%
- **Przykład**: +12% = droższe produkty/upselling
- **Wpływ na**: Przychody (dodatkowo)

#### 4. 👥 Optymalizacja zatrudnienia
- **Zakres**: 0% do 25%
- **Przykład**: -15% = mniej kosztów pracowniczych
- **Wpływ na**: Koszty (40% wagi)

#### 5. 🏛️ Redukcja zobowiązań ZUS
- **Zakres**: 0% do 20%
- **Przykład**: -10% = optymalizacja umów
- **Wpływ na**: Koszty (15% wagi)

### Gotowe scenariusze (przyciski):

#### 📊 Konserwatywny
```
Przychody: +5%
Koszty: -8%
Ticket: +5%
Labor: -5%
ZUS: -3%

Wynik: ~+150k PLN rocznie
```

#### 📈 Umiarkowany
```
Przychody: +12%
Koszty: -15%
Ticket: +12%
Labor: -10%
ZUS: -8%

Wynik: ~+500k PLN rocznie
```

#### 🚀 Agresywny
```
Przychody: +25%
Koszty: -22%
Ticket: +20%
Labor: -18%
ZUS: -15%

Wynik: ~+1.2M PLN rocznie
```

#### ⚖️ Break-even
- Automatycznie oblicza parametry potrzebne do wyjścia na zero
- Pokazuje minimalną redukcję kosztów

---

## 📊 Interpretacja wyników

### Panel wyników pokazuje:

1. **Przychody Netto (Średnio)**
   - Nowa wartość miesięczna
   - Zmiana vs. obecny stan

2. **Koszty Operacyjne (Średnio)**
   - Nowa wartość miesięczna
   - Zmiana vs. obecny stan

3. **Wynik Netto (Średnio)**
   - 🟢 Zielony = Zysk
   - 🔴 Czerwony = Strata
   - Zmiana vs. obecny stan

4. **Marża Netto**
   - Procent rentowności
   - Zmiana w punktach procentowych

5. **Potencjał Roczny**
   - Dodatkowy zysk (lub oszczędności)
   - Wartość roczna (× 12 miesięcy)

### Wykres projekcji 12-miesięcznej:

- **🟢 Zielona linia** = Przychody (z fill)
- **🟠 Pomarańczowa linia** = Koszty (z fill)
- **🟢/🔴 Słupki** = Zysk/Strata
  - Zielony = miesiące zyskowne
  - Różowy = miesiące stratne

---

## 💡 Przykłady użycia

### Scenariusz 1: "Potrzebuję wyjść na zero"
1. Kliknij przycisk **⚖️ Break-even**
2. Symulator obliczy minimalną redukcję kosztów
3. Sprawdź wykres - wszystkie miesiące na poziomie 0

### Scenariusz 2: "Chcę zwiększyć przychody o 20%"
1. Przesuń suwak **📈 Wzrost przychodów** na +20%
2. Obserwuj zmianę w panelu wyników
3. Sprawdź **Potencjał Roczny**

### Scenariusz 3: "Co jeśli zredukuję koszty o 10% i zwiększę ticket o 15%?"
1. **💰 Redukcja kosztów** → -10%
2. **📊 Wzrost średniego rachunku** → +15%
3. Zobacz łączny efekt w **Wynik Netto**
4. Sprawdź wykres projekcji

### Scenariusz 4: "Testowanie różnych wariantów"
1. Kliknij **📊 Konserwatywny** - zobacz wynik
2. Kliknij **📈 Umiarkowany** - porównaj
3. Kliknij **🚀 Agresywny** - sprawdź maksimum
4. **🔄 RESET** - wróć do wartości bazowych

---

## 🎨 Funkcje interaktywne

### Hover effects:
- **Karty KPI**: Powiększają się i świecą
- **Wykresy**: Tooltips z dokładnymi wartościami
- **Suwaki**: Thumbs powiększają się i świecą
- **Przyciski**: Animacja podniesienia

### Real-time updates:
- Każda zmiana suwaka → natychmiastowa aktualizacja
- Kolory zmieniają się dynamicznie:
  - 🟢 Zielony = wzrost/poprawa
  - 🔴 Czerwony = spadek/pogorszenie
  - ⚪ Szary = bez zmian

### Responsywność:
- Desktop: 2 kolumny (controls + results)
- Tablet/Mobile: 1 kolumna (stack)
- Wykresy: Auto-resize przy zmianie okna

---

## 🔧 Zaawansowane

### Edycja danych źródłowych:
```python
# src/fp_holding_analyzer.py (linia ~30)
excel_path = "/path/to/your/excel.xlsx"
```

### Zmiana kolorystyki:
```css
/* W pliku report_generator.py, sekcja <style> */
--primary-color: #3B82F6;  /* Niebieski */
--success-color: #06FFA5;  /* Zielony */
--danger-color: #FF006E;   /* Różowy */
```

### Export danych:
```bash
# Wygeneruj CSV z wynikami
python3 -c "from src.fp_holding_analyzer import *; analyzer = FPHoldingAnalyzer(); analyzer.export_to_csv()"
```

---

## ❓ FAQ

**Q: Jak często mogę generować raport?**
A: Tak często jak chcesz - każde uruchomienie `generate_report.py` tworzy nowy raport.

**Q: Czy mogę edytować parametry w kodzie?**
A: Tak, wszystkie wartości bazowe są w `src/fp_holding_analyzer.py`.

**Q: Czy raport działa offline?**
A: Nie całkiem - wykresy Plotly wymagają CDN (internet). Ale sam raport HTML jest lokalny.

**Q: Jak zapisać wyniki symulacji?**
A: Użyj screenshot (Cmd+Shift+4 na Mac) lub Print to PDF w przeglądarce.

**Q: Czy mogę zmienić język na angielski?**
A: Tak, edytuj stringi w `report_generator.py` w sekcji HTML.

---

## 📞 Support

W razie problemów:
1. Sprawdź, czy wszystkie zależności są zainstalowane (`pip install -r requirements.txt`)
2. Upewnij się, że plik Excel istnieje i jest dostępny
3. Sprawdź konsolę przeglądarki (F12) dla błędów JavaScript

---

**Happy analyzing! 📊💰🚀**
