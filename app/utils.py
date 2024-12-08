# app/utils.py

import os


def allowed_file(filename, allowed_extensions={'pdf', 'doc', 'docx'}):
    """
    Check if the uploaded file has an allowed extension.

    :param filename: The name of the uploaded file.
    :param allowed_extensions: Set of allowed file extensions.
    :return: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file, upload_path):
    """
    Saves the uploaded file to the designated path.

    :param file: File object from request.
    :param upload_path: Path to save the file.
    :return: Path where the file is saved.
    """
    filepath = os.path.join(upload_path, file.filename)
    file.save(filepath)
    return filepath

# Additional utility functions can be added here as needed.
