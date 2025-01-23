import serialization
import app_globals as app
import ui_globals as ui
import tkinter as tk

from file_readers import read_file
from window import Window



class TextViewer:
    def __init__(self, window: Window, text: str):
        # Load settings before creating UI elements
        self.load_settings()

        # Store window
        self.window = window

        # Store text for font changes
        self.text = text
        
        # Set is scrolling
        self.is_scrolling = False

        # Set UI and key bindings
        self._create_ui()
        self._set_key_bindings()

        # Set initial values
        self.update_scroll_speed(self.scroll_amount)
        self.change_font(None)
    

    def _create_ui(self):
        self._create_frames()
        self._create_font_controls()
        self._create_speed_controls()
        self._create_action_buttons()
        self._create_text_area()
    

    def _create_frames(self):
        # Top frame to hold other frames, Left frame for controls, Center frame for buttons
        top_frame = ui.create_frame(self.window.get_root(), fill=tk.X, padx=5, pady=5)
        self.left_frame = ui.create_frame(top_frame, side=tk.LEFT)
        self.center_frame = ui.create_frame(top_frame, expand=True)

        # Frame to hold the text
        self.frame = ui.create_frame(self.window.get_root(), fill='both', expand=True)
    
    
    def _create_font_controls(self):
        # Font dropdown
        self.font_var = ui.create_dropdown(
            self.left_frame, app.FONTS, self.current_font, self.change_font, padx=(5, 5), width=30)
        
        # Size dropdown
        self.size_var = ui.create_dropdown(
            self.left_frame, app.FONT_SIZES, str(self.font_size), self.change_font, padx=(0, 5))
    

    def _create_speed_controls(self):
        # Speed slider
        ui.create_label(self.left_frame, "Velocitat: ", padx=(10, 2))
        self.speed_slider = ui.create_slider(self.left_frame, 1, 50, self.scroll_amount, self.update_scroll_speed)
        self.scroll_label = ui.create_label(self.left_frame, str(self.scroll_amount)+"%")
    
    def _create_action_buttons(self):
        # Reset button
        ui.create_button(self.left_frame, "Reinicia Valors", self.reset_settings, takefocus=False, padx=(10, 0))

        # Open file button
        ui.create_button(self.center_frame, "Obrir Arxiu", self.open_new_document)

        # Scroll buttons
        scroll_left_button = ui.create_button(self.center_frame, "← Mou")
        scroll_right_button = ui.create_button(self.center_frame, "Mou →")

        # Bind scroll buttons' press & release events
        ui.bind_button_events(scroll_left_button, lambda e: self.start_scrolling(e, False), self.stop_scrolling)
        ui.bind_button_events(scroll_right_button, lambda e: self.start_scrolling(e, True), self.stop_scrolling)
    

    def _create_text_area(self):
        # Horizontal scrollbar
        scrollbar = ui.create_scrollbar(self.frame, 'horizontal', fill=tk.X)

        # Text widget
        self.text_area = ui.create_textarea(self.frame, scrollbar.set, height=1, width=1000)
        scrollbar.config(command=self.text_area.xview)

        # Insert text and disable editing
        self.text_area.insert(tk.END, self.text)
        self.text_area.configure(state='disabled')

        # Focus the text area
        self.text_area.focus_set()
    

    def _set_key_bindings(self):
        root = self.window.get_root()

        # Bind spacebar & LCtrl
        root.bind('<space>', lambda e: self.scroll_text(e, True))
        root.bind('<Control_L>', lambda e: self.scroll_text(e, False))

        # Bind all other keys to do nothing
        root.bind('<Key>', self.block_key)


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
            self.window.get_root().after(50, lambda: self.continuous_scroll(scroll_right))

    def scroll_text(self, event, scroll_right):
        current_pos = float(self.text_area.xview()[0])
        speed = self.scroll_amount if scroll_right else -self.scroll_amount
        new_pos = min(1.0, current_pos + speed)
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
    

    def save_settings(self):
        serialization.set_setting('font', self.font_var.get())
        serialization.set_setting('font_size', int(self.size_var.get()))
        serialization.set_setting('speed', int(float(self.speed_slider.get())))
        serialization.save()
    

    def load_settings(self):
        self.current_font = serialization.get_setting('font')
        self.font_size = serialization.get_setting('font_size')
        self.scroll_amount = serialization.get_setting('speed')
        print("TextViewer loaded settings: [",
              f"Font: {self.current_font} |",
              f"Font Size: {self.font_size} |",
              f"Speed: {self.scroll_amount} ]")
    

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
            self.window.update_title(f"Lector Horitzontal - {app.get_filename(document_path)}")
        except Exception as e:
            print(f"Error loading file: {e}")
