import app_globals as app
import ui_globals as ui
import tkinter as tk

from tkinter import ttk
from window import Window
from app_controller import AppController



class AppUI:
    def __init__(self, window: Window, controller: AppController):
        # Set variables
        self.root = window.get_root()
        self.controller = controller
        self.text = ""
        self.text_area: tk.Text = None
        self.is_scrolling = False

        # Top frame to hold other frames, Left frame for controls
        top_frame: tk.Frame = ui.create_frame(self.root, fill=tk.X, padx=5, pady=5)
        left_frame: tk.Frame = ui.create_frame(top_frame, side=tk.LEFT)

        # Font Dropdowns
        font, fsize = self.controller.get_current_font()
        font_var: tk.StringVar = ui.create_dropdown(
            left_frame, app.FONTS, font, self._on_font_changed, padx=(5, 5), width=30)
        
        fsize_var: tk.StringVar = ui.create_dropdown(
            left_frame, app.FONT_SIZES, str(fsize), self._on_font_size_changed, padx=(0, 5))
        
        # Speed slider
        ui.create_label(left_frame, "Velocitat: ", padx=(10, 2))

        current_speed: float = self.controller.get_scroll_speed()
        scroll_label: tk.Label = ui.create_label(left_frame, f"{current_speed:.1f}%")
        speed_slider: ttk.Scale = ui.create_slider(left_frame, 1, 50, current_speed, lambda value: self._on_scroll_speed_changed(value, scroll_label))

        # Restart button
        ui.create_button(left_frame, "Reinicia Valors", lambda: self._reset_settings(font_var, fsize_var, speed_slider, scroll_label),
                          takefocus=False, padx=(10, 0))

        # Other UI elements
        center_frame: tk.Frame = ui.create_frame(top_frame, expand=True)
        text_frame: tk.Frame = ui.create_frame(self.root, fill='both', expand=True)

        self._create_action_buttons(center_frame)
        self._create_text_area(text_frame)
        
        # Set input Key bindings
        self.root.bind('<space>', lambda _: self._scroll(True))
        self.root.bind('<Control_L>', lambda _: self._scroll(False))
        self.root.bind('<Key>', self._on_key_pressed)
    
    
    ### UI Elements Callbacks
    def _on_font_size_changed(self, event: app.TkEvent):
        new_size: int = int(event.widget.get())
        new_font: app.FontTuple = self.controller.on_font_size_changed(new_size)
        self.text_area.configure(font=new_font)

    
    def _on_font_changed(self, event: app.TkEvent):
        new_font: str = str(event.widget.get())
        changed_font: app.FontTuple = self.controller.on_font_changed(new_font)
        self.text_area.configure(font=changed_font)

    
    def _on_scroll_speed_changed(self, value: str, scroll_label: tk.Label):
        speed: float = float(value)
        self.controller.on_scroll_speed_changed(speed)
        scroll_label.config(text=f"{speed:.1f}%")

    
    def _start_scrolling(self, scroll_right: bool):
        self._stop_scrolling()
        self.is_scrolling = True
        self._continuous_scroll(scroll_right)
    
    
    def _stop_scrolling(self):
        self.is_scrolling = False
        self.text_area.focus_set()
    

    def _continuous_scroll(self, scroll_right: bool):
        if not self.is_scrolling:
            return
        
        # Scroll and call _continuous_scroll() again after a while
        self._scroll(scroll_right)
        self.root.after(25, lambda: self._continuous_scroll(scroll_right))
    
    
    def _scroll(self, scroll_right: bool):
        new_scrolled_pos: float = self.controller.scroll(scroll_right)
        self.text_area.xview_moveto(new_scrolled_pos)
        return "break"

    
    def _reset_settings(self, font_var: tk.StringVar, size_var: tk.StringVar, speed_slider: ttk.Scale, speed_label: tk.Label):
        # Reset settings and get their new values
        self.controller.reset_settings()

        font, size = self.controller.get_current_font()
        new_speed: float = self.controller.get_scroll_speed()

        # Configure UI elements according to new settings
        self.text_area.configure(font=(font, size))
        font_var.set(font)
        size_var.set(size)
        speed_slider.set(new_speed)
        speed_label.config(text=f"{new_speed:.1f}%")

    
    def _open_new_file(self):
        new_text: str = self.controller.open_new_file()
        self.display_new_text(new_text)
    

    # TODO: Probably temp. function, only used in main and in _open_new_file()
    def display_new_text(self, new_text: str):
        # Replace text in text area and move to scroll 0
        self.text_area.configure(state='normal')
        self.text_area.replace(1.0, tk.END, new_text)
        self.text_area.configure(state='disabled')
        self.text_area.xview_moveto(0.0)
    
    
    def _on_key_pressed(self, event: app.TkEvent):
        # Block event propagation for all keys that are not space and LCtrl
        if event.keysym != 'space' and event.keysym != 'Control_L':
            return "break"


    
    ### UI Elements Creation Buttons
    def _create_action_buttons(self, parent_frame: tk.Frame):
        # Open file button
        ui.create_button(parent_frame, "Obrir Arxiu", self._open_new_file)

        # Scroll buttons
        scroll_left_button = ui.create_button(parent_frame, "← Mou")
        scroll_right_button = ui.create_button(parent_frame, "Mou →")

        # Bind scroll buttons' press & release events
        ui.bind_button_events(scroll_left_button, lambda _: self._start_scrolling(False), lambda _: self._stop_scrolling())
        ui.bind_button_events(scroll_right_button, lambda _: self._start_scrolling(True), lambda _: self._stop_scrolling())
    

    def _create_text_area(self, parent_frame: tk.Frame):
        # Horizontal scrollbar
        scrollbar = ui.create_scrollbar(parent_frame, 'horizontal', fill=tk.X)

        # Text widget
        self.text_area = ui.create_textarea(parent_frame, scrollbar.set, height=1, width=1000)
        scrollbar.config(command=self.text_area.xview)

        # Insert text and disable editing
        self.text_area.configure(state='disabled', font=self.controller.get_current_font())

        # Focus the text area
        self.text_area.focus_set()
