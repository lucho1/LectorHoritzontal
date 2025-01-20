import tkinter as tk
import app_globals as app

from text_viewer import TextViewer
from file_readers import read_file



def create_window(text: str, filename: str):
    root = tk.Tk()
    app_viewer = TextViewer(root, text, filename)
    root.mainloop()


### MAIN
if __name__ == "__main__":
    app.print_info("\n\n\n")
    app.print_blue("==== LECTOR HORITZONTAL, per Lucho Suaya ====")

    #filepath = "D:/Repos/LectorHoritzontal/data/test/reader_test.epub"
    #filepath = "D:/Repos/LectorHoritzontal/data/test/reader_test.pdf"
    filepath = "D:/Repos/LectorHoritzontal/data/test/reader_test.docx"
    if not app.file_exists(filepath):
        app.print_error(f"No file found at: {filepath}")
        exit(1)

    file: str = read_file(filepath)
    name: str = app.get_filename(filepath)
    create_window(file, name)
