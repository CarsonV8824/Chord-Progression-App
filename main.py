import sys
from PyQt6.QtWidgets import QApplication
from app.window import MainWindow

from PyQt6.QtGui import QIcon

import os

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "styles", "logo.png")))
    window = MainWindow()
    window.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "styles", "logo.png")))
    window.setObjectName("main_window")

    stylesheet_path = os.path.join(os.path.dirname(__file__), "styles", "style.css")

    with open(stylesheet_path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
