import sys
import os

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

# Dynamically add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.utils import parse_resume  # Parse resume text from uploaded files
from app.nlp.model_response import generate_resume_suggestions_with_key
from langchain_community.llms import OpenAI  # Import OpenAI client


# Main Streamlit app
def main():
    """Main function to run Streamlit app for resume and job description matching."""

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

    if api_key_input and not api_key_input.startswith("sk-"):
        st.error("❌ Invalid API key format. API keys usually start with 'sk-'. Please check and try again.")
        return

    # Save API Key temporarily in session state for persistence
    if "api_key" not in st.session_state:
        st.session_state.api_key = None

    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ API key verified successfully!")

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

        # Validate API key
        if "api_key" not in st.session_state or not st.session_state.api_key:
            st.error("❌ Please enter a valid OpenAI API key before proceeding.")
            return

        # Validate inputs
        if not uploaded_file:
            st.error("❌ Please upload a resume.")
            return

        if not job_description.strip():
            st.error("❌ Please input the job description.")
            return

        # Process uploaded resume
        try:
            with st.spinner("Parsing the resume..."):
                resume_text = parse_resume(uploaded_file)
                if not resume_text.strip():
                    st.warning("⚠️ Could not extract any text from the uploaded resume. Please check the file.")
                    return
            st.success("✅ Resume successfully processed.")
        except Exception as e:
            st.error(f"An error occurred while processing the resume: {e}")
            return

        # Generate suggestions using the user's API key
        try:
            with st.spinner("Generating suggestions..."):

                # Dynamically use the user's API key to call LangChain's OpenAI client
                result = generate_resume_suggestions_with_key(
                    resume_text, job_description, st.session_state.api_key
                )

            # Display results
            st.subheader("🚀 Compatibility Evaluation")
            st.markdown(f"**{result['compatibility_evaluation']}**")

            st.subheader("🔍 Improvement Suggestions")
            st.write(result.get("suggestions", "No suggestions available."))

            st.subheader("💼 Example Resume Bullet Points")
            st.write(result.get("bullet_points", "No bullet points available."))
        except Exception as e:
            st.error(f"An error occurred while generating suggestions: {e}")

if __name__ == "__main__":
    main()
