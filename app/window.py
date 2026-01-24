from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QTabWidget,
    QListWidget,
    QLineEdit
)
from PyQt6.QtCore import Qt

from data.data import make_chord_progression

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

        self.length_label = QLabel("Length of Chord Progression:")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter a number (e.g., 2)")
        
        self.confirm_button = QPushButton("generate")

        self.confirm_button.clicked.connect(self.generate_chord)

        self.chord_progressions = QListWidget()

        tab1_layout.addWidget(self.chord_label)
        tab1_layout.addWidget(self.fast_or_slow)
        tab1_layout.addWidget(self.length_label)
        tab1_layout.addWidget(self.length_input)
        tab1_layout.addWidget(self.confirm_button)
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
        
        match selected:
            case "fast generation":chord_prog = make_chord_progression("data/10kchords.zip", int(length_text))
            case "slow generation":chord_prog = make_chord_progression("data/chords.zip", int(length_text))
        chord_prog = chord_prog.replace(" ", ", ")
        self.chord_progressions.insertItem(0, chord_prog)

        with Database() as d:
            d.add_data(chord_prog)