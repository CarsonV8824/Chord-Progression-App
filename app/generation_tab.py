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
    QMessageBox,
    
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QTimer, QSize

from PyQt6.QtGui import QMovie, QKeyEvent, QShortcut, QKeySequence

from data.data import make_chord_progressions_threaded

from database.db import Database

import os, sys

def resource_path(rel_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, rel_path)

class ProgressionSignal(QObject):
    progression_ready = pyqtSignal(list)

class GenerationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.signal_emitter = ProgressionSignal()
        self.signal_emitter.progression_ready.connect(self.on_progression_ready)

        # pop-up message box for notifications
        self.msg = QMessageBox()
        self.msg.setText("Chord Progression Generated and Saved!")
        self.msg.setWindowTitle("Notification")
        self.msg.setIcon(QMessageBox.Icon.Information)

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
        self.length_input.setPlaceholderText("(4-16)")
        self.right_layout.addWidget(self.length_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.generate_button = QPushButton("Generate Chord Progression")
        self.generate_button.setObjectName("generate_button")
        self.right_layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.generate_button.clicked.connect(self.generate_chord)

        self.load = QLabel()
        self.movie = QMovie(resource_path("styles/Loading_icon.gif"))
        self.movie.setScaledSize(QSize(100, 75))
        self.load.setMovie(self.movie)
        self.movie.start()
        self.right_layout.addWidget(self.load, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.load.hide()

        self.results_list_label = QLabel("Generated Chord Progressions:")
        self.results_list_label.setObjectName("results_list_label")
        self.results_list_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.left_layout.addWidget(self.results_list_label)

        self.result_list = QListWidget()
        self.result_list.setObjectName("result_list")
        self.left_layout.addWidget(self.result_list)

        delete_shortcut = QShortcut(QKeySequence("Backspace"), self)
        delete_shortcut.activated.connect(self.delete_selected)

    def delete_selected(self):
        item = self.result_list.currentItem()
        if item:
            row = self.result_list.row(item)
            self.result_list.takeItem(row)
            with Database() as d:
                d.delete_data_by_progression(item.text())

    def on_progression_ready(self, results: str):
        chord_prog = results[0].replace(" ", ", ")
        self.result_list.insertItem(0, chord_prog)
        self.result_list.item(0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        with Database() as d:
            d.add_data(chord_prog)
        
        self.msg.show()
        QTimer.singleShot(2000, self.msg.close)
        self.generate_button.setEnabled(True)

        self.load.hide()
    
    def generate_chord(self):
        self.generate_button.setEnabled(False)
        self.load.show()
        selected = self.fast_or_slow.currentText()
        length_text = self.length_input.text()

        complex_or_simple = self.simple_or_complex.currentText()

        if not length_text.isdigit() or int(length_text) <= 3 or int(length_text) > 16:
            self.not_right_length = QMessageBox()
            self.not_right_length.setText("Please enter a valid length between 4 and 16.")
            self.not_right_length.setWindowTitle("Invalid Length")
            self.not_right_length.setIcon(QMessageBox.Icon.Warning)
            self.not_right_length.show()
            QTimer.singleShot(2000, self.not_right_length.close)
            self.load.hide()
            self.generate_button.setEnabled(True)
            return
        
        if length_text.isdigit() and int(length_text) > 0:
            self.length_label.setText("Length of Chord Progression:")
        
        def on_progression_ready_thread(results: str):
            
            self.signal_emitter.progression_ready.emit(results)

        try:
            filepath = resource_path("data/chords.zip")
        except FileNotFoundError as e:
            print(e)
            filepath = "data/chords.zip"
        match complex_or_simple:
            case "popular":
                try:
                    filepath = resource_path("data/chords.zip")
                except FileNotFoundError as e:
                    print(e)
                    filepath = "data/chords.zip"
            case "jazz":
                try:
                    filepath = resource_path("data/complex_chords.zip")
                except FileNotFoundError as e:
                    print(e)
                    filepath = "data/complex_chords.zip"

        match selected:
            case "fast generation":
                make_chord_progressions_threaded(filepath, int(length_text), lines_to_read=10000, num_progressions=1, callback=on_progression_ready_thread)
            case "slow generation":
                make_chord_progressions_threaded(filepath, int(length_text), lines_to_read=100000, num_progressions=1, callback=on_progression_ready_thread)
                