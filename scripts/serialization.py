import json
import app_globals as app

from typing import Union



# Current Settings global var
_current_settings: dict[str, Union[str, int]] = app.DEFAULT_SETTINGS.copy()



# Getters & Setters
def get_current_settings() -> dict[str, Union[str, int]]:
    return _current_settings

def get_setting(setting_name: str) -> Union[str, int]:
    return _current_settings[setting_name]

def set_setting(setting_name: str, setting_value: Union[str, int]):
    _current_settings[setting_name] = setting_value
    

# Serialization functions
def save():
    global _current_settings
    if not _current_settings:
        _current_settings = app.DEFAULT_SETTINGS.copy()

    try:
        app.ensure_file_exists(app.SETTINGS_FILEPATH)
        with open(app.SETTINGS_FILEPATH, 'w') as f:
            json.dump(_current_settings, f)
    except Exception as e:
        app.print_error(f"Couldn't save settings: {e}")


def load() -> dict[str, Union[str, int]]:
    print("Loading settings...")
    global _current_settings
    _current_settings = app.DEFAULT_SETTINGS.copy()

    try:
        if app.file_exists(app.SETTINGS_FILEPATH):
            print(f"Settings loaded from: {app.SETTINGS_FILEPATH}")
            with open(app.SETTINGS_FILEPATH, 'r') as f:
                _current_settings.update(json.load(f))
        else:
            print(f"Using default settings, no settings file found at: {app.SETTINGS_FILEPATH}")
    except Exception as e:
        app.print_error(f"CUsing default settings, couldn't load settings: {e}")
    
    return _current_settings
