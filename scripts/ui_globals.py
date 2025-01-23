import tkinter as tk
from tkinter import ttk



def create_button(parent: tk.Widget, text: str, callback = None, takefocus = False, padx = 5, side = tk.LEFT, **kwargs) -> ttk.Button:
    button = ttk.Button(parent, text=text, command=callback, takefocus=takefocus, **kwargs)
    button.pack(side=side, padx=padx)
    return button


def bind_button_events(button: ttk.Button, pressed_callback = None, release_callback = None):
    button.bind('<ButtonPress-1>', pressed_callback)
    button.bind('<ButtonRelease-1>', release_callback)


def create_dropdown(parent: tk.Widget, values: list, initial_value: str, width: int, callback = None, padx = 5, side = tk.LEFT) -> tuple[ttk.Combobox, tk.StringVar]:
    dropdown_var = tk.StringVar(value=initial_value)
    dropdown = ttk.Combobox(parent, textvariable=dropdown_var, values=values, state='readonly', width=width)
    dropdown.pack(side=side, padx=padx)

    if callback:
        dropdown.bind('<<ComboboxSelected>>', callback)
    
    return dropdown_var


def create_slider(parent: tk.Widget, from_: float, to: float, initial_value: float, callback = None, length = 100, side = tk.LEFT) -> ttk.Scale:
    slider = ttk.Scale(parent, from_=from_, to=to, value=initial_value, orient='horizontal', length=length)
    slider.pack(side=side)
    if callback:
        slider.configure(command=callback)
    
    return slider


def create_label(parent: tk.Widget, text: str, padx = 5, side = tk.LEFT, **kwargs) -> tk.Label:
    label = tk.Label(parent, text=text, bg='#E0E0E0', **kwargs)
    label.pack(side=side, padx=padx)
    return label


def create_textarea(parent: tk.Widget, height: int, width: int, xscroll_callback) -> tk.Text:
    text_area = tk.Text(parent, wrap='none', height=height, width=width, bg='#E0E0E0', fg='black', xscrollcommand=xscroll_callback)
    text_area.pack(expand=True, fill='x')
    return text_area


def create_scrollbar(parent: tk.Widget, orientation:str, fill, side = tk.BOTTOM) -> tk.Scrollbar:
    scrollbar = tk.Scrollbar(parent, orient=orientation)
    scrollbar.pack(side=side, fill=fill)
    return scrollbar
