from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from api_keys.keys import OPENAI_API_KEY

from .templates import COMPATIBILITY_TEMPLATE, SUGGESTIONS_TEMPLATE, BULLET_POINTS_TEMPLATE


def generate_resume_suggestions(resume_text, job_description):
    """
    Analyze the compatibility between resume and job description,
    provide improvement suggestions, and generate example bullet points.

    :param resume_text: Extracted text from the resume.
    :param job_description: Text of the job description.
    :return: Dictionary containing compatibility evaluation, suggestions, and bullet points.
    """

    # Initialize the OpenAI client
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    # Define template-based chains using imported templates
    compatibility_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=COMPATIBILITY_TEMPLATE, input_variables=["resume_text", "job_description"])
    )

    suggestions_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=SUGGESTIONS_TEMPLATE, input_variables=["resume_text", "job_description"])
    )

    bullet_points_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=BULLET_POINTS_TEMPLATE, input_variables=["job_description"])
    )

    # Call the chains in sequence
    compatibility_evaluation = compatibility_chain.run({
        "resume_text": resume_text,
        "job_description": job_description
    }).strip()

    suggestions = suggestions_chain.run({
        "resume_text": resume_text,
        "job_description": job_description
    }).strip()

    bullet_points = bullet_points_chain.run({
        "job_description": job_description
    }).strip()

    # Return the results in the expected format
    return {
        "compatibility_evaluation": compatibility_evaluation,
        "suggestions": suggestions,
        "bullet_points": bullet_points
    }


def generate_resume_suggestions_with_key(resume_text, job_description, user_api_key):
    """
    A version of `generate_resume_suggestions` that dynamically accepts a user-provided OpenAI API key.

    :param resume_text: Extracted text from a resume.
    :param job_description: Text of the job description.
    :param user_api_key: The OpenAI API key provided by the user.
    :return: A dictionary containing compatibility evaluation, improvement suggestions, and bullet points.
    """
    # Initialize the OpenAI client with the user's API key
    client = OpenAI(temperature=0, openai_api_key=user_api_key)

    # Chains using imported templates
    compatibility_chain = LLMChain(
        llm=client,
        prompt=PromptTemplate(template=COMPATIBILITY_TEMPLATE, input_variables=["resume_text", "job_description"])
    )

    suggestions_chain = LLMChain(
        llm=client,
        prompt=PromptTemplate(template=SUGGESTIONS_TEMPLATE, input_variables=["resume_text", "job_description"])
    )

    bullet_points_chain = LLMChain(
        llm=client,
        prompt=PromptTemplate(template=BULLET_POINTS_TEMPLATE, input_variables=["job_description"])
    )

    # Execute the chains
    compatibility_evaluation = compatibility_chain.run({
        "resume_text": resume_text,
        "job_description": job_description
    }).strip()

    suggestions = suggestions_chain.run({
        "resume_text": resume_text,
        "job_description": job_description
    }).strip()

    bullet_points = bullet_points_chain.run({
        "job_description": job_description
    }).strip()

    return {
        "compatibility_evaluation": compatibility_evaluation,
        "suggestions": suggestions,
        "bullet_points": bullet_points
    }
