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

class GenerationTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main horizontal layout to hold left and right sections
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left container with result list
        self.left_widget = QWidget()
        self.left_widget.setObjectName("left_widget")
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)
        main_layout.addWidget(self.left_widget)

        # Right container with controls
        # Right container with controls
        self.right_widget = QWidget()
        self.right_widget.setObjectName("right_widget")
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)  # Center horizontally
        self.right_widget.setLayout(self.right_layout)
        main_layout.addWidget(self.right_widget)

        self.chord_label = QLabel("Make a chord Progression")
        self.chord_label.setObjectName("chord_label")
        self.chord_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.right_layout.addWidget(self.chord_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.fast_or_slow = QComboBox()
        self.fast_or_slow.setObjectName("fast_or_slow")
        self.fast_or_slow.addItems(["fast generation", "slow generation"])
        self.right_layout.addWidget(self.fast_or_slow, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.simple_or_complex = QComboBox()
        self.simple_or_complex.setObjectName("simple_or_complex")
        self.simple_or_complex.addItems(["popular", "jazz"])
        self.right_layout.addWidget(self.simple_or_complex, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.length_label = QLabel("Length of Chord Progression:")
        self.length_label.setObjectName("length_label")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.right_layout.addWidget(self.length_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.length_input = QLineEdit()
        self.length_input.setObjectName("length_input")
        self.length_input.setPlaceholderText("Enter a number (e.g., 2)")
        self.right_layout.addWidget(self.length_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.generate_button = QPushButton("Generate Chord Progression")
        self.generate_button.setObjectName("generate_button")
        self.right_layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.generate_button.clicked.connect(self.generate_chord)

        self.result_list = QListWidget()
        self.result_list.setObjectName("result_list")
        self.left_layout.addWidget(self.result_list)

    
    def generate_chord(self):
        selected = self.fast_or_slow.currentText()
        length_text = self.length_input.text()

        complex_or_simple = self.simple_or_complex.currentText()

        if not length_text.isdigit() or int(length_text) <= 0 or int(length_text) > 16:
            self.length_label.setText("Please enter a valid positive integer for length (1-16).")
            return
        
        if length_text.isdigit() and int(length_text) > 0:
            self.length_label.setText("Length of Chord Progression:")
        
        def on_progression_ready(results:str):
            chord_prog = results[0].replace(" ", ", ")
            self.result_list.insertItem(0, chord_prog)
            self.result_list.item(self.result_list.count() - 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            with Database() as d:
                d.add_data(chord_prog)
        
        filepath = "data/chords.zip"
        match complex_or_simple:
            case "popular":
                filepath = "data/chords.zip"
            case "jazz":
                filepath = "data/complex_chords.zip"

        match selected:
            case "fast generation":
                make_chord_progressions_threaded(filepath, int(length_text), lines_to_read=10000, num_progressions=1, callback=on_progression_ready)
            case "slow generation":
                make_chord_progressions_threaded(filepath, int(length_text), lines_to_read=100000, num_progressions=1, callback=on_progression_ready)