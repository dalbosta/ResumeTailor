# ResumeTailor: A Resume Optimization and Job Matching Tool

**ResumeTailor** is a tool that leverages AI to assist job seekers by optimizing their resumes and providing tailored insights based on a specific job description. It performs advanced validation, evaluates compatibility, suggests improvements, and even builds interview preparation insights by researching the target company and job role.

---

## Features

1. **Validation of Inputs (Resumes and Job Descriptions)**:
   Ensures both job descriptions and resumes meet required standards by checking for content validity, clarity, and sufficiency.

2. **Comprehensive Analysis**:
   Analyzes the compatibility between your resume and job description and highlights factors that impact your chances.

3. **Actionable Suggestions**:
   Provides meaningful, AI-driven suggestions to improve your resume for better alignment with the job description.

4. **Tailored Resume Bullet Points**:
   Suggests professionally crafted, result-oriented resume bullet points aligned with the target job.

5. **Interview Insights**:
   Performs research on the target company and job role and provides interview preparation insights using web search integrations.

6. **Simple File Parsing**:
   Parses and extracts text from resumes in **PDF**, **DOCX**, and image-based PDFs (via OCR) formats.

---

## New Features Introduced

The latest update adds the following enhancements:

1. **Integration with Advanced Analysis Workflow (`run_full_analysis`)**:
   - Combines multiple steps, such as validating resume/job description, performing compatibility analysis, generating tailored suggestions, and providing interview insights, into a single flow.
   - Automatically extracts the company name and job title from the job description for targeted insights.

2. **Interview Preparation Insights**:
   - Uses the SERP API to gather information about the company and job role's interview process and supplements this data with analysis from OpenAI's GPT-based models.
   - Converts real-world data into actionable insights for interview preparation.

3. **Dynamic Validation and Suggestions**:
   - Performs detailed validation of both resume quality and job descriptions with specific error messaging.
   - Provides highly customized suggestions and bullet points tailored to the unique combination of resume and job description.

4. **Error Handling Improvements**:
   - Enhanced error checking with detailed messages for missing or invalid inputs, unsupported file types, and other failures during parsing and analysis.

---

## Requirements

To run the updated project, you need the following:

1. **Python version:** >= 3.13.1  
2. **Dependencies:**  
   Install the required Python libraries using:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Keys:**  
   The application requires:
   - **OpenAI API Key**: For GPT-based analysis.
   - **SERP API Key**: For interview preparation insights via web search.

4. **Tesseract OCR** (optional):  
   Required for extracting text from image-based PDFs. Install instructions are available [here](https://github.com/tesseract-ocr/tesseract).

---

## Installation

Follow these steps to set up and run the application:

1. Clone the repository:
   ```bash
   git clone https://github.com/dalbosta/ResumeTailor.git
   cd ResumeTailor
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # On macOS or Linux
   venv\Scripts\activate           # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables for API keys:
   - **Option 1**: Add keys to `api_keys/keys.py` like:
     ```python
     OPENAI_API_KEY = "your-openai-api-key"
     SERP_API_KEY = "your-serp-api-key"
     ```
   - **Option 2**: Set the keys as environment variables:
     ```bash
     export OPENAI_API_KEY="your-openai-api-key"
     export SERP_API_KEY="your-serp-api-key"
     ```

---

## How It Works

### 1. Resume Parsing and Validation
The application accepts resumes in **PDF** or **DOCX** formats. During parsing:
   - Text content is extracted using `PyPDF2` or `python-docx`.
   - For image-based documents, it uses **OCR** via `pytesseract`.
   - Inputs (resume and job description) are validated to ensure they are sufficient for further processing.

### 2. Advanced Analysis Workflow
The core logic (`run_full_analysis`) performs:
   - **Validation**: Evaluates both the job description and resume for completeness and validity.
   - **Analysis**:
     - Compatibility evaluation between the resume and job description.
     - Suggestions to improve your resume.
     - Example resume bullet points aligned to the job.
   - **Data Extraction**: Extracts the **company name** and **job title** from the job description.
   - **Interview Insights**:
     - Gathers company- and position-specific interview information using SERP API.
     - Analyzes information with GPT models for useful insights.

### 3. Output of Results
The results include:
   - Validation messages for resume and job description.
   - Compatibility analysis output.
   - Targeted suggestions to improve resume alignment.
   - Example resume bullet points generated for the job description.
   - Interview preparation data for the extracted company and job title.

---

## Running the Application

### Option 1: Flask API

Start the Flask server:
```bash
export FLASK_APP=app/main.py                # On macOS or Linux
set FLASK_APP=app\main.py                   # On Windows
flask run
```

The Flask API will run on `http://127.0.0.1:5000/`.

Key endpoints include:
- **POST /api/resume/upload**:  
   Accepts `file` (resume) and `job_description` as part of form data. Returns analysis results.

Example cURL command:
```bash
curl -X POST -F "file=@path/to/resume.pdf" -F "job_description=Job description text" http://127.0.0.1:5000/api/resume/upload
```

### Option 2: Streamlit

Run the Streamlit app:
```bash
streamlit run app/main.py
```

Steps:
1. Enter your OpenAI and SERP API keys directly in the UI.
2. Upload your resume (PDF or DOCX).
3. Add the job description text.
4. Hit "Generate Suggestions" to view results interactively.

---

## Example API Response

**Success**:
```json
{
    "message": "Resume analyzed successfully",
    "results": {
        "validation_results": "Inputs are valid.",
        "analysis": {
            "compatibility_evaluation": "High compatibility",
            "suggestions": "Add more leadership skills in your resume.",
            "bullet_points": [
                "Implemented a cost-saving strategy reducing expenses by 15%.",
                "Managed a team to achieve 200% of quarterly objectives."
            ]
        },
        "interview_insights": "Prepare for behavioral questions focusing on teamwork."
    }
}
```

**Error**:
```json
{
    "error": "Job description is required."
}
```

---

## Future Enhancements

- Enhance job-specific keyword extraction for better alignment.
- Add scoring visualization for compatibility reports.
- Improve algorithms for generating tailored bullet points and interview resources.
- Expand support for additional resume file formats like `.txt`.

---

Feel free to contribute or report issues via the [GitHub Repository](https://github.com/dalbosta/ResumeTailor).