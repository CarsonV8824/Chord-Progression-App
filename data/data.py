import markovify
import zipfile
import threading
from concurrent.futures import ThreadPoolExecutor

def read_file_lines(zip_path, lines_to_read:int):
    """Generator that yields one line at a time from a file inside a zip."""
    with zipfile.ZipFile(zip_path, "r") as z:
        txt_name = z.namelist()[0]
        with z.open(txt_name) as f:
            for num, line in enumerate(f):
                yield line.decode('utf-8')
                print(num)
                if num + 1 >= lines_to_read:
                    break

def make_chord_progression_from_lines(lines: str, length_of_prog: int) -> str:
    """Return a chord progression generated using a Markov model from pre-loaded lines."""
    text_model = markovify.NewlineText(lines)
    final = text_model.make_short_sentence(min_chars=10, max_chars=100)

    while final is None:
        final = text_model.make_short_sentence(min_chars=10, max_chars=100)

    test = final.split(" ")
    while len(test) < length_of_prog:
        count = 0
        while True:
            try:
                count += 1
                if count > 100:
                    break
                final = text_model.make_short_sentence(min_chars=10, max_chars=100)
                test = final.split(" ")
                break
            except Exception:
                continue    

    final = final.split(" ")[:length_of_prog]

    return " ".join(final)


def make_chord_progressions_threaded(file_path: str, length_of_prog: int, lines_to_read: int, num_progressions: int = 1, callback=None):
    """Generate multiple chord progressions in a background thread."""
    def run():
        
        lines = "\n".join(read_file_lines(file_path, lines_to_read))
        lines = lines.lstrip()
        
       
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(make_chord_progression_from_lines, lines, length_of_prog)
                for _ in range(num_progressions)
            ]
            results = [future.result() for future in futures]
        
        if callback:
            callback(results)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()