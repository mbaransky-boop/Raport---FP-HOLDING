"""Generowanie raportu HTML przy użyciu Jinja2"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


def generate_report(summary: dict, output_path: str, template_dir: str = None):
    output_path = Path(output_path)
    template_dir = Path(template_dir) if template_dir else Path(__file__).resolve().parents[1] / 'reports' / 'templates'

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('report.html.j2')
    rendered = template.render(summary=summary)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding='utf-8')
    return str(output_path)
