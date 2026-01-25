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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chord Progression App")
        self.setGeometry(100, 100, 400, 300)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # First tab
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1.setLayout(tab1_layout)
        tabs.addTab(tab1, "Create Chord Progressions")

        self.chord_label = QLabel("Make a chord Progression")
        self.chord_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.fast_or_slow = QComboBox()
        self.fast_or_slow.addItems(["fast generation", "slow generation"])

        confirm_fast_or_slow = QHBoxLayout()
        confirm_fast_or_slow.addStretch()
        confirm_fast_or_slow.addWidget(self.fast_or_slow)
        confirm_fast_or_slow.addStretch()

        self.length_label = QLabel("Length of Chord Progression:")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter a number (e.g., 2)")

        centerd_length_input = QHBoxLayout()
        centerd_length_input.addStretch()
        centerd_length_input.addWidget(self.length_input)
        centerd_length_input.addStretch()
        
        self.confirm_button = QPushButton("generate")

        self.confirm_button.clicked.connect(self.generate_chord)

        confirm_button_center = QHBoxLayout()
        confirm_button_center.addStretch()
        confirm_button_center.addWidget(self.confirm_button)
        confirm_button_center.addStretch()

        self.chord_progressions = QListWidget()

        tab1_layout.addWidget(self.chord_label)
        tab1_layout.addLayout(confirm_fast_or_slow)
        tab1_layout.addWidget(self.length_label)
        tab1_layout.addLayout(centerd_length_input)
        tab1_layout.addLayout(confirm_button_center)
        tab1_layout.addWidget(self.chord_progressions)
        
        
        tab1_layout.addStretch()

        # second tab

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()

        self.previous_progressions = QListWidget()

        with Database() as f:
            data = f.get_data()

            for index, line in enumerate(data):
                self.previous_progressions.insertItem(index, f"{line[0]}: {line[1]}")

        tab2.setLayout(tab2_layout)
        tabs.addTab(tab2, "Saved Chord Progressions")

        tab2_layout.addWidget(self.previous_progressions)

    def generate_chord(self):
        selected = self.fast_or_slow.currentText()
        length_text = self.length_input.text()

        if not length_text.isdigit() or int(length_text) <= 0 or int(length_text) > 20:
            self.length_label.setText("Please enter a valid positive integer for length (1-20).")
            return
        
        if length_text.isdigit() and int(length_text) > 0:
            self.length_label.setText("Length of Chord Progression:")
        
        
        def on_progression_ready(results:str):
            chord_prog = results[0].replace(" ", ", ")
            self.chord_progressions.insertItem(0, chord_prog)
            with Database() as d:
                d.add_data(chord_prog)
        
        match selected:
            case "fast generation":
                make_chord_progressions_threaded("data/chords.zip", int(length_text), lines_to_read=10000, num_progressions=1, callback=on_progression_ready)
            case "slow generation":
                make_chord_progressions_threaded("data/chords.zip", int(length_text), lines_to_read=100000, num_progressions=1, callback=on_progression_ready)