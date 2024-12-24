from flask import Blueprint, request, jsonify
from app.nlp.model import run_full_analysis
from app.utils import allowed_file, parse_resume
from api_keys.keys import OPENAI_API_KEY, SERP_API_KEY

# Define a Blueprint for routes
resume_tailor_bp = Blueprint('resume', __name__)


@resume_tailor_bp.route('/resume/upload', methods=['POST'])
def upload_and_generate_response():
    """
    Upload a resume, parse its content, and analyze it against the job description.
    Returns analysis results including validation, suggestions, and interview insights.
    """
    try:
        # Step 1: Get and validate the uploaded file
        uploaded_file = get_uploaded_file()

        # Step 2: Get and validate the job description text
        job_description = get_job_description()

        # Step 3: Parse the resume to extract text content
        try:
            resume_text = parse_resume(uploaded_file)
        except Exception as parse_error:
            raise ValueError(f"Failed to parse the resume: {str(parse_error)}")

        # Step 4: Call the analysis function with the inputs
        try:
            results = run_full_analysis(
                resume_text=resume_text,
                job_description=job_description,
                serp_api_key=SERP_API_KEY,  # Pass the SERP API Key from config
                openai_api_key=OPENAI_API_KEY  # Pass the OpenAI API Key from config
            )
        except Exception as analysis_error:
            raise ValueError(f"Failed to run analysis: {str(analysis_error)}")

        # Step 5: Return the analysis results
        return jsonify({
            'message': 'Resume analyzed successfully',
            'results': results
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
