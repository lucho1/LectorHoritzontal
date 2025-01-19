import os
os.system('color')



### Global Variables
# Console colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
DEFAULT = '\033[0m' # white

# Default settings list, to change default settings just modify this
# Note settings are saved & loaded so will prioritize saved settings
DEFAULT_SETTINGS = {
    'font': 'Calibri',
    'font_size': 75,
    'speed': 10,
    'window_width': 800,
    'window_height': 600,
    'window_x': 50,
    'window_y': 50
}



### Console print functions
def print_error(message: str) -> None:
   print(f"{RED}[ERROR]: {message}{DEFAULT}")

def print_warning(message: str) -> None:
   print(f"{YELLOW}[WARNING]: {message}{DEFAULT}")

def print_success(message: str) -> None:
   print(f"{GREEN}{message}{DEFAULT}")

def print_blue(message: str) -> None:
   print(f"{BLUE}{message}{DEFAULT}")

def print_info(message: str) -> None:
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
def file_exists(filepath) -> bool:
   return os.path.exists(filepath)

def get_filename(filepath: str) -> str:
    if file_exists(filepath):
        return os.path.basename(filepath)
    else:
        return print_and_return_error(f"No document file found at: {filepath}")

def get_extension(filepath: str) -> str:
   _, extension = os.path.splitext(filepath)
   return extension.lower()
