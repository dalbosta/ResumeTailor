import sys
import os

# Dynamically add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.utils import parse_resume  # Parse resume text from uploaded files
from app.nlp.model_response import generate_resume_suggestions


# Main Streamlit app
def main():
    """Main function to run Streamlit app for resume and job description matching."""

    # Title and Description
    st.title("Resume and Job Description Matcher")
    st.markdown(
        """
        Welcome to the **Resume Matcher App**!  
        Use this tool to evaluate the compatibility of your resume with a job description.  
        👉 **Steps**:
        1. Upload your resume (PDF format only).
        2. Paste the job description below.
        3. See insights and suggestions to improve your compatibility!
        """
    )

    # Sidebar for navigation (Optional)
    st.sidebar.header("Interaction")
    st.sidebar.info("Upload your resume and paste the job description using the inputs on the right!")

    # File Upload Widget (Resume)
    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF only)", type=["pdf"], help="Upload your resume in PDF format."
    )

    # Text Input for Job Description
    job_description = st.text_area(
        "Paste Job Description",
        placeholder="Paste the job description for the job you're targeting here...",
        help="Copy and paste detailed job descriptions for better matching.",
    )

    # Generate Button
    if st.button("Generate Suggestions"):
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

        # Generate suggestions using your API
        try:
            with st.spinner("Generating suggestions..."):
                result = generate_resume_suggestions(resume_text, job_description)

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
