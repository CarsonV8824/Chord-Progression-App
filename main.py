import sys
from PyQt6.QtWidgets import QApplication
from app.window import MainWindow
from PyQt6.QtGui import QIcon
import os

def resource_path(rel_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, rel_path)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("styles/logo.png")))
    window = MainWindow()
    window.setWindowIcon(QIcon(resource_path("styles/logo.png")))
    window.setObjectName("main_window")

    stylesheet_path = resource_path("styles/style.css")

    with open(stylesheet_path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()