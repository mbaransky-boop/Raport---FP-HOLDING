"""
Lokalny serwer HTTP do wyświetlania raportu FP HOLDING
"""
import http.server
import socketserver
import webbrowser
import time
import threading
from pathlib import Path
import os


PORT = 8000


def open_browser():
    """Otwórz przeglądarkę po 2 sekundach"""
    time.sleep(2)
    url = f'http://localhost:{PORT}/reports/fp_holding_raport.html'
    print(f"🌐 Otwieram przeglądarkę: {url}")
    webbrowser.open(url)


def main():
    # Sprawdź czy raport istnieje
    report = Path('reports/fp_holding_raport.html')
    
    if not report.exists():
        print("❌ Raport nie istnieje!")
        print("\n📝 Najpierw wygeneruj raport:")
        print("   python3 generate_fp_report.py")
        return
    
    print("=" * 80)
    print("🚀 URUCHAMIANIE LOKALNEGO SERWERA")
    print("=" * 80)
    print(f"\n📡 Serwer: http://localhost:{PORT}")
    print(f"📊 Raport: http://localhost:{PORT}/reports/fp_holding_raport.html")
    print("\n🌐 Przeglądarka otworzy się automatycznie za 2 sekundy...")
    print("\n⚠️  Aby zatrzymać serwer: naciśnij Ctrl+C")
    print("=" * 80 + "\n")
    
    # Otwórz przeglądarkę w osobnym wątku
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Uruchom serwer
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Serwer działa na porcie {PORT}")
            print(f"✅ Raport dostępny pod: http://localhost:{PORT}/reports/fp_holding_raport.html\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Serwer zatrzymany")
        print("💡 Raport pozostaje w folderze 'reports/' i można go otworzyć bezpośrednio")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {PORT} jest już zajęty!")
            print(f"\n💡 Zatrzym inny serwer lub użyj innego portu:")
            print(f"   python3 -m http.server 8080")
        else:
            print(f"\n❌ Błąd: {e}")


if __name__ == "__main__":
    main()
