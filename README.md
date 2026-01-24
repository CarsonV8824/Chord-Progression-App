# 🎵 Chord Progression Generator

A desktop application built with PyQt6 that generates chord progressions using Markov chain models trained on a dataset of musical chord sequences.

## ✨ Features

- **🤖 AI-Powered Generation**: Uses Markov chain models to generate realistic chord progressions
- **⚡ Dual Generation Modes**:
  - **🚀 Fast Generation**: Trains on 10,000 lines for quick results
  - **🐢 Slow Generation**: Trains on 100,000 lines for more diverse progressions
- **📏 Customizable Length**: Specify the number of chords in your progression (1-20 chords)
- **💾 History Management**: Automatically saves generated progressions to a local database
- **🔄 Multi-threaded Processing**: Non-blocking UI with background generation using thread pools
- **🎨 Modern Interface**: Clean, dark-themed UI built with PyQt6

## 📋 Prerequisites

- Python 3.8+
- PyQt6
- markovify
- SQLite3 (included with Python)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Chord-Progression-App.git
cd Chord-Progression-App
pip install PyQt6 markovify
```

## 📂 Project Structure

Chord-Progression-App/
│
├── app/
│   └── window.py          # Main application window and UI logic
│
├── data/
│   ├── data.py            # Markov model generation and threading logic
│   └── chords.zip         # Training dataset (not included)
│
├── database/
│   └── db.py              # SQLite database management
│
├── styles/
│   └── style.qss          # Qt stylesheet for UI theming
│
└── main.py                # Application entry point

## 🎮 Usage

```bash
python main.py
```

