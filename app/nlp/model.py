from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from .prompt_templates import (
    COMPATIBILITY_TEMPLATE,
    SUGGESTIONS_TEMPLATE,
    BULLET_POINTS_TEMPLATE,
    VALIDATE_AND_EVALUATE_RESUME,
    VALIDATE_AND_EVALUATE_JOB_DESCRIPTION,
)

# Constants
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0


def create_llm_client(api_key, model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE):
    """
    Create an instance of an LLM client using LangChain's updated ChatOpenAI.
    """
    return ChatOpenAI(
        openai_api_key=api_key,
        model_name=model,
        temperature=temperature)


def create_chain(client, template, input_variables):
    """
    Create a sequence chain using PromptTemplate connected to an LLM.
    """
    # Create a PromptTemplate
    prompt = PromptTemplate(template=template, input_variables=input_variables)

    # Combine the prompt with the client using the pipe operator (|)
    return prompt | client




def validate_input(client, resume_text, job_description):
    """
    Validate the resume and job description inputs and return validation results.
    """
    # Create validation chains
    resume_validation_chain = create_chain(
        client, VALIDATE_AND_EVALUATE_RESUME, ["resume_text"]
    )
    job_description_validation_chain = create_chain(
        client, VALIDATE_AND_EVALUATE_JOB_DESCRIPTION, ["job_description"]
    )

    # Run validation chains
    resume_validation_result = resume_validation_chain.invoke({"resume_text": resume_text}).content.strip()
    job_description_validation_result = job_description_validation_chain.invoke(
        {"job_description": job_description}).content.strip()

    # Parse validation results
    resume_validity, resume_sufficiency = parse_validation_result(resume_validation_result)
    job_description_validity, job_description_sufficiency = parse_validation_result(job_description_validation_result)

    # Collect errors
    errors = check_validation_errors(
        resume_validity,
        resume_sufficiency,
        job_description_validity,
        job_description_sufficiency,
    )
    return errors



def check_validation_errors(
        resume_validity, resume_sufficiency, job_description_validity, job_description_sufficiency
):
    """
    Collect and return validation errors for resume and job description inputs.
    """
    errors = []

    if resume_validity == "No":
        errors.append(f"Invalid Resume: {resume_sufficiency}")
    elif resume_sufficiency == "Insufficient":
        errors.append(f"Insufficient Resume: {resume_sufficiency}")

    if job_description_validity == "No":
        errors.append(f"Invalid Job Description: {job_description_sufficiency}")
    elif job_description_sufficiency == "Insufficient":
        errors.append(
            f"Insufficient Job Description: {job_description_sufficiency}"
        )

    return errors


def run_analysis(client, resume_text, job_description):
    """
    Perform analysis for compatibility, improvement suggestions, and bullet points.
    """
    # Create analysis chains as RunnableSequences
    compatibility_chain = create_chain(
        client, COMPATIBILITY_TEMPLATE, ["resume_text", "job_description"]
    )
    suggestions_chain = create_chain(
        client, SUGGESTIONS_TEMPLATE, ["resume_text", "job_description"]
    )
    bullet_points_chain = create_chain(
        client, BULLET_POINTS_TEMPLATE, ["job_description"]
    )

    # Run chains and collect results
    compatibility_evaluation = compatibility_chain.invoke(
        {"resume_text": resume_text, "job_description": job_description}).content.strip()
    suggestions = suggestions_chain.invoke(
        {"resume_text": resume_text, "job_description": job_description}).content.strip()
    bullet_points = bullet_points_chain.invoke({"job_description": job_description}).content.strip()

    return {
        "compatibility_evaluation": compatibility_evaluation,
        "suggestions": suggestions,
        "bullet_points": bullet_points,
    }



def parse_validation_result(validation_result):
    """
    Parse the validation result to extract validity and sufficiency status.
    Handles unexpected formats to prevent crashes.
    """
    try:
        # Clean up the input to remove trailing or extraneous whitespace/periods
        validation_result = validation_result.strip().rstrip(".")
        # Split result into lines
        lines = [line.strip() for line in validation_result.splitlines() if line.strip()]
        if len(lines) < 2:
            raise ValueError("Validation result must contain at least two lines.")
        if ":" not in lines[0] or ":" not in lines[1]:
            raise ValueError("Validation result lines must contain ':'")

        # Parse validity and sufficiency
        validity = lines[0].split(":", 1)[1].strip().split(" - ")
        sufficiency = lines[1].split(":", 1)[1].strip().split(" - ")

        return validity[0], sufficiency[1]

    except Exception as e:
        raise ValueError(f"Failed to parse validation result: {validation_result}. Error: {e}")


def generate_resume_suggestions_with_key(resume_text, job_description, user_openai_api_key):
    """
    Validate and evaluate inputs (resume and job description) before proceeding with comparison and suggestions.
    """
    # Create LLM client
    llm_client = create_llm_client(user_openai_api_key)

    # Validate inputs
    errors = validate_input(llm_client, resume_text, job_description)
    if errors:
        return {"error": "Validation failed for one or both inputs.", "details": errors}

    # Run analysis
    return run_analysis(llm_client, resume_text, job_description)
