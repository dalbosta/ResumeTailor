# templates.py

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
