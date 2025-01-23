import tkinter as tk
import app_globals as app
import serialization

from text_viewer import TextViewer
from file_readers import read_file
from window import Window



def create_window(text: str, filename: str):
    root = tk.Tk()
    app_viewer = TextViewer(root, text, filename)
    root.mainloop()


### MAIN
if __name__ == "__main__":
    app.print_info("\n\n\n")
    app.print_blue("==== LECTOR HORITZONTAL, per Lucho Suaya ====")

    #filepath = app.get_test_file("reader_test.pdf")
    #filepath = app.get_test_file("reader_test.epub")
    app.print_info("Root Dir: " + app.ROOT_DIR)
    app.print_info("Settings file: " + app.SETTINGS_FILEPATH)
    app.print_info("Test data folder: " + app.TEST_DATA_FILEPATH)

    # Load app
    app.print_blue("Loading App...")
    serialization.load()

    # Create app window
    root = tk.Tk()
    window = Window(root, f"Lector Horitzontal")
    app.load_fonts()
    
    # Load test file
    filepath = app.get_test_file("reader_test.docx")
    if not app.file_exists(filepath):
        app.print_error(f"No file found at: {filepath}")
        exit(1)

    file: str = read_file(filepath)
    name: str = app.get_filename(filepath)
    window.update_title(f"Lector Horitzontal -  {name}")

    # Create TextViewer & enter loop
    app_viewer = TextViewer(window, file)
    root.mainloop()
