import os
import json
import serialization
import app_globals as app
import ui_globals as ui
import tkinter as tk

from tkinter import ttk, font
from file_readers import read_file








class TextViewer:
    def __init__(self, root, text: str, filename: str):
        # Load settings before creating UI elements
        self.load_settings()

        # Set initial variables for the root window and text
        self.root = root
        self.root.title(f"Lector Horitzontal - {filename}")
        self.root.configure(bg='#E0E0E0')
        self.root.minsize(930, 600)
        self.root.geometry("930x600")
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}")
        
        self.fonts = sorted(list(font.families()))
        self.sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 48, 72, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500]
        self.is_scrolling = False

        # Create top frame for dropdowns and button
        self.top_frame = tk.Frame(root, bg='#E0E0E0')
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create font dropdown
        self.font_dropdown, self.font_var = ui.create_dropdown(self.top_frame, self.fonts, self.current_font, 35, self.change_font, (0, 10))

        # Create size dropdown
        self.size_dropdown, self.size_var = ui.create_dropdown(self.top_frame, self.sizes, str(self.font_size), 10, self.change_font)
        
        # Create left frame for dropdowns
        self.left_frame = tk.Frame(self.top_frame, bg='#E0E0E0')
        self.left_frame.pack(side=tk.LEFT)

        # Add reset button to the right of the speed controls
        self.reset_button = ui.create_button(self.left_frame, "Reinicia Valors", self.reset_settings, False, (10, 0))
        self.root.bind('<Configure>', self.on_window_configure)
        
        # Create speed slider
        ui.create_label(self.left_frame, "Velocitat: ", (10, 2))
        self.speed_slider = ui.create_slider(self.left_frame, 1, 50, self.scroll_amount, self.update_scroll_speed)
        
        # Add label to show current speed value
        self.scroll_label = ui.create_label(self.left_frame, str(self.scroll_amount)+"%")
        #width=4

        # Create center frame for button
        self.center_frame = tk.Frame(self.top_frame, bg='#E0E0E0')
        self.center_frame.pack(expand=True)

        # Add file open button
        self.open_button = ui.create_button(self.center_frame, "Obrir Arxiu", self.open_new_document)
        
        # Create scroll button
        self.is_scrolling = False
        self.scroll_left_button = ui.create_button(self.center_frame, "← Mou")
        self.scroll_right_button = ui.create_button(self.center_frame, "Mou →")

        # Bind button press and release events
        ui.bind_button_events(self.scroll_left_button, lambda e: self.start_scrolling(e, False), self.stop_scrolling)
        ui.bind_button_events(self.scroll_right_button, lambda e: self.start_scrolling(e, True), self.stop_scrolling)

        # Create a frame to hold the text
        self.frame = tk.Frame(root, bg='#E0E0E0')
        self.frame.pack(expand=True, fill='both')
        
        # Create horizontal scrollbar
        self.scrollbar = ui.create_scrollbar(self.frame, 'horizontal', tk.X)
        
        # Store text for font changes
        self.text = text

        # Configure text widget
        self.text_area = ui.create_textarea(self.frame, 1, 1000, ('Calibri', 75), self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.xview)
        
        # Insert text and disable editing
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state='disabled')
        
        # Bind spacebar
        self.root.bind('<space>', lambda e: self.scroll_text(e, True))
        self.root.bind('<Control_L>', lambda e: self.scroll_text(e, False))

        # Bind all other keys to do nothing
        self.root.bind('<Key>', self.block_key)

        # Focus the text area
        self.text_area.focus_set()

        # Set values
        self.update_scroll_speed(self.scroll_amount)
        self.change_font(None)


    def change_font(self, event):
        # Get selected font
        new_font = self.font_var.get()
        new_size = int(self.size_var.get())
        
        # Enable text widget temporarily
        self.text_area.configure(state='normal')
        
        # Update font
        self.text_area.configure(font=(new_font, new_size))
        
        # Clear and reinsert text
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.text)
        
        # Disable text widget again
        self.text_area.configure(state='disabled')
        self.save_settings()
    

    def update_scroll_speed(self, value):
        self.scroll_amount = float(value)/float(100000)
        self.scroll_label.config(text=f"{int(float(value))}%")
        self.save_settings()

    
    def start_scrolling(self, event, scroll_right):
        self.stop_scrolling(None)
        self.is_scrolling = True
        self.continuous_scroll(scroll_right)
    
    def stop_scrolling(self, event):
        self.is_scrolling = False
        self.text_area.focus_set()
    
    def continuous_scroll(self, scroll_right):
        if self.is_scrolling:
            self.scroll_text(None, scroll_right)
            self.root.after(50, lambda: self.continuous_scroll(scroll_right))

    def scroll_text(self, event, scroll_right):
        current_pos = float(self.text_area.xview()[0])
        speed = self.scroll_amount if scroll_right else -self.scroll_amount
        new_pos = min(1.0, current_pos + speed)  # Ensure we don't scroll past the end
        self.text_area.xview_moveto(new_pos)
        return "break"
    
    def block_key(self, event):
        if event.keysym != 'space':
            return "break"
    

    def reset_settings(self):
        # Use global DEFAULT_SETTINGS
        self.font_var.set(app.DEFAULT_SETTINGS['font'])
        self.size_var.set(str(app.DEFAULT_SETTINGS['font_size']))
        self.speed_slider.set(app.DEFAULT_SETTINGS['speed'])
        
        self.change_font(None)
        self.update_scroll_speed(app.DEFAULT_SETTINGS['speed'])

    def on_window_configure(self, event):
        # Only save if it's a real window change (not during initialization)
        if event.widget == self.root and self.root.winfo_viewable():
            self.window_width = self.root.winfo_width()
            self.window_height = self.root.winfo_height()
            self.window_x = self.root.winfo_x()
            self.window_y = self.root.winfo_y()
            self.save_settings()
    

    def save_settings(self):
        serialization.set_setting('font', self.font_var.get())
        serialization.set_setting('font_size', int(self.size_var.get()))
        serialization.set_setting('speed', int(float(self.speed_slider.get())))
        serialization.set_setting('win_w', self.window_width)
        serialization.set_setting('win_h', self.window_height)
        serialization.set_setting('win_x', self.window_x)
        serialization.set_setting('win_y', self.window_y)

        serialization.save()
    
    def load_settings(self):
        serialization.load()
        
        # Store values to be used in UI initialization
        self.current_font = serialization.get_setting('font')
        self.font_size = serialization.get_setting('font_size')
        self.scroll_amount = serialization.get_setting('speed')
        self.window_width = serialization.get_setting('window_width')
        self.window_height = serialization.get_setting('window_height')
        self.window_x = serialization.get_setting('window_x')
        self.window_y = serialization.get_setting('window_y')
        print("Settings used: [",
              f"Font: {self.current_font} |",
              f"Font Size: {self.font_size} |",
              f"Speed: {self.scroll_amount} |",
              f"Window: {self.window_width}x{self.window_height} @({self.window_x},{self.window_y})",
              "]")
    
    def open_new_document(self):
        document_path: str = app.open_file_dialog()
        if not document_path:
            return
        
        try:
            # Read new file
            new_text = read_file(document_path)

            self.text = new_text
            self.text_area.configure(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_text)
            self.text_area.configure(state='disabled')

            # Reset scroll position
            self.text_area.xview_moveto(0)
            
            # Update window title with filename
            self.root.title(f"Lector Horitzontal - {app.get_filename(document_path)}")
        except Exception as e:
            print(f"Error loading file: {e}")
