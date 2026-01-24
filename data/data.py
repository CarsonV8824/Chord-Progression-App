import markovify
import zipfile

def read_file_lines(zip_path):
    """Generator that yields one line at a time from a file inside a zip."""
    with zipfile.ZipFile(zip_path, "r") as z:
        txt_name = z.namelist()[0]
        with z.open(txt_name) as f:
            for num, line in enumerate(f):
                yield line.decode('utf-8')
                if num >= 100000:
                    break

def make_chord_progression(file_path: str, length_of_prog: int = 2) -> str:
    """Return a chord progression generated using a Markov model."""
    lines = "\n".join(read_file_lines(file_path))
    lines = lines.lstrip()

    text_model = markovify.NewlineText(lines)
    final = text_model.make_short_sentence(min_chars=50, max_chars=100)

    while final is None:
        final = text_model.make_short_sentence(min_chars=50, max_chars=100)

    test = final.split(" ")
    while len(test) < length_of_prog:
        final = text_model.make_short_sentence(min_chars=50, max_chars=100)
        test = final.split(" ")

    final = final.split(" ")[:length_of_prog]
    return " ".join(final)