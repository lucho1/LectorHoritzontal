import app_globals as app
import serialization

from text_manager import TextManager



class AppController:
    def __init__(self, text_manager: TextManager):
        # Set variables
        self.font: str = ""
        self.font_size: int = 0
        self.scroll_speed: float = 0.0
        self.current_position: float = 0.0
        self.bg_color: str = ""
        self.text_color: str = ""
        self.text_manager = text_manager

        # Reset settings and load them
        self.reset_settings(False)
        self._load_settings()


    ### Public functions TODO: Change name current_font to font
    def get_current_font(self) -> app.FontTuple:
        return (self.font, self.font_size)
    
    def get_bg_color(self) -> str:
        return self.bg_color

    def get_text_color(self) -> str:
        return self.text_color    
    
    def get_scroll_speed(self) -> float:
        return self.scroll_speed
    
    
    ### Public callback methods
    def on_font_size_changed(self, new_size: int) -> app.FontTuple:
        self.font_size = new_size
        self._save_settings()
        return self.get_current_font()
    

    def on_font_changed(self, new_font: str) -> app.FontTuple:
        self.font = new_font
        self._save_settings()
        return self.get_current_font()
    
    def on_bg_color_changed(self, new_color: str):
        self.bg_color = new_color
        self._save_settings()
    
    
    def on_text_color_changed(self, new_color: str):
        self.text_color = new_color
        self._save_settings()

    
    def on_scroll_speed_changed(self, new_scroll_speed: float):
        self.scroll_speed = new_scroll_speed
        self._save_settings()

    
    def scroll(self, scroll_right: bool) -> float:
        # Calculate speed
        speed: float = self.scroll_speed
        speed = speed if scroll_right else -speed
        speed /= float(100000)

        # Scroll text and return new pos
        return self.text_manager.scroll_text(speed)

    
    def reset_settings(self, save: bool = True):
        # Set settings back to default and save
        self.font = app.DEFAULT_SETTINGS['font']
        self.font_size = app.DEFAULT_SETTINGS['font_size']
        self.scroll_speed = app.DEFAULT_SETTINGS['speed']

        if save:
            self._save_settings()
    
    
    def open_new_file(self) -> str:
        return self.text_manager.open_new_file()
    

    ### Serialization
    def _save_settings(self):
        serialization.set_setting('font', self.font)
        serialization.set_setting('font_size', self.font_size)
        serialization.set_setting('speed', self.scroll_speed)

        serialization.set_setting('bg_color', self.bg_color)
        serialization.set_setting('text_color', self.text_color)
        serialization.save()
    
    
    def _load_settings(self):
        self.font = str(serialization.get_setting('font'))
        self.font_size = int(serialization.get_setting('font_size'))
        self.scroll_speed = float(serialization.get_setting('speed'))

        self.bg_color = str(serialization.get_setting('bg_color'))
        self.text_color = str(serialization.get_setting('text_color'))
