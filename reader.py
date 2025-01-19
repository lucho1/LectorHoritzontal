import os
import tkinter as tk

from text_viewer import TextViewer
from file_readers import read_file



def create_window(text, filename):
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

    if os.path.exists(filepath):
        print("Reading Document: " + filepath)
        file = read_file(filepath)
        create_window(file, os.path.basename(filepath))
    else:
        print(f"No document file found at: {filepath}")
    