from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QTabWidget,
    QListWidget,
    QLineEdit,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from data.data import make_chord_progressions_threaded

from database.db import Database

from app.generation_tab import GenerationTab

from app.data_saved_tab import dataSavedTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chord Progression App")
        self.setGeometry(100, 100, 400, 300)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.this_layout = QVBoxLayout()
        self.central_widget.setLayout(self.this_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs_widget")
        self.this_layout.addWidget(self.tabs)

        # first tab
        self.generation_tab = GenerationTab()
        self.generation_tab.setObjectName("generation_tab")
        self.tabs.addTab(self.generation_tab, "Generate Chord Progression")

        # second tab
        self.data_saving_tab = dataSavedTab()
        self.tabs.addTab(self.data_saving_tab, "Saved Chord Progressions")

        # Link tabs for button state management
        self.generation_tab.set_other_tab(self.data_saving_tab)
        self.data_saving_tab.set_other_tab(self.generation_tab)
