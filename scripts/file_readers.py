import app_globals as app
import ebooklib

from typing import Callable
from docx import Document
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup



### Variable list of available readers according to file extension
### To extend support, add extension and function name here, and create the function below
AVAILABLE_READERS: dict[str, Callable[[str], str]] = {
    '.docx': '_read_docx',
    '.pdf': '_read_pdf',
    '.epub': '_read_epub'
}



### Main public function to use in this script
def read_file(filepath: str) -> str:
    # Get file extension and convert to lowercase
    app.print_info("Reading Document: " + filepath)
    extension = app.get_extension(filepath)

    # Check if we can read it
    if extension not in AVAILABLE_READERS:
        return app.print_and_return_error(f"Unsupported file type '{extension}'")
    
    # Try reading it
    file_text_content: str = ""
    try:
        reader_function: Callable[[str], str] = globals()[AVAILABLE_READERS[extension]]
        file_text_content: str = reader_function(filepath)
    except Exception as e:
        return app.print_and_return_error(f"Couldn't read file: {e}")

    # Check if it's not empty
    if file_text_content == "":
        return app.print_and_return_error(f"No text found in file!")

    app.print_success("\n\nSuccessfully read text in file!")
    return file_text_content



### Private Reader functions
def _read_docx(filepath: str) -> str:
    doc = Document(filepath)
    ret: str = ""
    
    # Iterate paragraphs in doc and append their text
    for paragraph in doc.paragraphs:
        ret += app.inline_text(paragraph.text)
        
    return ret

def _read_pdf(filepath: str) -> str:
    doc = PdfReader(filepath)
    ret: str = ""
        
    # Iterate pages in the doc, get their object and extract & append text
    for page_num in range(len(doc.pages)):
        page = doc.pages[page_num]
        ret += app.inline_text(page.extract_text())
        
    return ret

def _read_epub(filepath: str) -> str:
    doc = epub.read_epub(filepath)
    ret: str = ""
        
    # Iterate all the doc items
    for item in doc.get_items():
        # If item is not document, skip it
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        
        # Parse item content with BeautifulSoup (HTML parser) and append its text
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        ret += app.inline_text(soup.get_text())
        
    return ret
