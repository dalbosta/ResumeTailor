import tempfile
import os
from werkzeug.datastructures import FileStorage
from pdf2image import convert_from_path
import PyPDF2
from docx import Document
import pytesseract


def parse_resume(file_obj):
    """
    Parse a resume file, handling both Flask (FileStorage), Streamlit (UploadedFile), and file paths (string).
    Converts the file into a temporary file for processing and extracts text based on the file type.

    :param file_obj: The file object (Flask FileStorage, Streamlit UploadedFile, or file path as string).
    :return: A string containing all extracted text from the resume.
    """

    temp_file_path = None  # Store the temporary file path for cleanup and debugging
    try:
        # Step 1: Handle different input types (Flask FileStorage, Streamlit UploadedFile, or file path)
        if isinstance(file_obj, str):  # If it's a file path
            file_path = file_obj

        elif isinstance(file_obj, FileStorage):  # Flask's FileStorage object
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_obj.filename)[1]) as temp_file:
                file_obj.save(temp_file.name)
                temp_file_path = temp_file.name
            file_path = temp_file_path

        elif hasattr(file_obj, "read") and hasattr(file_obj, "name"):  # Streamlit's UploadedFile object
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_obj.name)[1]) as temp_file:
                temp_file.write(file_obj.read())
                temp_file.flush()
                temp_file_path = temp_file.name
            file_path = temp_file_path

        else:
            raise ValueError(f"Unsupported file object type: {type(file_obj)}")

        # Debugging: Log the file path being processed
        print(f"Temporary file created at: {file_path}")

        # Step 2: Determine the file type from its extension
        file_extension = os.path.splitext(file_path)[1].lower()

        # Step 3: Parse the file based on its type
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)  # Extract text from PDF
            if not text.strip():  # Attempt OCR if no text is extracted
                print("No text extracted from PDF. Trying OCR...")
                text = extract_text_from_pdf_with_ocr(file_path)
            return text

        elif file_extension == '.docx':
            return extract_text_from_docx(file_path)  # Extract text from DOCX files

        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    finally:
        # Step 4: Cleanup temporary file after processing
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)  # Delete the temp file
                print(f"Temporary file deleted: {temp_file_path}")
            except PermissionError as e:
                print(f"Permission error while deleting temp file: {e}")
            except Exception as e:
                print(f"Error while deleting temp file: {e}")


def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyPDF2.

    :param file_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f"Number of pages in PDF: {len(pdf_reader.pages)}")
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_text_from_pdf_with_ocr(file_path):
    """
    Extracts text from a PDF by converting it to images and running OCR (using pytesseract).

    :param file_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""

    try:
        # Convert PDF pages to images
        pages = convert_from_path(file_path, dpi=300)  # Removed 'use_temp=True'
        for page_index, page in enumerate(pages):
            print(f"Running OCR on page {page_index + 1}...")
            text += pytesseract.image_to_string(page)
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        raise e

    return text



def extract_text_from_docx(file_path):
    """
    Extracts text from a DOCX file.

    :param file_path: Path to the DOCX file.
    :return: Extracted text as a string.
    """
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
    allowed_extensions = {'pdf', 'doc', 'docx', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
