from flask import Blueprint, request, jsonify
from app.nlp.model import run_full_analysis
from app.utils import allowed_file, parse_resume
from api_keys.keys import OPENAI_API_KEY, SERP_API_KEY
from app.nlp.model import LLMHelper  # Assuming LLMHelper is accessible here

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

            if not resume_text.strip():
                raise ValueError(
                    "The uploaded resume is empty or could not be parsed.\n"
                    "Please upload a valid file."
                )

        except Exception as parse_error:
            raise ValueError(f"Failed to parse the resume:\n{str(parse_error)}")

        # Step 4: Run the analysis
        try:
            results = run_full_analysis(
                resume_text=resume_text,
                job_description=job_description,
                serp_api_key=SERP_API_KEY,
                openai_api_key=OPENAI_API_KEY
            )

            # Handle specific errors
            if "error" in results:
                return jsonify({
                    "error": results["error"].replace("\n", "<br>"),
                    "details": results.get("details", [])
                }), 400

        except Exception as analysis_error:
            raise ValueError(f"Analysis error:\n{str(analysis_error)}")

        # Step 4.5: Extract and validate company name and job title
        try:
            llm_helper = LLMHelper(api_key=OPENAI_API_KEY)  # Instantiate the LLM helper
            company_name, job_title = llm_helper.extract_company_and_job_title(job_description)
        except ValueError as extraction_error:
            return jsonify({"error": str(extraction_error)}), 400

        # Step 5: Return analysis results (success response)
        return jsonify({
            "message": "Analysis conducted successfully.",
            "results": results,
            "company_name": company_name,
            "job_title": job_title,
        }), 200

    # Handle any validation or unexpected errors
    except ValueError as ve:
        return jsonify({"error": str(ve).replace("\n", "<br>")}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error:\n{str(e).replace('\n', '<br>')}"}), 500


# Helper functions remain unchanged.
def get_uploaded_file():
    """
    Retrieve and validate the uploaded file from the request.
    """
    if 'file' not in request.files:
        raise ValueError("No file was uploaded in the request.")

    file = request.files['file']

    if file.filename == '':
        raise ValueError("The uploaded file is empty. Please select a valid file.")

    if not allowed_file(file.filename):
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

    return file


def get_job_description():
    """
    Retrieve and validate the job description provided in the request.
    """
    job_description = request.form.get('job_description')
    if not job_description or not job_description.strip():
        raise ValueError("Job description is required and cannot be empty.")
    return job_description
