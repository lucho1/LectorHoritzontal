import tkinter as tk
from tkinter import ttk, colorchooser


### Style
def configure_ttk_style(bg_color: str):
    style = ttk.Style()
    style.theme_use('vista') # TODO: Probably unavailable outside Windows

    style.configure('TButton', background=bg_color, borderwidth=0, relief='flat', padding=(10, 5))
    style.configure('TCombobox', borderwidth=0, relief='flat', arrowsize=12)
    style.configure('TScale', background=bg_color, borderwidth=0, relief='flat', troughcolor='#CCCCCC')
    
    style.map('TButton',
        background=[('active', '#CCCCCC')],
        highlightcolor=[('focus', bg_color)],
        relief=[('pressed', 'flat')],
        borderwidth=[('active', 0)])



### UI Basics (Frames and Text)
def create_frame(parent: tk.Widget, fill = None, expand = False, side = None, padx = 0, pady = 0) -> tk.Frame:
    frame = tk.Frame(parent, bg=parent.cget('bg'), borderwidth=0, relief='flat')
    frame.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
    return frame


def create_label(parent: tk.Widget, text: str, padx = 5, **kwargs) -> tk.Label:
    label = tk.Label(parent, text=text, bg=parent.cget('bg'), borderwidth=0, **kwargs)
    label.pack(side=tk.LEFT, padx=padx)
    return label


def create_textarea(parent: tk.Widget, xscroll_callback, height: int, width: int) -> tk.Text:
    text_area = tk.Text(parent, wrap='none', height=height, width=width, xscrollcommand=xscroll_callback, borderwidth=0, relief='flat', padx=10, pady=10)
    text_area.pack(expand=True, fill='x')
    return text_area



### Buttons
def create_button(parent: tk.Widget, text: str, callback = None, padx = 5, **kwargs) -> ttk.Button:
    button = ttk.Button(parent, style='TButton', text=text, command=callback, takefocus=False, **kwargs)
    button.pack(side=tk.LEFT, padx=padx)
    return button


def bind_button_events(button: ttk.Button, pressed_callback = None, release_callback = None):
    button.bind('<ButtonPress-1>', pressed_callback)
    button.bind('<ButtonRelease-1>', release_callback)



### Other UI Elements
def create_slider(parent: tk.Widget, from_: float, to: float, initial_value: float, callback = None) -> ttk.Scale:
    slider = ttk.Scale(parent, style='TScale', orient='horizontal', length=100, from_=from_, to=to, value=initial_value)
    slider.pack(side=tk.LEFT)
    if callback:
        slider.configure(command=callback)
    
    return slider


def create_scrollbar(parent: tk.Widget, orientation:str, fill) -> tk.Scrollbar:
    scrollbar = tk.Scrollbar(parent, orient=orientation, borderwidth=0, relief='flat')
    scrollbar.pack(side=tk.BOTTOM, fill=fill)
    return scrollbar


def create_dropdown(parent: tk.Widget, values: list, initial_value: str, callback = None, padx = 5, width: int = 10) -> tk.StringVar:
    dropdown_var = tk.StringVar(value=initial_value)
    dropdown = ttk.Combobox(parent, style='TCombobox', state='readonly', textvariable=dropdown_var, values=values, width=width)
    dropdown.pack(side=tk.LEFT, padx=padx)

    if callback:
        dropdown.bind('<<ComboboxSelected>>', callback)
    
    return dropdown_var


def create_color_picker(parent: tk.Widget, initial_color: str, target_widget: tk.Widget, callback, label: str = "", padx = 5) -> tk.Button:
    frame = create_frame(parent, side=tk.LEFT, padx=padx)
    if label:
        create_label(frame, label, padx=2)
    
    color_button = tk.Button(frame, width=3, bg=initial_color, borderwidth=1, relief='solid')
    color_button.pack(side=tk.LEFT, pady=2)

    def pick_color():
        result = colorchooser.askcolor()
        if result and result[1]:
            color = result[1]
            color_button.configure(bg=color)
            callback(color, target_widget)
    
    color_button.configure(command=pick_color)
    return color_button
