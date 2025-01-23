import tkinter as tk
from tkinter import ttk



def create_frame(parent: tk.Widget, fill = None, expand = False, side = None, padx = 0, pady = 0) -> tk.Frame:
    frame = tk.Frame(parent, bg='#E0E0E0')
    frame.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady)
    return frame


def create_button(parent: tk.Widget, text: str, callback = None, takefocus = False, padx = 5, **kwargs) -> ttk.Button:
    button = ttk.Button(parent, text=text, command=callback, takefocus=takefocus, **kwargs)
    button.pack(side=tk.LEFT, padx=padx)
    return button


def bind_button_events(button: ttk.Button, pressed_callback = None, release_callback = None):
    button.bind('<ButtonPress-1>', pressed_callback)
    button.bind('<ButtonRelease-1>', release_callback)


def create_dropdown(parent: tk.Widget, values: list, initial_value: str, callback = None, padx = 5, width: int = 10) -> tuple[ttk.Combobox, tk.StringVar]:
    dropdown_var = tk.StringVar(value=initial_value)
    dropdown = ttk.Combobox(parent, textvariable=dropdown_var, values=values, state='readonly', width=width)
    dropdown.pack(side=tk.LEFT, padx=padx)

    if callback:
        dropdown.bind('<<ComboboxSelected>>', callback)
    
    return dropdown_var


def create_slider(parent: tk.Widget, from_: float, to: float, initial_value: float, callback = None) -> ttk.Scale:
    slider = ttk.Scale(parent, from_=from_, to=to, value=initial_value, orient='horizontal', length=100)
    slider.pack(side=tk.LEFT)
    if callback:
        slider.configure(command=callback)
    
    return slider


def create_label(parent: tk.Widget, text: str, padx = 5, **kwargs) -> tk.Label:
    label = tk.Label(parent, text=text, bg='#E0E0E0', **kwargs)
    label.pack(side=tk.LEFT, padx=padx)
    return label


def create_textarea(parent: tk.Widget, xscroll_callback, height: int, width: int) -> tk.Text:
    text_area = tk.Text(parent, wrap='none', height=height, width=width, bg='#E0E0E0', fg='black', xscrollcommand=xscroll_callback)
    text_area.pack(expand=True, fill='x')
    return text_area


def create_scrollbar(parent: tk.Widget, orientation:str, fill) -> tk.Scrollbar:
    scrollbar = tk.Scrollbar(parent, orient=orientation)
    scrollbar.pack(side=tk.BOTTOM, fill=fill)
    return scrollbar
