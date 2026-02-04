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
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QTimer, QSize

from PyQt6.QtGui import QMovie, QKeyEvent, QShortcut, QKeySequence

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
        
        self.store_text = QLabel("Saved Chord Progressions:")
        self.store_text.setObjectName("store_text")
        self.store_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.store_text)

        self.saved_chords = QListWidget()
        self.saved_chords.setObjectName("saved_chords")
        self.container_layout.addWidget(self.saved_chords)

        self.refresh_saved_chords()

        delete_shortcut = QShortcut(QKeySequence("Backspace"), self)
        delete_shortcut.activated.connect(self.delete_selected)

        #Right container for buttons
        
        right_container = QWidget()
        right_container.setObjectName("right_container_data_saved")
        right_layout = QVBoxLayout()
        right_container.setLayout(right_layout)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(right_container)
        
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_selected)
        right_layout.addWidget(self.delete_button)


    def refresh_saved_chords(self):
        self.saved_chords.clear()
        with Database() as db:
            chords = db.get_data()
            for num, chord in enumerate(chords):
                self.saved_chords.addItem(f"{num+1}: {chord[1]}")
                self.saved_chords.item(self.saved_chords.count() - 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def delete_selected(self):
        item = self.saved_chords.currentItem()
        if item:
            row = self.saved_chords.row(item)
            self.saved_chords.takeItem(row)
            progression = item.text().split(": ", 1)[1]
            with Database() as d:
                d.delete_data_by_progression(progression)
            self.refresh_saved_chords()

        
    