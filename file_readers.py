import os
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



### Main public functions to use in this script
def get_filename(filepath: str) -> str:
    if os.path.exists(filepath):
        return os.path.basename(filepath)
    else:
        return _print_and_return_str(f"No document file found at: {filepath}")

def read_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return _print_and_return_str(f"No document file found at: {filepath}")

    # Get file extension and convert to lowercase
    print("Reading Document: " + filepath)
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    # Check if we can read it
    if extension not in AVAILABLE_READERS:
        return _print_and_return_str(f"\nError: Unsupported file type '{extension}'")
    
    # Try reading it
    file_text_content: str = ""
    try:
        reader_function: Callable[[str], str] = globals()[AVAILABLE_READERS[extension]]
        file_text_content: str = reader_function(filepath)
    except Exception as e:
        return _print_and_return_str(f"\n\nError reading file: {e}")

    # Check if it's not empty
    if file_text_content == "":
        return _print_and_return_str(f"\n\nNo text found in file!")

    print("\n\nSuccessfully read text in file!")
    print(f"\nDisplaying text from '{extension}' file at: {filepath}")
    return file_text_content



### Private Helper functions
def _print_and_return_str(error: str) -> str:
    print(error)
    return error

def _inline_text(text: str) -> str:
    if text.strip():
        return text.strip().replace('\n', ' ') + " "
    return ""



### Private Reader functions
def _read_docx(filepath: str) -> str:
    doc = Document(filepath)
    ret: str = ""
    
    # Iterate paragraphs in doc and append their text
    for paragraph in doc.paragraphs:
        ret += _inline_text(paragraph.text)
        
    return ret

def _read_pdf(filepath: str) -> str:
    doc = PdfReader(filepath)
    ret: str = ""
        
    # Iterate pages in the doc, get their object and extract & append text
    for page_num in range(len(doc.pages)):
        page = doc.pages[page_num]
        ret += _inline_text(page.extract_text())
        
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
        ret += _inline_text(soup.get_text())
        
    return ret
