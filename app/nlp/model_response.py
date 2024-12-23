from langchain_community.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from .templates import COMPATIBILITY_TEMPLATE, SUGGESTIONS_TEMPLATE, BULLET_POINTS_TEMPLATE

def generate_resume_suggestions_with_key(resume_text, job_description, user_api_key):
    """
    A version of `generate_resume_suggestions` that dynamically accepts a user-provided OpenAI API key.
    """
    # Use ChatOpenAI with a valid model
    client = ChatOpenAI(
        openai_api_key=user_api_key,
        model="gpt-4o",  # Replace gpt-4o with a valid model
        temperature=0
    )

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
