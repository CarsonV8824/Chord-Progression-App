class ChordLibrary:
    """custom chord library for mapping chord names to their constituent notes."""
    #Note: I used AI to help me make this when I got stuck
    NOTE_TO_INT: dict[str, int] = {
        "C": 0, "B#": 0, "C#": 1, "Db": 1,
        "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "Fb": 4, "E#": 5,
        "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10,
        "B": 11, "Cb": 11
    }

    INT_TO_NOTE: dict[int, str] = {
        v: k for k, v in NOTE_TO_INT.items()
    }

    CHORD_FORMULAS = {
        # --- TRIADS ---
        "":        [0, 4, 7],     
        "m":       [0, 3, 7],
        "min":     [0, 3, 7],    
        "dim":     [0, 3, 6],      
        "aug":     [0, 4, 8],      
        "sus2":    [0, 2, 7],      
        "sus4":    [0, 5, 7],      

        # --- POWER CHORD ---
        "5":       [0, 7],
        "no3rd":   [0, 7],
        "no3d":    [0, 7],        

        # --- SIXTH CHORDS ---
        "6":       [0, 4, 7, 9],  
        "m6":      [0, 3, 7, 9],  

        # --- SEVENTH CHORDS ---
        "7":       [0, 4, 7, 10],  
        "maj7":    [0, 4, 7, 11],  
        "M7":      [0, 4, 7, 11],  
        "m7":      [0, 3, 7, 10], 
        "min7":    [0, 3, 7, 10], 
        "mMaj7":   [0, 3, 7, 11],  
        "dim7":    [0, 3, 6, 9],   
        "m7b5":    [0, 3, 6, 10],  
        "ø":       [0, 3, 6, 10],  

        # --- NINTH CHORDS ---
        "9":       [0, 4, 7, 10, 14],      
        "maj9":    [0, 4, 7, 11, 14],      
        "m9":      [0, 3, 7, 10, 14],      
        "mMaj9":   [0, 3, 7, 11, 14],       
        "dim9":    [0, 3, 6, 9, 14],       

                                      

        # --- ELEVENTH CHORDS ---
        "11":      [0, 4, 7, 10, 14, 17],  
        "maj11":   [0, 4, 7, 11, 14, 17],
        "m11":     [0, 3, 7, 10, 14, 17],
        "mMaj11":  [0, 3, 7, 11, 14, 17],
        "dim11":   [0, 3, 6, 9, 14, 17],

        # --- THIRTEENTH CHORDS ---
        "13":      [0, 4, 7, 10, 14, 17, 21],
        "maj13":   [0, 4, 7, 11, 14, 17, 21],
        "m13":     [0, 3, 7, 10, 14, 17, 21],
        "mMaj13":  [0, 3, 7, 11, 14, 17, 21],
        "dim13":   [0, 3, 6, 9, 14, 17, 21],

        # --- ALTERED DOMINANTS ---
        "7b5":     [0, 4, 6, 10],
        "7#5":     [0, 4, 8, 10],
        "7b9":     [0, 4, 7, 10, 13],
        "7#9":     [0, 4, 7, 10, 15],
        "7#11":    [0, 4, 7, 10, 18],
        "7b13":    [0, 4, 7, 10, 20],
        "7alt":    [0, 4, 6, 10, 13, 15, 20],


        # --- ADD CHORDS ---
        "add9":    [0, 4, 7, 14],
        "madd9":   [0, 3, 7, 14],
        "minadd9":  [0, 3, 7, 14],
        "add11":   [0, 4, 7, 17],
        "add#11":  [0, 4, 7, 18],
        "add13":   [0, 4, 7, 21],
        "madd11":  [0, 3, 7, 17],
        "minadd11": [0, 3, 7, 17],
        "madd13":  [0, 3, 7, 21],
        "minadd13": [0, 3, 7, 21],


        # --- SUSPENDED + EXTENSIONS ---
        "sus2add9": [0, 2, 7, 14],
        "sus4add9": [0, 5, 7, 14],
        "7sus4":    [0, 5, 7, 10],
        "9sus4":    [0, 5, 7, 10, 14],


        # --- AUGMENTED / DIMINISHED EXTENSIONS ---
        "aug7":    [0, 4, 8, 10],
        "augMaj7": [0, 4, 8, 11],
        "dimMaj7": [0, 3, 6, 11],
        "dim7b9":  [0, 3, 6, 9, 13],

        # --- SIXTH/SEVENTH COMBOS ---
        "6/9":     [0, 4, 7, 9, 14],
        "m6/9":    [0, 3, 7, 9, 14],

        # --- OTHER CHORD TYPES ---
        "69":      [0, 4, 7, 9, 14],
        "m79":     [0, 3, 7, 10, 14, 21],
        "min79":    [0, 3, 7, 10, 14, 21],
        "79":      [0, 4, 7, 10, 14, 21],
        "m711":    [0, 3, 7, 10, 14, 17],
        "min711":   [0, 3, 7, 10, 14, 17],
        "711":     [0, 4, 7, 10, 14, 17],
        "m713":   [0, 3, 7, 10, 14, 21],
        "maj713":  [0, 4, 7, 11, 14, 21],
        "m11b13":  [0, 3, 7, 10, 14, 17, 20],
        "11b13":   [0, 4, 7, 10, 14, 17, 20],
        "13b9":    [0, 4, 7, 10, 13, 21],
        "m13b9":   [0, 3, 7, 10, 13, 21],
        "13#9":    [0, 4, 7, 10, 15, 21],
        "m13#9":   [0, 3, 7, 10, 15, 21],
        "13#11":   [0, 4, 7, 10, 18, 21],
        "m13#11":  [0, 3, 7, 10, 18, 21],
        "13b9#11": [0, 4, 7, 10, 13, 18, 21],
        "m13b9#11":[0, 3, 7, 10, 13, 18, 21],
        "13b9b13": [0, 4, 7, 10, 13, 20, 21],
        "m13b9b13":[0, 3, 7, 10, 13, 20, 21],
        "713":     [0, 4, 7, 10, 14, 17, 21],
        "m713":    [0, 3, 7, 10, 14, 17, 21],
        "maj711":  [0, 4, 7, 11, 14, 17],
        "mMaj711": [0, 3, 7, 11, 14, 17],
        "m7b5113":  [0, 3, 6, 10, 14, 21],
        "m7b513":   [0, 3, 6, 10, 14, 21],
        "7b513":    [0, 4, 6, 10, 14, 21],
        "7b5113":   [0, 4, 6, 10, 14, 21],
        "m7b511":  [0, 3, 6, 10, 14],
        "m7b13":   [0, 3, 7, 10, 20],
        "7b13":    [0, 4, 7, 10, 20],
        "m7b11":   [0, 3, 7, 10, 17],
        "7b11":    [0, 4, 7, 10, 17],
        "m7#11":   [0, 3, 7, 10, 18],
        "7#11":    [0, 4, 7, 10, 18],
        "m7b513#11":[0, 3, 6, 10, 18, 21],
        "7b513#11": [0, 4, 6, 10, 18, 21],
        "7b5113#11":[0, 4, 6, 10, 18, 21],
        "m7b5113#11":[0, 3, 6,  10, 18, 21],
    }

    def __parse_chord(self, chord) -> tuple[str, str, str | None]:
        
        if "/" in chord:
            chord, bass = chord.split("/")
        else:
            bass = None

        # Extract root (letter + optional #/b)
        if len(chord) > 1 and chord[1] in "#b":
            root = chord[:2]
            quality = chord[2:]
        else:
            root = chord[0]
            quality = chord[1:]

        return root, quality, bass
    
    def chord_to_notes(self, chord) -> list[str]:
        root, quality, bass = self.__parse_chord(chord)

        if quality not in self.CHORD_FORMULAS:
            raise ValueError(f"Unknown chord quality: {quality}")

        root_val = self.NOTE_TO_INT[root]
        intervals = self.CHORD_FORMULAS[quality]

        # Build chord notes (pitch classes)
        notes = [(root_val + i) % 12 for i in intervals]

        # If no slash bass, return normally
        if not bass:
            return [self.INT_TO_NOTE[n] for n in notes]

        # Apply slash bass
        bass_val = self.NOTE_TO_INT[bass]

        # Start with bass note
        ordered = [bass_val]

        # Add other notes above the bass
        for n in notes:
            if n == bass_val:
                continue
            while n < bass_val:
                n += 12
            ordered.append(n)

        # Convert back to note names
        return [self.INT_TO_NOTE[n % 12] for n in ordered]

if __name__ == "__main__":
    
    chord_lib = ChordLibrary()
    print(chord_lib.chord_to_notes("C/E"))  
    print(chord_lib.chord_to_notes("F#dim7/Eb"))