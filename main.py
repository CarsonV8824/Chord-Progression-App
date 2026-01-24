import sys
from PyQt6.QtWidgets import QApplication
from app.window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    with open("styles/style.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)


    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
