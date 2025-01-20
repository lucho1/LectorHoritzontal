import json
import app_globals as app

from typing import Union



# Getters & Setters
def get_current_settings() -> dict[str, Union[str, int]]:
    return app.CURRENT_SETTINGS

def get_setting(setting_name: str) -> Union[str, int]:
    return app.CURRENT_SETTINGS[setting_name]

def set_setting(setting_name: str, setting_value: Union[str, int]):
    app.CURRENT_SETTINGS[setting_name] = setting_value
    

# Serialization functions
def save():
    if not app.CURRENT_SETTINGS:
        app.CURRENT_SETTINGS = app.DEFAULT_SETTINGS.copy()

    try:
        app.ensure_file_exists(app.SETTINGS_FILEPATH)
        with open(app.SETTINGS_FILEPATH, 'w') as f:
            json.dump(app.CURRENT_SETTINGS, f)
    except Exception as e:
        app.print_error(f"Couldn't save settings: {e}")


def load() -> dict[str, Union[str, int]]:
    print("Loading settings...")
    app.CURRENT_SETTINGS = app.DEFAULT_SETTINGS.copy()

    try:
        if app.file_exists(app.SETTINGS_FILEPATH):
            print(f"Settings loaded from: {app.SETTINGS_FILEPATH}")
            with open(app.SETTINGS_FILEPATH, 'r') as f:
                app.CURRENT_SETTINGS.update(json.load(f))
        else:
            print(f"Using default settings, no settings file found at: {app.SETTINGS_FILEPATH}")
    except Exception as e:
        app.print_error(f"CUsing default settings, couldn't load settings: {e}")
    
    return app.CURRENT_SETTINGS
