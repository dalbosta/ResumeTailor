from flask import Blueprint, request, jsonify
from app.nlp.model import generate_resume_suggestions_with_key
from app.utils import allowed_file
from app.utils import parse_resume

from api_keys.keys import OPENAI_API_KEY

# Define a Blueprint for routes
resume_tailor_bp = Blueprint('resume', __name__)


@resume_tailor_bp.route('/resume/upload', methods=['POST'])
def upload_and_generate_response():
    """
    Upload a resume, parse its content, and compare it with the job description.
    Returns model suggestions.
    """
    try:
        # Get and validate the uploaded file
        uploaded_file = get_uploaded_file()

        # Get and validate the job description text
        job_description = get_job_description()

        # Parse the resume to extract text content
        try:
            resume_contents = parse_resume(uploaded_file)
        except Exception as parse_error:
            # Handle specific parsing errors
            raise ValueError(f"Failed to parse the resume: {str(parse_error)}")

        # Generate GPT suggestions using extracted resume text and job description text
        suggestions = generate_resume_suggestions_with_key(
            resume_text=resume_contents, job_description=job_description, user_openai_api_key=OPENAI_API_KEY)

        # Return the AI's suggestions
        return jsonify({
            'message': 'Resume processed and response generated successfully',
            'suggestions': suggestions
        }), 200

    except ValueError as ve:
        # Handle validation and parsing-related errors
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Handle unexpected errors (e.g., runtime issues)
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


def get_uploaded_file():
    """
    Retrieves and validates the uploaded file from the request.
    :return: The uploaded file object if valid.
    :raises ValueError: If the file is missing, empty, or invalid.
    """
    if 'file' not in request.files:
        raise ValueError("No file part in the request")

    file = request.files['file']

    if file.filename == '':
        raise ValueError("No selected file")

    if not allowed_file(file.filename):
        raise ValueError("Unsupported file format")

    return file


def get_job_description():
    """
    Retrieves and validates the job description text from the request.
    :return: The job description text if valid.
    :raises ValueError: If the job description is missing or empty.
    """
    job_description = request.form.get('job_description')
    if not job_description:
        raise ValueError("Job description is required")
    return job_description
