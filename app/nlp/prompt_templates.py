# prompt_templates.py

# Validate and Evaluate Resume Template
VALIDATE_AND_EVALUATE_RESUME = """
Evaluate the following text to determine if it is a valid resume and contains sufficient information for meaningful comparison.

Criteria:
1. Valid Resume: Should include essential sections, such as experience, education, and skills. Partial validity can apply if key sections (e.g., experience) are present but others (e.g., skills) are missing.
2. Sufficient Information: Should explicitly state key qualifications, roles, achievements, or other details relevant for assessing compatibility with a job description.
3. Structure: The resume should be correctly formatted with clearly identifiable sections for easier evaluation.

Text (Resume):
{resume_text}

Response Format:
1. Resume Validity: [Yes/Partial/No] - [Reason or Missing Elements]
2. Resume Sufficiency: [Sufficient/Insufficient] - [Reason or Missing Elements]
3. Structural Issues: [Yes/No] - [Reason or Suggestions for Improvement]

Focus on identifying specific areas lacking validity, sufficiency, or structure, avoiding redundant sentences.
"""

# Validate and Evaluate Job Description Template
VALIDATE_AND_EVALUATE_JOB_DESCRIPTION = """
Evaluate the following text to determine if it is a valid job description and contains sufficient information for meaningful comparison.

Criteria:
1. Valid Job Description: Should clearly describe responsibilities, qualifications, required skills, and expectations for the role. Industry-specific terms or qualifications should be present when relevant.
2. Sufficient Information: Should include specific details describing the role's key requirements, tasks, and qualifications.
3. Clarity: The job description should be understandable, concise, and avoid ambiguity. Major omissions (like missing qualifications) should be clarified.

Text (Job Description):
{job_description}

Response Format:
1. Job Description Validity: [Yes/No] - [Reason or Missing Elements]
2. Job Description Sufficiency: [Sufficient/Partially Insufficient/Insufficient] - [Reason or Missing Elements]
3. Clarity Issues: [Yes/No] - [Reason or Suggestions for Improvement]

Focus your response on identifying missing sections, insufficient data, or unclear phrasing while avoiding repetitive or generic feedback.
"""


# Compatibility Evaluation Template
COMPATIBILITY_TEMPLATE = """
Evaluate the compatibility between the given resume and job description on a scale from 1 to 10, considering explicit and transferable alignments.

Criteria:
1. Direct Alignment: Assess how well the resume matches the explicit requirements, qualifications, and skills listed in the job description.
2. Transferable Skills: Identify skills or experiences that, while not explicitly listed, are relevant based on the job's industry, domain, or context.
3. Structural Issues: Consider if the resume's organization, clarity, or length impacts compatibility.

Resume:
{resume_text}

Job Description:
{job_description}

Response Format:
1. Compatibility Score: [1-10] \n [Specific reasoning for the score]
2. Strengths: [Resume elements that align, directly or implicitly, with the job requirements]
3. Weaknesses: [Specific gaps, misalignments, or structural issues hindering compatibility]
"""

# Improvement Suggestions Template
SUGGESTIONS_TEMPLATE = """
Provide actionable and specific suggestions on improving the following resume to better align it with the given job description.

Criteria:
1. Prioritize High-Impact Changes: Focus on adjustments that address key misalignments between the resume and job description requirements (e.g., missing skills or experiences).
2. Include Meta-Role Suggestions: Add broad recommendations on tailoring the resume format (e.g., switching to a technical or managerial tone) if relevant.
3. Avoid Redundant Suggestions: Do not recommend changes for areas where the resume is already aligned.

Resume:
{resume_text}

Job Description:
{job_description}

Response Format:
Actionable Suggestions:
1. [Suggestion 1] - [Reason tied to job description]
2. [Suggestion 2] - [Reason tied to job description]
3. [Meta Suggestion, if applicable] - [Reason to shift focus]
"""

# Example Bullet Points Template
BULLET_POINTS_TEMPLATE = """
Based on the following job description, generate three concise, result-oriented resume bullet points. These should align directly with the key skills, responsibilities, and qualifications listed in the job description.

Criteria:
1. Use Quantitative Language: Include measurable outcomes wherever possible (e.g., "Increased sales by 20%").
2. Use Contextual Phrasing: When metrics are unavailable, highlight actions or processes achieved within the role's context using impactful language (e.g., "Organized team projects to improve efficiency").
3. Ensure Relevance: Each point must explicitly align with or support a key job requirement.

Job Description:
{job_description}

Response Format:
- [Bullet Point 1: Action - Impact - Result]
- [Bullet Point 2: Action - Impact - Result]
- [Bullet Point 3: Action - Impact - Result]
"""

# Search and Analyze Interview Process Template
SEARCH_INTERVIEW_INFO_TEMPLATE = """
You are an AI assistant helping job applicants prepare for job interviews. From the search results provided below, summarize specific and actionable insights related to the company and job role:

1. List up to 5 known interview questions for the job. If no questions are available, explicitly state: "No interview questions found."
2. Indicate the typical number of interview rounds and their types (e.g., technical, behavioral, or HR). If unavailable, state: "No information found."
3. Summarize key applicant insights or experiences, focusing on trends, tips, or challenges applicants encountered.

Ensure all insights are concise, organized, and directly relevant to interview preparation.

Company: {company_name}
Job Title: {job_title}

Search Results:
{search_results}

Response Format:
1. Known Questions: [List questions or state "No interview questions found."]
2. Number of Rounds: [Number and type of rounds or "No information found."]
3. Key Insights: [Summary of applicant experiences or challenges.]
"""

# Extract Company Name and Job Title Template
EXTRACT_COMPANY_AND_OCCUPATION_TEMPLATE = """
Extract the company name and job title from the following job description text.

Guidelines:
1. If the company name or job title cannot be explicitly identified, return "Unknown" for the relevant field.
2. Handle ambiguous cases carefully by considering textual context, but do not guess. Clarify potential ambiguities when possible.
3. Suggest corrections or clarifications for unclear job descriptions if feasible (e.g., "Rephrase to specify the exact company name.").

Job Description:
{job_description}

Response Format:
Company Name: [Company Name or Unknown]
Job Title: [Job Title or Unknown]
Clarifications (if applicable): [Suggestions or clarifications]
"""


