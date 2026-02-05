import librosa
import numpy as np
from audio.chord_libary import ChordLibrary
from scipy.io.wavfile import write
import pygame
import tempfile
import os
import time
import threading

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

def play_audio(path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(path)
    sound.play()
    time.sleep(sound.get_length())
    os.remove(path)


def play_chord_concurrently(chord_str: str="Cmin"):    
    """
    Play the notes of a chord concurrently, ensuring correct octave handling.
    """    # --------------------------
    # Note name to MIDI conversion utilities

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
        chord_notes = ChordLibrary().chord_to_notes(chord_str)
    except Exception as e:
        print(f"Error parsing chord '{chord_str}': {e}")
        return

    for n in chord_notes:
        midi = note_to_midi(n + str(base_octave))

        # Ensure notes ascend properly
        if prev_midi is not None and midi <= prev_midi:
            midi += 12

        all_notes.append(midi_to_note_name(midi))
        prev_midi = midi

    print("Notes:", all_notes)

    # --------------------------
    # Play each note concurrently
    # --------------------------

    threads: list[threading.Thread] = []

    for note in all_notes:
        freq = librosa.note_to_hz(note)
        wav_path = create_temp_wav(freq=freq, duration=1.0)

        t = threading.Thread(target=play_audio, args=(wav_path,))
        threads.append(t)
        t.start()

    while any(t.is_alive() for t in threads):
        time.sleep(0.01)

    pygame.mixer.quit()

if __name__ == "__main__":
    play_chord_concurrently("Bbmin9")


