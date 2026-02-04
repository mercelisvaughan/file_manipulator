import io
from pypdf import PdfReader, PdfWriter

def merge_pdfs(files):
    """
    Merges a list of uploaded files into a single PDF.
    Returns: BytesIO object containing the merged PDF.
    """
    writer = PdfWriter()
    for f in files:
        reader = PdfReader(f)
        # Add every page from the current file to the writer
        for page in reader.pages:
            writer.add_page(page)
            
    return _writer_to_bytes(writer)

def split_pdf(file, mode='burst', page_range=None):
    """
    Splits a PDF based on the mode.
    - 'burst': Returns a list of (filename, bytes) for EVERY page.
    - 'range': Returns a single PDF bytes object containing only the requested pages.
    """
    reader = PdfReader(file)
    
    # MODE A: BURST (Explode into individual pages)
    if mode == 'burst':
        results = []
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            # Create a tuple: (filename, content)
            results.append((f"page_{i+1}.pdf", _writer_to_bytes(writer)))
        return results # Returns a list
    
    # MODE B: RANGE (Extract specific pages like "1-3")
    elif mode == 'range' and page_range:
        try:
            # Parse "1-3" into start=1, end=3
            start, end = map(int, page_range.split('-'))
            writer = PdfWriter()
            
            # Python uses 0-based indexing, so we subtract 1 from start
            # We loop from (start-1) up to (end)
            for i in range(start - 1, end):
                if i < len(reader.pages):
                    writer.add_page(reader.pages[i])
            return _writer_to_bytes(writer) # Returns single bytes object
        except ValueError:
            return None 

def rotate_pdf(file, angle):
    """
    Rotates all pages in the PDF by the given angle (90, 180, 270).
    """
    reader = PdfReader(file)
    writer = PdfWriter()
    
    for page in reader.pages:
        # pypdf's rotate function takes an integer (90, 180, etc)
        page.rotate(int(angle))
        writer.add_page(page)
        
    return _writer_to_bytes(writer)

def protect_pdf(file, password):
    """
    Encrypts the PDF with a password.
    """
    reader = PdfReader(file)
    writer = PdfWriter()
    
    # Copy all pages over
    writer.append_pages_from_reader(reader)
    
    # Encrypt the new file
    writer.encrypt(password)
    
    return _writer_to_bytes(writer)

def _writer_to_bytes(writer):
    """
    Internal helper function.
    Converts a PdfWriter object into a BytesIO object so Django can send it as a file download.
    """
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file.
    Returns: A BytesIO object containing the text as a .txt file.
    """
    reader = PdfReader(file)
    text_content = []

    # Loop through every page and extract text
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            text_content.append(f"--- Page {i+1} ---\n{text}\n")
        else:
            text_content.append(f"--- Page {i+1} ---\n[No text found or image-only page]\n")

    # Join all text
    full_text = "\n".join(text_content)

    # Convert string to bytes so Django can download it as a .txt file
    output_stream = io.BytesIO()
    output_stream.write(full_text.encode('utf-8'))
    output_stream.seek(0)
    
    return output_stream
