import librosa
import numpy as np
from pychord import Chord
from scipy.io.wavfile import write
import pygame
import tempfile
import os
import time

def create_temp_wav(freq:float=440, duration:float=1.0, sr:int=44100) -> str:
    """
    Docstring for create_temp_wav
    
    :param freq: Frequency of the sine wave in Hz
    :param duration: Duration of the audio in seconds
    :param sr: Sampling rate in Hz
    :return: Path to the temporary WAV file
    """
    t = np.linspace(0, duration, int(sr * duration), False)
    audio = 0.3 * np.sin(2 * np.pi * freq * t)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    path = tmp.name
    tmp.close()  

    write(path, sr, audio.astype(np.float32))
    return path

def play_audio(file_path: str):
    """
    Docstring for play_audio
    
    :param file_path: Path to the WAV file to be played
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(file_path)

if __name__ == "__main__":

    # Canonical 12 pitch classes for MIDI math
    PITCH_CLASSES = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    # Enharmonic equivalents → canonical names
    ENHARMONIC_MAP = {
        "B#": "C",
        "Db": "C#",
        "Eb": "D#",
        "Fb": "E",
        "E#": "F",
        "Gb": "F#",
        "Ab": "G#",
        "Bb": "A#",
        "Cb": "B"
    }

    def normalize_name(name):
        """Convert enharmonic spellings to canonical pitch class."""
        return ENHARMONIC_MAP.get(name, name)

    def note_to_midi(note):
        """Convert note name like 'C#4' to MIDI number."""
        name = normalize_name(note[:-1])
        octave = int(note[-1])
        return PITCH_CLASSES.index(name) + (octave + 1) * 12

    def midi_to_note_name(midi):
        """Convert MIDI number back to canonical note name."""
        name = PITCH_CLASSES[midi % 12]
        octave = midi // 12 - 1
        return f"{name}{octave}"

    # --------------------------
    # Build chord notes with correct octave handling
    # --------------------------

    base_octave = 4
    prev_midi = None
    all_notes = []

    try:
        chord_notes = Chord("Bbmin11").components() 
    except Exception as e:
        print("Error parsing chord:", e)

    for n in chord_notes:
        midi = note_to_midi(n + str(base_octave))

        # Ensure notes ascend properly
        if prev_midi is not None and midi <= prev_midi:
            midi += 12

        all_notes.append(midi_to_note_name(midi))
        prev_midi = midi

    print("Notes:", all_notes)

    # --------------------------
    # Play each note
    # --------------------------

    for note in all_notes:
        freq = librosa.note_to_hz(note)
        print(note, freq)
        wav_path = create_temp_wav(freq=freq, duration=1.0)
        play_audio(wav_path)




        

