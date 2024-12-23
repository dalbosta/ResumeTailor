# ResumeTailor: A Resume Optimization and Job Matching Tool

**ResumeTailor** is a tool that leverages AI to improve your resume by analyzing it against a provided job description. The application extracts key information from resumes, validates inputs, and generates actionable suggestions, ensuring compatibility with your target job. It can also provide example bullet points that align with the job description using OpenAI's API.

This project can be run as either a **Flask** app (for REST API-based interactions) or a **Streamlit** app (for a web interface), making it highly versatile.

---

## Features

1. **Validate Job Descriptions and Resumes:**
   Ensures both job descriptions and resumes meet the required standards by checking content validity and sufficiency.

2. **Input Analysis:**
   Evaluates the compatibility between a resume and a job description.

3. **Suggestions for Improvement:**
   Provides actionable suggestions to improve your resume so it aligns better with the target job.

4. **Example Resume Bullet Points:**
   Suggests well-constructed, result-oriented resume bullet points based on the job description.

5. **Simple Text Extraction:**
   Supports parsing and text extraction from **PDF** and **DOCX** files, with backup OCR for non-text PDFs.

---

## Requirements

To run the project, you need the following:

1. **Python version:** >= 3.13.1  
2. **Dependencies:**
   Ensure the required Python libraries are installed. These include:
   - `Flask` - For API-based interactions.
   - `Streamlit` - For the web interface.
   - `Werkzeug` - For file handling in Flask.
   - `numpy` & `pandas` - For data processing support.
   - `PyPDF2` & `pdf2image` - For PDF text parsing and OCR extraction.
   - `pytesseract` - For OCR support.
   - `docx` - For extracting text from Word files.
   - `LangChain` packages - For LLM (Large Language Model) integrations.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dalbosta/ResumeTailor.git
   cd ResumeTailor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS or Linux
   venv\Scripts\activate           # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Tesseract OCR is installed (for parsing image-based PDFs).  
   Follow installation instructions for your operating system [here](https://github.com/tesseract-ocr/tesseract).

5. Set up the environment:  
   Create a `.env` file or set the `OPENAI_API_KEY` environment variable containing your OpenAI API Key.

---

## Running the Application

### Option 1: As a Flask App
1. Start the Flask server:
   ```bash
   export FLASK_APP=app/main.py                # On macOS or Linux
   set FLASK_APP=app\main.py                   # On Windows
   flask run
   ```

2. The app will run on `http://127.0.0.1:5000/`.

3. Available routes:
   - **`GET /`**: Home route.
   - **`GET /about`**: About route.
   - **`POST /api/analyze`**: Accepts JSON input (resume text and job description) to process using OpenAI.

### Option 2: As a Streamlit App
1. Run the Streamlit app:
   ```bash
   streamlit run app_streamlit/app.py
   ```

2. Open the URL displayed in the terminal (typically **http://localhost:8501**).

3. Steps in the Streamlit interface:
   - Enter your OpenAI API key (it is **not stored**).
   - Upload your resume (PDF or DOCX format only).
   - Paste the job description.
   - Click "Generate Suggestions" to see results.


---

## How It Works

### 1. Resume Parsing
The app accepts **PDF** and **DOCX** resumes. If the file contains no text (e.g., scanned PDFs), it uses OCR with `pytesseract` to extract text from images.

### 2. Validation
Prompts such as **VALIDATE_AND_EVALUATE_RESUME** and **VALIDATE_AND_EVALUATE_JOB_DESCRIPTION** analyze the quality of the input data, ensuring it is sufficient for further processing.

### 3. Compatibility Analysis
The app uses Large Language Models (like OpenAI's GPT) to analyze the compatibility between the resume and the job description. It provides:
   - A compatibility score.
   - Specific strengths and weaknesses.

### 4. Suggestions and Bullet Points
The app suggests ways to improve your resume to better match the target job. It also generates example bullet points tailored to the job description.

---

## Example Workflow in Streamlit

1. User uploads a resume (**resume.pdf**).
2. App extracts text using `parse_resume`.
3. User pastes the job description into a text box in Streamlit.
4. When the user clicks "Generate Suggestions":
   - Resume and job description are validated.
   - Inputs are analyzed by OpenAI's API.
   - Suggestions and compatibility results are displayed in the interface.

---

## API Usage via Flask

### Endpoint: `/api/analyze`

#### Request:
```json
{
   "resume": "Cleaned resume text from the user",
   "job_description": "Given job description for analysis"
}
```

#### Response:
```json
{
   "compatibility_evaluation": "Output from OpenAI LLM",
   "suggestions": "Suggestions for improving the resume",
   "bullet_points": ["Point 1", "Point 2", "Point 3"]
}
```

---

## Notes and Tips

1. **Customizability:**  
   Update the `templates.py` file to use custom prompts tailored to niche industries or specific job roles.

2. **Tesseract OCR Settings:**  
   Ensure Tesseract's `tesseract` binary is correctly configured in your system's PATH for OCR processing of image-based PDFs.

3. **Environment Variables:**  
   For production environments, securely manage the `OPENAI_API_KEY` using `.env` files or cloud secrets.

---

## Future Enhancements

- Expand support for additional file formats (e.g., `.txt` resumes).
- Introduce a scoring report visualization in Streamlit.
- Implement job-specific keyword extraction for resume tailoring.
- Implement websearch tools for LLM to find relevant info regarding interviews for given occupation and company

---

Feel free to contribute or report issues in the [GitHub Repository](https://github.com/dalbosta/ResumeTailor).

