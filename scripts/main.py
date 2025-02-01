import tkinter as tk
import app_globals as app
import serialization

from text_manager import TextManager
from app_controller import AppController
from window import Window
from file_readers import read_file
from app_ui import AppUI



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
    text_mgr: TextManager = TextManager()
    controller: AppController = AppController(text_mgr)
    

    # Create app window
    root = tk.Tk()
    app.load_fonts()
    window = Window(root, controller, f"Lector Horitzontal")
    
    # Load test file
    filepath = app.get_test_file("reader_test.docx")
    if not app.file_exists(filepath):
        app.print_error(f"No file found at: {filepath}")
        exit(1)

    file_content: str = read_file(filepath)
    name: str = app.get_filename(filepath)
    window.set_title(f"Lector Horitzontal -  {name}")

    # Create TextViewer & enter loop
    #app_viewer = TextViewer(window, file)
    ui = AppUI(window, controller)
    ui.display_new_text(file_content)
    root.mainloop()
