from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from secrets import OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY  # Ensure the API key is set correctly
)


def generate_resume_suggestions(resume_text, job_description_text):
    """
    Analyze the compatibility between resume and job description,
    provide improvement suggestions, and generate example bullet points.

    :param resume_text: Extracted text from the resume.
    :param job_description_text: Text of the job description.
    :return: Dictionary containing compatibility evaluation, suggestions, and bullet points.
    """

    # Initialize the OpenAI client (LangChain LLM)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    # Define template and chain for compatibility evaluation
    compatibility_template = """
    Evaluate the compatibility between the following resume and job description on a scale from 1 to 10, 
    and provide specific strengths and weaknesses.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    compatibility_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=compatibility_template, input_variables=["resume_text", "job_description"])
    )

    # Define template and chain for improvement suggestions
    suggestions_template = """
    Provide actionable suggestions on how the resume can be improved to align better with the following job description:

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    suggestions_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=suggestions_template, input_variables=["resume_text", "job_description"])
    )

    # Define template and chain for example bullet points
    bullet_points_template = """
    Based on the following job description, generate three formatted and result-oriented resume bullet points 
    to enhance the provided resume. Use professional language.

    Job Description:
    {job_description}
    """

    bullet_points_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=bullet_points_template, input_variables=["job_description"])
    )

    # Call the chains in sequence
    compatibility_evaluation = compatibility_chain.run({
        "resume_text": resume_text,
        "job_description": job_description_text
    }).strip()

    suggestions = suggestions_chain.run({
        "resume_text": resume_text,
        "job_description": job_description_text
    }).strip()

    bullet_points = bullet_points_chain.run({
        "job_description": job_description_text
    }).strip()

    # Return the results in the expected format
    return {
        "compatibility_evaluation": compatibility_evaluation,
        "suggestions": suggestions,
        "bullet_points": bullet_points
    }
