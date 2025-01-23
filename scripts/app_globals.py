import os

from typing import Union, Callable
from tkinter import filedialog, font

os.system('color')



### Global Variables
# Console colors (ANSI codes stored as strings)
RED: str = '\033[91m'
GREEN: str = '\033[92m'
YELLOW: str = '\033[93m'
BLUE: str = '\033[94m'
DEFAULT: str = '\033[0m' # white

# Filepath to root directory
ROOT_DIR: str = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

# Filepath to settings file
SETTINGS_FILEPATH: str = os.path.join(ROOT_DIR, "data\\settings\\settings.json")

# Filepath to test files
TEST_DATA_FILEPATH: str = os.path.join(ROOT_DIR, "data\\test\\")

# Default settings list, to change default settings just modify this
# Note settings are saved & loaded so will prioritize saved settings
DEFAULT_SETTINGS: dict[str, Union[str, int]] = {
    'font': 'Calibri',
    'font_size': 75,
    'speed': 10,
    'win_w': 800,
    'win_h': 600,
    'win_x': 50,
    'win_y': 50
}

# Current settings list
CURRENT_SETTINGS: dict[str, Union[str, int]] = DEFAULT_SETTINGS.copy()

# Supported readers according to file extension and the function used to read them (located in file_readers.py)
# To extend support, add extension and function name here, and create the function in file_readers.py
SUPPORTED_READERS: dict[str, Callable[[str], str]] = {
    '.docx': '_read_docx',
    '.pdf': '_read_pdf',
    '.epub': '_read_epub'
}

# Fonts settings
FONTS: list = {}
FONT_SIZES: list = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 48, 72, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500]



### Console print functions
def print_error(message: str):
   print(f"{RED}[ERROR]: {message}{DEFAULT}")

def print_warning(message: str):
   print(f"{YELLOW}[WARNING]: {message}{DEFAULT}")

def print_success(message: str):
   print(f"{GREEN}{message}{DEFAULT}")

def print_blue(message: str):
   print(f"{BLUE}{message}{DEFAULT}")

def print_info(message: str):
   print(f"{message}")



### Helper functions
def load_fonts():
   global FONTS
   FONTS = sorted(list(font.families()))

def print_and_return_error(error_msg: str) -> str:
    print_error(error_msg)
    return error_msg

def inline_text(text: str) -> str:
    if text.strip():
        return text.strip().replace('\n', ' ') + " "
    return ""



### Filesystem functions
def file_exists(filepath: str) -> bool:
   return os.path.exists(filepath)

def get_filename(filepath: str) -> str:
    if file_exists(filepath):
        return os.path.basename(filepath)
    else:
        return print_and_return_error(f"No document file found at: {filepath}")

def get_extension(filepath: str) -> str:
   _, extension = os.path.splitext(filepath)
   return extension.lower()

def get_abs_filepath(relative_filepath: str) -> str:
   return os.path.join(ROOT_DIR, relative_filepath)

def get_test_file(test_file_name: str) -> str:
   return os.path.join(TEST_DATA_FILEPATH, test_file_name)

def ensure_file_exists(filepath: str) -> str:
   return os.makedirs(os.path.dirname(filepath), exist_ok=True)


def open_file_dialog() -> str:
   # Get supported file types
   file_types = [('', '')]
   all_extensions: str = ""

   for extension in SUPPORTED_READERS.keys():
      formatted_extension: str = '*' + extension

      all_extensions += formatted_extension + ';'
      file_types.append((extension.upper() + ' files', formatted_extension))
   
   file_types[0] = ('All supported files', all_extensions)
   
   # Open filedialog
   filepath: str = filedialog.askopenfilename(title='Select a file to read', filetypes=file_types)
   return filepath
