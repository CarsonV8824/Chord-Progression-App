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
    temp_wav_path = create_temp_wav(freq=440, duration=2.0)
    play_audio(temp_wav_path)

    chord = Chord("Cmaj13")
    print(chord.components())