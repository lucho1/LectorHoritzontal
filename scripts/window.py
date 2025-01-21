import tkinter as tk
import serialization
import app_globals as app



class Window:
    def __init__(self, root: tk.Tk, title: str):
        # Set the root window
        self.root = root
        self.root.title(title)
        self.root.configure(bg='#E0E0E0')

        # Load settings and configure window
        self._load_settings()
        self.root.minsize(930, 600)
        self.root.geometry("930x600")
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        # Bind window events
        self.root.bind('<Configure>', self._on_window_configure)
    
    
    def update_title(self, new_title: str):
        self.root.title(new_title)
    

    def get_root(self) -> tk.Tk:
        return self.root
    
    
    def _on_window_configure(self, event):
        if event.widget == self.root and self.root.winfo_viewable():
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            self.x = self.root.winfo_x()
            self.y = self.root.winfo_y()
            self._save_settings()
    

    def _save_settings(self):
        serialization.set_setting('win_w', self.width)
        serialization.set_setting('win_h', self.height)
        serialization.set_setting('win_x', self.x)
        serialization.set_setting('win_y', self.y)
        serialization.save()
    
    
    def _load_settings(self):
        self.width = serialization.get_setting('win_w')
        self.height = serialization.get_setting('win_h')
        self.x = serialization.get_setting('win_x')
        self.y = serialization.get_setting('win_y')

        print("Window settings:", f"Size: {self.width}x{self.height}", f"Position: ({self.x},{self.y})")
