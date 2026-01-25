import sys
from PyQt6.QtWidgets import QApplication
from app.window import MainWindow

import os

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setObjectName("main_window")

    stylesheet_path = os.path.join(os.path.dirname(__file__), "styles/style.css")

    with open(stylesheet_path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
