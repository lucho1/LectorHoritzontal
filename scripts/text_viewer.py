import os
import json
import app_globals as app
import tkinter as tk

from tkinter import filedialog, ttk, font
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
        self.font_var = tk.StringVar(value=self.current_font)
        self.font_dropdown = ttk.Combobox(self.top_frame,
                                        textvariable=self.font_var,
                                        values=self.fonts,
                                        state='readonly',
                                        width=35)
        
        self.font_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.font_dropdown.bind('<<ComboboxSelected>>', self.change_font)

        # Create size dropdown
        self.size_var = tk.StringVar(value=str(self.font_size))
        self.size_dropdown = ttk.Combobox(self.top_frame,
                                        textvariable=self.size_var,
                                        values=self.sizes,
                                        state='readonly',
                                        width=10)
        self.size_dropdown.pack(side=tk.LEFT)
        self.size_dropdown.bind('<<ComboboxSelected>>', self.change_font)
        
        # Create left frame for dropdowns
        self.left_frame = tk.Frame(self.top_frame, bg='#E0E0E0')
        self.left_frame.pack(side=tk.LEFT)

        # Add reset button to the right of the speed controls
        self.reset_button = ttk.Button(self.left_frame, 
                                     text="Reinicia Valors", 
                                     command=self.reset_settings,
                                     takefocus=False)
        self.reset_button.pack(side=tk.LEFT, padx=(10, 0))
        self.root.bind('<Configure>', self.on_window_configure)
        
         # Create speed slider
        tk.Label(self.left_frame, text="Velocitat: ", bg='#E0E0E0').pack(side=tk.LEFT, padx=(10, 2))
        self.speed_slider = ttk.Scale(self.left_frame, 
                                    from_=1,        # Fastest
                                    to=50,         # Slowest
                                    value=self.scroll_amount, # Default value
                                    orient='horizontal',
                                    length=100,     # Slider width in pixels
                                    command=self.update_scroll_speed)
        self.speed_slider.pack(side=tk.LEFT)
        
        # Add label to show current speed value
        self.scroll_label = tk.Label(self.left_frame, 
                                  text=str(self.scroll_amount)+"%", 
                                  bg='#E0E0E0',
                                  width=4)
        self.scroll_label.pack(side=tk.LEFT)
        


        # Create center frame for button
        self.center_frame = tk.Frame(self.top_frame, bg='#E0E0E0')
        self.center_frame.pack(expand=True)
        
        # Create scroll button
        self.is_scrolling = False
        
        # Add file open button
        self.open_button = ttk.Button(self.center_frame, 
                                    text="Obrir Arxiu", 
                                    command=self.open_file,
                                    takefocus=False)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.scroll_left_button = ttk.Button(self.center_frame, text="← Mou", takefocus=False)
        self.scroll_left_button.pack(side=tk.LEFT, padx=5)
        
        self.scroll_right_button  = ttk.Button(self.center_frame, text="Mou →", takefocus=False)
        self.scroll_right_button.pack(side=tk.LEFT, padx=5)        

        # Bind button press and release events
        self.scroll_left_button.bind('<ButtonPress-1>', lambda e: self.start_scrolling(e, False))
        self.scroll_left_button.bind('<ButtonRelease-1>', self.stop_scrolling)
        self.scroll_right_button.bind('<ButtonPress-1>', lambda e: self.start_scrolling(e, True))
        self.scroll_right_button.bind('<ButtonRelease-1>', self.stop_scrolling)


        # Create a frame to hold the text
        self.frame = tk.Frame(root, bg='#E0E0E0')
        self.frame.pack(expand=True, fill='both')
        
        # Create horizontal scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient='horizontal')
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure text widget
        self.text_area = tk.Text(self.frame, 
                                wrap='none',
                                height=1,
                                width = 1000,
                                bg='#E0E0E0', 
                                fg='black', 
                                font=('Calibri', 75),
                                xscrollcommand=self.scrollbar.set)
        
        self.text_area.pack(expand=True, fill='x')
        self.text = text  # Store text for font changes
        
        # Configure scrollbar
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
        settings = {
            'font': self.font_var.get(),
            'font_size': int(self.size_var.get()),
            'speed': int(float(self.speed_slider.get())),
            'window_width': self.window_width,
            'window_height': self.window_height,
            'window_x': self.window_x,
            'window_y': self.window_y
        }
        
        try:
            os.makedirs(os.path.dirname(app.SETTINGS_FILEPATH), exist_ok=True)
            with open(app.SETTINGS_FILEPATH, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Couldn't save settings: {e}")
    
    def load_settings(self):
        print("Loading settings...")
        settings = app.DEFAULT_SETTINGS.copy()
        
        try:
            if os.path.exists(app.SETTINGS_FILEPATH):
                print(f"Settings loaded from: {app.SETTINGS_FILEPATH}")
                with open(app.SETTINGS_FILEPATH, 'r') as f:
                    loaded_settings = json.load(f)
                    settings.update(loaded_settings)
            else:
                print(f"No settings file found at: {app.SETTINGS_FILEPATH}")
                print("Using default settings")
        except Exception as e:
            print(f"Couldn't load settings: {e}")
            print("Using default settings")
        
        # Store values to be used in UI initialization
        self.current_font = settings['font']
        self.font_size = settings['font_size']
        self.scroll_amount = settings['speed']
        self.window_width = settings['window_width']
        self.window_height = settings['window_height']
        self.window_x = settings['window_x']
        self.window_y = settings['window_y']
        print("Settings used: [",
              f"Font: {settings['font']} |",
              f"Font Size: {settings['font_size']} |",
              f"Speed: {settings['speed']} |",
              f"Window: {settings['window_width']}x{settings['window_height']} @({settings['window_x']},{settings['window_y']})",
              "]")
    
    def open_file(self):
        # Ask for file
        file_types = [
            ('All supported files', '*.epub;*.pdf;*.docx'),
            ('EPUB files', '*.epub'),
            ('PDF files', '*.pdf'),
            ('Word files', '*.docx'),
        ]
        
        filepath = filedialog.askopenfilename(
            title='Select a file to read',
            filetypes=file_types
        )
        
        if filepath:  # If a file was selected
            try:
                # Read new file
                new_text = read_file(filepath)
                
                # Update text area
                self.text = new_text
                self.text_area.configure(state='normal')
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, new_text)
                self.text_area.configure(state='disabled')
                
                # Reset scroll position
                self.text_area.xview_moveto(0)
                
                # Update window title with filename
                filename = os.path.basename(filepath)
                self.root.title(f"Lector Horitzontal - {filename}")
                
            except Exception as e:
                print(f"Error loading file: {e}")

