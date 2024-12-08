# app/routes/resume_routes.py

import os
from flask import Blueprint, request, jsonify
from app.utils import allowed_file, save_file

# Assume this path exists and is writable
#temporary test with static file
UPLOAD_PATH = '../../uploads/resumes'

resume_bp = Blueprint('resume', __name__)

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_PATH, exist_ok=True)

@resume_bp.route('/resume/upload', methods=['POST'])
def upload_resume():
    """
    Endpoint to upload a resume file.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if allowed_file(file.filename):
        # Save the file in the specified upload directory
        saved_path = save_file(file, UPLOAD_PATH)
        return jsonify({'message': f'File {file.filename} uploaded successfully', 'path': saved_path})
    else:
        return jsonify({'error': 'Unsupported file format'}), 400


@resume_bp.route('/resume/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """
    Endpoint to retrieve a resume by ID.
    """
    # Mock-up logic for retrieving resume data
    return jsonify({'resume_id': resume_id, 'content': 'Sample resume content'})
