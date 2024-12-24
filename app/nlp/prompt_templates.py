# prompt_templates.py

# Validate and Evaluate Resume Template
VALIDATE_AND_EVALUATE_RESUME = """
Determine if the following text represents a valid resume and contains sufficient information for meaningful comparison:
1. A valid resume should include sections such as experience, education, skills, or similar categories.
2. Sufficient information means key qualifications, experiences, or accomplishments are present.

Resume:
{resume_text}

Return your evaluation in the following format:
1. Resume Validity: [Yes/No] - [Explanation]
2. Resume Sufficiency: [Sufficient/Insufficient] - [Explanation]
"""

# Validate and Evaluate Job Description Template
VALIDATE_AND_EVALUATE_JOB_DESCRIPTION = """
Determine if the following text represents a valid job description and contains sufficient information for meaningful comparison:
1. A valid job description should include responsibilities, qualifications, or expectations.
2. Sufficient information means the job's key requirements, responsibilities, or expectations are clearly stated.

Job Description:
{job_description}

Return your evaluation in the following format:
1. Job Description Validity: [Yes/No] - [Explanation]
2. Job Description Sufficiency: [Sufficient/Insufficient] - [Explanation]
"""


# Compatibility Evaluation Template
COMPATIBILITY_TEMPLATE = """
Evaluate the compatibility between the following resume and job description on a scale from 1 to 10, 
and provide specific strengths and weaknesses.

Resume:
{resume_text}

Job Description:
{job_description}
"""

# Improvement Suggestions Template
SUGGESTIONS_TEMPLATE = """
Provide actionable suggestions on how the resume can be improved to align better with the following job description:

Resume:
{resume_text}

Job Description:
{job_description}
"""

# Example Bullet Points Template
BULLET_POINTS_TEMPLATE = """
Based on the following job description, generate three formatted and result-oriented resume bullet points 
to enhance the provided resume. Use professional language.

Job Description:
{job_description}
"""
