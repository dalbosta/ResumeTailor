import sys
import os

# Dynamically add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.utils import parse_resume  # Parse resume text from uploaded files
from app.nlp.model import generate_resume_suggestions_with_key

# Constants for messages
ERROR_INVALID_API_KEY = "❌ Invalid API key format. API keys usually start with 'sk-'. Please check and try again."
ERROR_MISSING_API_KEY = "❌ Please enter a valid OpenAI API key before proceeding."
ERROR_NO_RESUME = "❌ Please upload a resume."
ERROR_NO_JOB_DESCRIPTION = "❌ Please input the job description."
ERROR_EMPTY_RESUME = "⚠️ Could not extract any text from the uploaded resume. Please check the file."
ERROR_PROCESSING = "An error occurred while processing the resume: {}"
ERROR_GENERATING_SUGGESTIONS = "An error occurred while generating suggestions: {}"
SUCCESS_API_KEY = "✅ API key verified successfully!"
SUCCESS_RESUME_PROCESSED = "✅ Resume successfully processed."


def validate_api_key(api_key_input):
    """
    Validate the OpenAI API key entered by the user.
    """
    if not api_key_input:
        st.error(ERROR_MISSING_API_KEY)
        return False

    if not api_key_input.startswith("sk-"):
        st.error(ERROR_INVALID_API_KEY)
        return False

    # Save API Key temporarily in session state for persistence
    st.session_state.api_key = api_key_input
    st.success(SUCCESS_API_KEY)
    return True


def validate_inputs(uploaded_file, job_description):
    """
    Validate uploaded resume and job description inputs.
    """
    if not uploaded_file:
        st.error(ERROR_NO_RESUME)
        return False

    if not job_description.strip():
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


def display_results(result):
    """
    Display the results of the LLM chain.
    """
    if "error" in result:
        # Display validation failure with details
        st.error(f"❌ {result['error']}")
        st.subheader("Details")
        for detail in result.get("details", []):
            st.write(f"- {detail}")
    else:
        # Display compatibility evaluation, suggestions, and bullet points
        st.subheader("🚀 Compatibility Evaluation")
        st.markdown(f"**{result.get('compatibility_evaluation', 'No compatibility evaluation available.')}**")

        st.subheader("🔍 Improvement Suggestions")
        st.write(result.get("suggestions", "No suggestions available."))

        st.subheader("💼 Example Resume Bullet Points")
        st.write(result.get("bullet_points", "No bullet points available."))


def main():
    """Main function to run the Streamlit app for resume and job description matching."""

    # Title and Description
    st.title("ResumeTailor 1.0")
    st.markdown(
        """
        <p style="line-height:1.5;font-size:16px;">
        Welcome to the <b>Resume Tailor App</b>! <br>
        Use this tool to evaluate the compatibility of your resume with a job description. <br>
        Project created by Derek Albosta. <br>
        Project repository: <a href="https://github.com/dalbosta/ResumeTailor" target="_blank">https://github.com/dalbosta/ResumeTailor</a>. <br><br>
        👉 <b>Steps</b>: <br>
        1. "Enter your OpenAI API Key. THIS KEY IS NOT STORED"<br>
        2. Upload your resume (PDF/DOCX format only).<br>
        3. Paste the job description below.<br>
        4. See insights and suggestions to improve your compatibility!<br>
        </p>
        """,
        unsafe_allow_html=True
    )

    # Step 1: Let the user enter their OpenAI API Key
    st.subheader("Step 1: Enter Your OpenAI API Key")
    api_key_input = st.text_input(
        "Enter your OpenAI API Key. THIS KEY IS NOT STORED",
        type="password",
        help="Your API key is required to call OpenAI services and will only be used during this session."
    )

    if not validate_api_key(api_key_input):
        return

    # Step 2: File Upload Widget (Resume)
    st.subheader("Step 2: Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF or DOCX only)",
        type=["pdf", "docx"],
        help="Upload your resume in either PDF or DOCX format."
    )

    # Step 3: Text Input for Job Description
    st.subheader("Step 3: Paste the Job Description")
    job_description = st.text_area(
        "Paste Job Description",
        placeholder="Paste the job description for the job you're targeting here...",
        help="Copy and paste detailed job descriptions for better matching.",
    )

    # Step 4: Generate Suggestions Button
    if st.button("Generate Suggestions"):

        if not validate_inputs(uploaded_file, job_description):
            return

        # Process resume
        resume_text = process_resume(uploaded_file)
        if resume_text is None:
            return

        # Generate suggestions
        try:
            with st.spinner("Generating suggestions..."):
                result = generate_resume_suggestions_with_key(
                    resume_text, job_description, st.session_state.api_key
                )
            display_results(result)
        except Exception as e:
            st.error(ERROR_GENERATING_SUGGESTIONS.format(e))


if __name__ == "__main__":
    main()
