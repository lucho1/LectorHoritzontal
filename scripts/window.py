import tkinter as tk
import serialization

from app_controller import AppController



class Window:
    def __init__(self, root: tk.Tk, controller: AppController, title: str):
        # Set variables
        self.controller: AppController = controller
        self.width: float = 0.0
        self.height: float = 0.0
        self.x: float = 0.0
        self.y: float = 0.0
        self.scroll_callback = None

        # Set the root window
        self.root: tk.Tk = root
        self.root.title(title)
        self.root.configure(bg='#E0E0E0')

        # Load settings and configure window
        self._load_settings()
        self.root.minsize(930, 600)
        self.root.geometry("930x600")
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

        # Bind window events and keys
        self.root.bind('<Configure>', self._on_window_configure)
        self.root.bind('<space>', self._on_space_pressed)
        self.root.bind('<Control_L>', self._on_left_ctrl_pressed)
        self.root.bind('<Key>', self._on_key_pressed)
    
    
    ### Public functions
    def set_scroll_callback(self, callback):
        self.scroll_callback = callback
    
    def set_title(self, new_title: str):
        self.root.title(new_title)

    def get_root(self) -> tk.Tk:
        return self.root
    
    
    ### Key bindings & Event callbacks
    def _on_space_pressed(self, _):
        new_pos: float = self.controller.scroll(True)
        
        if self.scroll_callback:
            self.scroll_callback(new_pos)
        
        return "break"
    

    def _on_left_ctrl_pressed(self, _):
        new_pos: float = self.controller.scroll(False)
        
        if self.scroll_callback:
            self.scroll_callback(new_pos)
        
        return "break"
    
    
    def _on_key_pressed(self, event):
        if event.keysym != 'space' and event.keysym != 'Control_L':
            return "break"
    
    
    def _on_window_configure(self, event):
        if event.widget == self.root and self.root.winfo_viewable():
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            self.x = self.root.winfo_x()
            self.y = self.root.winfo_y()
            self._save_settings()
    

    ### Serialization
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

        print("Window settings:", f"Size({self.width}x{self.height})", f"Position({self.x},{self.y})")
