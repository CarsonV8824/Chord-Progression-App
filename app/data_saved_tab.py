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
    QFileDialog
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QTimer, QSize, QThread, QEvent

from PyQt6.QtGui import QMovie, QKeyEvent, QShortcut, QKeySequence

from data.data import make_chord_progressions_threaded

from audio.music import play_chord_concurrently

from audio.chord_libary import ChordLibrary

from database.db import Database

from.generation_tab import GenerationTab

from pathlib import Path

import os, sys, threading, time

class ChordWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, chords):
        super().__init__()
        self.chords = chords

    def run(self):
        if self.chords:
            for chord in self.chords:
                try:
                    chord = chord.replace("min", "m")
                    play_chord_concurrently(chord)      
                except Exception as e:
                    print(f"Error playing chord in data_saved_tab line 103 {chord}: {e}")
        self.finished.emit()
        
class dataSavedTab(QWidget):
    #Note: I used AI to help me with the threading implementation
    def __init__(self):
        super().__init__()

        self._play_thread = None
        self._play_worker = None
        
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

        self.play_chord_button = QPushButton("Play Selected Chord")
        self.play_chord_button.setObjectName("play_chord_button")
        self.play_chord_button.clicked.connect(self.play_chord)
        right_layout.addWidget(self.play_chord_button)

        self.export_progressions_button = QPushButton("Export Progressions")
        self.export_progressions_button.setObjectName("export_progressions_button")
        self.export_progressions_button.clicked.connect(self.export_progressions)
        right_layout.addWidget(self.export_progressions_button)



    def refresh_saved_chords(self):
        self.saved_chords.clear()
        with Database() as db:
            chords = db.get_data()
            for num, chord in enumerate(chords):
                self.saved_chords.addItem(f"{num+1}: {chord[1]}")
                self.saved_chords.item(self.saved_chords.count() - 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                try:
                    tooltip = "Notes in chords: " + str([ChordLibrary().chord_to_notes(chord_name) for chord_name in chord[1].split(", ")]).replace("'", "")
                    self.saved_chords.item(self.saved_chords.count() - 1).setToolTip(tooltip)
                except Exception as e:
                    self.saved_chords.item(self.saved_chords.count() - 1).setToolTip("Error generating tooltip: " + str(e))

    def delete_selected(self):
        item = self.saved_chords.currentItem()
        if item:
            row = self.saved_chords.row(item)
            self.saved_chords.takeItem(row)
            progression = item.text().split(": ", 1)[1]
            with Database() as d:
                d.delete_data_by_progression(progression)
            self.refresh_saved_chords()
    
    def play_chord(self):
        self.play_chord_button.setEnabled(False)
        self.other_tab.hear_chord_button.setEnabled(False)
        self.other_tab.generate_button.setEnabled(False)
        try:
            chord_prog = self.saved_chords.currentItem().text()
        except AttributeError:
            self.play_chord_button.setEnabled(True)
            self.other_tab.hear_chord_button.setEnabled(True)
            self.other_tab.generate_button.setEnabled(True)
            return

        chord_prog = chord_prog.split(": ", 1)[1]
        chord_prog = chord_prog.split(", ")

        if chord_prog == None or len(chord_prog) == 0 or chord_prog[0] == "":
            self.play_chord_button.setEnabled(True)
            self.other_tab.hear_chord_button.setEnabled(True)
            self.other_tab.generate_button.setEnabled(True)
            return

        self._play_thread = QThread()
        self._play_worker = ChordWorker(chord_prog)
        self._play_worker.moveToThread(self._play_thread)

        self._play_thread.started.connect(self._play_worker.run)
        self._play_worker.finished.connect(self._play_thread.quit)
        self._play_worker.finished.connect(self._play_worker.deleteLater)
        self._play_thread.finished.connect(self._clear_play_thread)
        self._play_thread.finished.connect(self._play_thread.deleteLater)

        self._play_worker.error.connect(lambda msg: print("Error:", msg))

        self._play_thread.start()

    def _clear_play_thread(self):
        self._play_thread = None
        self._play_worker = None
        self.play_chord_button.setEnabled(True)
        self.other_tab.hear_chord_button.setEnabled(True)
        self.other_tab.generate_button.setEnabled(True)

    def export_progressions(self):
        # Get the user's Downloads directory
        def get_downloads_folder():
            home = Path.home()
            downloads = home / "Downloads"
            return str(downloads)

        downloads_dir = get_downloads_folder()

        content = self.saved_chords.currentItem()
        if content is None:
            self.no_progression_msg = QMessageBox()
            self.no_progression_msg.setText("Please select a chord progression to export.")
            self.no_progression_msg.setWindowTitle("No Progression Selected")
            self.no_progression_msg.setIcon(QMessageBox.Icon.Warning)
            self.no_progression_msg.show()
            QTimer.singleShot(2000, self.no_progression_msg.close)
            return
        content = content.text()
        content = content.split(": ", 1)[1]
        file_path = os.path.join(downloads_dir, "chord_progressions.txt")

        try:
            with open(file_path, "a", encoding="utf-8") as f:
                list_of_chords = content.split(", ")
                f.write(content + "\n" + f"Chords: {[ChordLibrary().chord_to_notes(item) for item in list_of_chords]}" + "\n")

            self.finished_export_msg = QMessageBox()
            self.finished_export_msg.setText(f"Chord progression exported to {file_path}")
            self.finished_export_msg.setWindowTitle("Export Successful")
            self.finished_export_msg.setIcon(QMessageBox.Icon.Information)
            self.finished_export_msg.show()
            QTimer.singleShot(2000, self.finished_export_msg.close)

            print("Saved to:", file_path)
        except Exception as e:
            self.error_export_msg = QMessageBox()
            self.error_export_msg.setText(f"Error exporting chord progression: {e}")
            self.error_export_msg.setWindowTitle("Export Failed")
            self.error_export_msg.setIcon(QMessageBox.Icon.Critical)
            self.error_export_msg.show()
            QTimer.singleShot(2000, self.error_export_msg.close)
    
    def set_other_tab(self, other_tab):
        """Set reference to the other tab"""
        self.other_tab = other_tab
        #hear_chord_button