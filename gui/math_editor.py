from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import os


class MathEditor(QWebEngineView):

    def __init__(self):
        super().__init__()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "..", "web", "editor.html")
        html_path = os.path.abspath(html_path)

        self.load(QUrl.fromLocalFile(html_path))

    def get_latex(self, callback):
        self.page().runJavaScript("getLatex();", callback)