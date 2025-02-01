import app_globals as app

from file_readers import read_file



class TextManager:
    def __init__(self):
        self.current_text_pos: float = 0.0
    

    ### Public functions
    def scroll_text(self, speed: float) -> float:
        self.current_text_pos = min(1.0, self.current_text_pos + speed)
        self.current_text_pos = max(0.0, self.current_text_pos)
        return self.current_text_pos

    
    def open_new_file(self) -> str:
        # Open file dialog
        document_path: str = app.open_file_dialog()
        if not document_path:
            ret = f"Couldn't find document path: {document_path}"
            app.print_error(ret)
            return ret
        
        # Try read new file and return its content
        try:
            new_text: str = read_file(document_path)
            self.current_text_pos = 0.0
            return new_text
            
            # TODO Update window title with filename
            #self.window.update_title(f"Lector Horitzontal - {app.get_filename(document_path)}")
        except Exception as e:
            ret = f"Error loading file: {e}"
            app.print_error(ret)
            return ret