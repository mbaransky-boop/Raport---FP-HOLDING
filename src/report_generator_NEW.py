"""
Generator interaktywnego raportu HTML
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    """Generator raportu HTML z wykresami"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.analysis = analyzer.analysis
