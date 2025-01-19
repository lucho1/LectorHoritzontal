import tkinter as tk

from text_viewer import TextViewer
from file_readers import read_file, get_filename



def create_window(text: str, filename: str):
    root = tk.Tk()
    app = TextViewer(root, text, filename)
    root.mainloop()



# MAIN
if __name__ == "__main__":
    print("\n\n\n")
    print("==== LECTOR HORITZONTAL, per Lucho Suaya ====")

    #filepath = "D:/Repos/LectorHoritzontal/reader_test.epub"
    #filepath = "D:/Repos/LectorHoritzontal/reader_test.pdf"
    filepath = "D:/Repos/LectorHoritzontal/reader_test.docx"

    file: str = read_file(filepath)
    name: str = get_filename(filepath)
    create_window(file, name)
    