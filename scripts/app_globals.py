import os
from typing import Union
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
    'window_width': 800,
    'window_height': 600,
    'window_x': 50,
    'window_y': 50
}



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
