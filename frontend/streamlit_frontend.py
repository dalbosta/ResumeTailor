import sys
import os

# Dynamically add the root directory to sys.path (if needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.utils import parse_resume  # Parse resume text from uploaded files
from app.nlp.model import run_full_analysis

# Constants for messages
ERROR_INVALID_API_KEY = "❌ Invalid API key format. API keys usually start with 'sk-'. Please check and try again."
ERROR_MISSING_API_KEY = "❌ Please enter a valid OpenAI API key and SERP API key before proceeding."
ERROR_NO_RESUME = "❌ Please upload a resume."
ERROR_NO_JOB_DESCRIPTION = "❌ Please input the job description."
ERROR_EMPTY_RESUME = "⚠️ Could not extract any text from the uploaded resume. Please check the file."
ERROR_PROCESSING = "An error occurred while processing the resume: {}"
ERROR_ANALYSIS = "An error occurred during the analysis: {}"
SUCCESS_API_KEY = "✅ API keys verified successfully!"
SUCCESS_RESUME_PROCESSED = "✅ Resume successfully processed."


def validate_api_keys(openai_api_key_input, serp_api_key_input):
    """
    Validate the OpenAI and SERP API keys entered by the user.
    """
    if not openai_api_key_input or not serp_api_key_input:
        st.error(ERROR_MISSING_API_KEY)
        return False

    if not openai_api_key_input.startswith("sk-"):
        st.error(ERROR_INVALID_API_KEY)
        return False

    # Save API Keys temporarily in session state for persistence
    st.session_state.openai_api_key = openai_api_key_input
    st.session_state.serp_api_key = serp_api_key_input
    st.success(SUCCESS_API_KEY)
    return True


def validate_inputs(uploaded_file, job_description_text):
    """
    Validate uploaded resume and job description inputs.
    """
    if not uploaded_file:
        st.error(ERROR_NO_RESUME)
        return False

    if not job_description_text.strip():
        st.error(ERROR_NO_JOB_DESCRIPTION)
        return False

    return True


def process_resume(uploaded_file):
    """
    Parse and process the uploaded resume file.
    """
    try:
        with st.spinner("Parsing the resume..."):
            resume_text = parse_resume(uploaded_file)
            if not resume_text.strip():
                st.warning(ERROR_EMPTY_RESUME)
                return None
        st.success(SUCCESS_RESUME_PROCESSED)
        return resume_text
    except Exception as e:
        st.error(ERROR_PROCESSING.format(e))
        return None


def display_results(results):
    """
    Display results of the `run_full_analysis` function.
    """
    if "error" in results:
        # Error from `run_full_analysis`
        st.error(results["error"])
        if "details" in results:
            st.subheader("Details")
            for detail in results["details"]:
                st.write(f"- {detail}")
        return

    # Display results
    st.subheader("✅ Validation Results")
    validation_results = results.get("validation_results", "No validation results available.")
    st.write(validation_results)

    st.subheader("📊 Compatibility Evaluation")
    compatibility = results.get("analysis", {}).get("compatibility_evaluation", "N/A")
    st.write(f"**{compatibility}**")

    st.subheader("🔍 Suggestions for Improvement")
    suggestions = results.get("analysis", {}).get("suggestions", "No suggestions available.")
    st.write(suggestions)

    st.subheader("💼 Resume Bullet Points")
    bullet_points = results.get("analysis", {}).get("bullet_points", "No bullet points available.")
    st.write(bullet_points)

    st.subheader("🔎 Interview Insights")
    interview_insights = results.get("interview_insights", "No interview insights available.")
    st.write(interview_insights)


def generate_insights(uploaded_file, job_description_text):
    """
    Generate insights by running the full analysis pipeline.
    """
    # Validate inputs
    if not validate_inputs(uploaded_file, job_description_text):
        return

    # Process the uploaded resume
    resume_text = process_resume(uploaded_file)
    if not resume_text:
        return

    # Run the analysis pipeline
    try:
        with st.spinner("Running full analysis..."):
            results = run_full_analysis(
                resume_text=resume_text,
                job_description=job_description_text,
                serp_api_key=st.session_state.serp_api_key,
                openai_api_key=st.session_state.openai_api_key,
            )
        display_results(results)
    except Exception as e:
        st.error(str(e))  # Use the exception message directly



def main():
    """
    Main entry-point function for running the Streamlit app.
    """
    # Title and description
    st.title("Resume Tailor 1.0")
    st.markdown(
        """
        <p style="line-height:1.5;font-size:16px;">
        🚀 Welcome to <b>Resume Tailor 2.0</b>! <br>
        📄 Use this tool to evaluate how well your resume aligns with job descriptions.
        <br>
        🎯 This tool provides compatibility evaluations, tailored suggestions, and more insights!
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Step 1: API Key Section
    st.subheader("Step 1: Enter Your API Keys")
    openai_api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key for LLM analysis. (Starts with 'sk-')"
    )
    serp_api_key_input = st.text_input(
        "SERP API Key",
        type="password",
        help="Enter your SERP API key for fetching interview insights."
    )
    if not validate_api_keys(openai_api_key_input, serp_api_key_input):
        return

    # Step 2: Resume Upload Section
    st.subheader("Step 2: Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload resume (PDF or DOCX format)",
        type=["pdf", "docx"],
        help="Accepted formats: PDF, DOCX. Smaller files are recommended for better analysis."
    )

    # Step 3: Job Description Section
    st.subheader("Step 3: Paste the Job Description")
    job_description_text = st.text_area(
        "Paste Job Description",
        placeholder="Copy and paste the job description here...",
        help="Better descriptions generate more relevant feedback!"
    )

    # Analyze inputs when button is clicked
    if st.button("Generate Insights"):
        generate_insights(uploaded_file, job_description_text)


if __name__ == "__main__":
    main()
