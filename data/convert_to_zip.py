import zipfile

def convert_txt_to_zip(txt_file_path, zip_file_path):
    with open(txt_file_path, 'r') as txt_file:
        lines = txt_file.readlines()

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('complex_chords.txt', ''.join(lines))

if __name__ == "__main__":
    convert_txt_to_zip('data/complex_chords.txt', 'data/complex_chords.zip')