import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.resize(900, 500)
window.show()
sys.exit(app.exec())