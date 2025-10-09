#!/usr/bin/env python3
"""
Kompletny workflow: generuj raport + uruchom serwer
"""
import sys
import subprocess
import webbrowser
import http.server
import socketserver
import threading
import time
from pathlib import Path

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from fp_analyzer import FPHoldingAnalyzer
    from report_generator import ReportGenerator
    LIBS_OK = True
except ImportError:
    LIBS_OK = False

PORT = 8000

def install_dependencies():
    """Zainstaluj zależności"""
    print("📦 Instaluję zależności...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'pandas', 'openpyxl', 'plotly', 'numpy', '-q'
        ], check=True)
        print("✅ Zależności zainstalowane")
        return True
    except:
        print("⚠️  Zainstaluj ręcznie: pip3 install pandas openpyxl plotly numpy")
        return False

def generate_report():
    """Wygeneruj raport"""
    print("\n📊 Generuję raport...")
    
    excel_file = "/Users/michalbaranski/Desktop/Tabela kosztowa doraportu.xlsx"
    
    if not Path(excel_file).exists():
        print(f"❌ Brak pliku: {excel_file}")
        return False
    
    try:
        from fp_analyzer import FPHoldingAnalyzer
        from report_generator import ReportGenerator
        
        analyzer = FPHoldingAnalyzer(excel_file)
        if not analyzer.run_full_analysis():
            return False
        
        report_gen = ReportGenerator(analyzer)
        report_path = report_gen.generate_html()
        print(f"✅ Raport: {report_path}")
        return True
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

def open_browser():
    """Otwórz przeglądarkę"""
    time.sleep(2)
    url = f'http://localhost:{PORT}/reports/fp_holding_raport.html'
    webbrowser.open(url)

def start_server():
    """Uruchom serwer"""
    print("\n🌐 Uruchamiam serwer...")
    print(f"📡 Adres: http://localhost:{PORT}/reports/fp_holding_raport.html")
    print("⚠️  Zatrzymaj: Ctrl+C\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("✅ Serwer działa!\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Zatrzymano")

def main():
    print("=" * 80)
    print("🚀 FP HOLDING - AUTOMATYCZNY RAPORT")
    print("=" * 80)
    
    # Sprawdź biblioteki
    if not LIBS_OK:
        print("\n⚠️  Brak wymaganych bibliotek")
        if not install_dependencies():
            return 1
    
    # Generuj raport
    if not generate_report():
        return 1
    
    # Uruchom serwer
    start_server()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
