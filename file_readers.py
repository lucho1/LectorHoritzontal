import os
import ebooklib

from docx import Document
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup



# Private reader functions
def _read_docx(filepath):
    try:
        # Create a Document object
        doc = Document(filepath)
        ret = ""
        
        # Iterate through paragraphs and print their text
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only print non-empty paragraphs
                ret += paragraph.text.strip().replace('\n', ' ') + " "
        
        if ret:
            print("\n\nSuccessfully read text in file!")
        else:
            print("\n\nNo text found in file!")
            ret = f"Error: No text found in file!"
        
        return ret
                
    except Exception as e:
        print(f"\n\nError reading the file: {e}")
        return f"Error reading the file: {e}"


def _read_pdf(filepath):
    try:
        # Create a PDF reader object
        reader = PdfReader(filepath)
        ret = ""
        
        # Iterate through all pages and print text
        for page_num in range(len(reader.pages)):
            # Get the page object
            page = reader.pages[page_num]
            
            # Extract text from page
            text = page.extract_text()
            if text.strip():
                ret += text.strip().replace('\n', ' ') + " "
                
        if ret:
            print("\n\nSuccessfully read text in file!")
        else:
            print("\n\nNo text found in file!")
            ret = f"Error: No text found in file!"
        
        return ret
                
    except Exception as e:
        print(f"\n\nError reading the file: {e}")
        return f"Error reading the file: {e}"


def _read_epub(filepath):
    try:
        # Create epub reader object
        book = epub.read_epub(filepath)
        ret = ""
        
        # Iterate through all the items
        for item in book.get_items():
            # If item is document content
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Get the content
                content = item.get_content()
                
                # Parse HTML content with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Get text content
                text = soup.get_text()
                
                # Print cleaned text (if not empty)
                if text.strip():
                    ret += text.strip().replace('\n', ' ') + " "
        
        if ret:
            print("\n\nSuccessfully read text in file!")
        else:
            print("\n\nNo text found in file!")
            ret = f"Error: No text found in file!"
        
        return ret
                
    except Exception as e:
        print(f"\n\nError reading the file: {e}")
        return f"Error reading the file: {e}"



# List of available readers according to file extension
# To extend support, add extension and function name here, and create the function below)
AVAILABLE_READERS = {
        '.docx': _read_docx,
        '.pdf': _read_pdf,
        '.epub': _read_epub
}

# Main public function to use in this script
def read_file(filepath):
    # Get file extension and convert to lowercase
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    if extension in AVAILABLE_READERS:
        print(f"\nReading '{extension}' file: {filepath}")
        return AVAILABLE_READERS[extension](filepath)
    else:
        print(f"\nUnsupported file type: '{extension}'")
        return f"Error: Unsupported file type '{extension}'"