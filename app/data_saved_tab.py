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

from.generation_tab import GenerationTab

class dataSavedTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout matching generation_tab structure
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Container
        self.container = QWidget()
        self.container.setObjectName("data_saved_container")
        self.container_layout = QVBoxLayout()
        self.container.setLayout(self.container_layout)
        main_layout.addWidget(self.container)
        
        self.saved_chords = QListWidget()
        self.saved_chords.setObjectName("saved_chords")
        self.container_layout.addWidget(self.saved_chords)

        with Database() as db:
            chords = db.get_data()
            for chord in chords:
                self.saved_chords.addItem(f"{chord[0]}: {chord[1]}")  
                self.saved_chords.item(self.saved_chords.count() - 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    