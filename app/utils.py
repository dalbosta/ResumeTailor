import os
import tempfile

import PyPDF2
from docx import Document
from pdf2image import convert_from_path
import pytesseract

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}


def parse_resume(file_like):
    """
    Function to parse a resume file (FileStorage or file path) and extract all text.

    :param file_like: The file or file-like object (path or FileStorage).
    :return: A string containing all the text from the resume.
    """
    temp_file = None
    try:
        # Check if `file_like` is a path or FileStorage object
        if isinstance(file_like, str):
            file_path = file_like
        else:
            # Save the uploaded file temporarily
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_like.filename)[1])
            file_like.save(temp_file.name)
            temp_file.close()  # Explicitly close the file handle
            file_path = temp_file.name

        # Determine file extension and parse accordingly
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
            if not text.strip():
                print("No text extracted; attempting OCR...")
                text = extract_text_from_pdf_with_ocr(file_path)
            return text
        elif file_extension == '.docx':
            return extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    finally:
        # Clean up the temporary file if it was created
        if temp_file and os.path.exists(temp_file.name):
            os.unlink(temp_file.name)


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


def allowed_file(filename):
    """
    Validate if a file has one of the allowed extensions.
    :param filename: Name of the file to check
    :return: Boolean indicating if the file is allowed
    """

    # Validate if file has a proper extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
