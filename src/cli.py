"""
Prosty CLI dla generatora raportów sprzedażowych.
"""
import argparse
import sys
from pathlib import Path
from sales_reports.src import ingest, analysis, report


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Sales reports generator CLI")
    p.add_argument("--input", "-i", required=True, help="Ścieżka do pliku CSV z danymi sprzedaży")
    p.add_argument("--output", "-o", required=True, help="Ścieżka do wygenerowanego raportu HTML")
    p.add_argument("--format", "-f", choices=["html","pdf"], default="html", help="Format raportu")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Błąd: brak pliku wejściowego: {input_path}")
        sys.exit(2)

    print(f"Wczytuję dane z: {input_path}")
    df = ingest.read_sales_csv(str(input_path))
    summary = analysis.summarize_sales(df)

    print(f"Generuję raport...")
    out = report.generate_report(summary, str(output_path))
    print(f"Wygenerowano raport: {out}")


if __name__ == "__main__":
    main()
