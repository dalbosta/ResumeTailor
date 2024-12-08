import os
import PyPDF2
from docx import Document
from pdf2image import convert_from_path
import pytesseract


def parse_resume(file_path):
    """
    Function to parse a resume file and extract all text.

    :param file_path: The path to the resume file.
    :return: A string containing all the text from the resume.
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
        if not text.strip():
            # Fallback to OCR if no text is extracted
            print("No text extracted; attempting OCR...")
            text = extract_text_from_pdf_with_ocr(file_path)
        return text
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Number of pages: {len(reader.pages)}")
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_text_from_pdf_with_ocr(file_path):
    # Convert PDF to image using pdf2image
    pages = convert_from_path(file_path, 300)
    text = ""
    for page in pages:
        # Convert the image to text using pytesseract
        text += pytesseract.image_to_string(page)
    return text


def extract_text_from_docx(file_path):
    text = ""
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

# Usage of pytesseract requires it to be installed on your machine.
