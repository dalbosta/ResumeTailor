from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import requests

from .prompt_templates import (
    COMPATIBILITY_TEMPLATE,
    SUGGESTIONS_TEMPLATE,
    BULLET_POINTS_TEMPLATE,
    VALIDATE_AND_EVALUATE_RESUME,
    VALIDATE_AND_EVALUATE_JOB_DESCRIPTION,
    SEARCH_INTERVIEW_INFO_TEMPLATE, EXTRACT_COMPANY_AND_OCCUPATION_TEMPLATE,
)

# Constants
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0
SERP_API_URL = "https://serpapi.com/search.json"


class LLMHelper:
    """
    Encapsulates logic for creating and interacting with the LLM.
    """

    def __init__(self, api_key, model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE):
        self.client = ChatOpenAI(
            openai_api_key=api_key,
            model_name=model,
            temperature=temperature
        )

    def create_chain(self, template, input_variables):
        """
        Create a reusable prompt chain for the LLM.
        """
        prompt = PromptTemplate(template=template, input_variables=input_variables)
        return prompt | self.client

    def invoke_chain(self, chain, **inputs):
        """
        Invoke a chain and return the result content.
        """
        return chain.invoke(inputs).content.strip()

    def extract_company_and_job_title(self, job_description):
        """
        Extract the company name and job title from the job description.
        """
        chain = self.create_chain(EXTRACT_COMPANY_AND_OCCUPATION_TEMPLATE, ["job_description"])
        result = self.invoke_chain(chain, job_description=job_description)

        # Parse result
        try:
            lines = result.splitlines()
            company_name = lines[0].split(":")[1].strip()
            job_title = lines[1].split(":")[1].strip()
        except Exception as e:
            raise ValueError(f"Failed to parse extraction result: {result}. Error: {e}")

        return company_name, job_title


class ValidationService:
    """
    Handles validation logic for the resume and job description.
    """

    def __init__(self, llm_helper):
        self.llm_helper = llm_helper

    def validate(self, resume_text, job_description):
        """
        Runs validation for both resume and job description.
        """
        resume_chain = self.llm_helper.create_chain(
            VALIDATE_AND_EVALUATE_RESUME, ["resume_text"]
        )
        job_chain = self.llm_helper.create_chain(
            VALIDATE_AND_EVALUATE_JOB_DESCRIPTION, ["job_description"]
        )

        # Run the validation chains
        resume_result = self.llm_helper.invoke_chain(resume_chain, resume_text=resume_text)
        job_result = self.llm_helper.invoke_chain(job_chain, job_description=job_description)

        # Parse results and collect errors
        resume_validity, resume_sufficiency = self._parse_validation_result(resume_result)
        job_validity, job_sufficiency = self._parse_validation_result(job_result)
        errors = self._collect_errors(resume_validity, resume_sufficiency, job_validity, job_sufficiency)

        return errors

    @staticmethod
    def _parse_validation_result(validation_result):
        """
        Parses validity and sufficiency status from a validation result string.
        """
        try:
            lines = [line.strip() for line in validation_result.splitlines() if line.strip()]
            validity = lines[0].split(":")[1].strip().split(" - ")
            sufficiency = lines[1].split(":")[1].strip().split(" - ")
            return validity[0], sufficiency[1]
        except Exception as e:
            raise ValueError(f"Failed to parse validation result: {validation_result}. Error: {e}")

    @staticmethod
    def _collect_errors(resume_validity, resume_sufficiency, job_validity, job_sufficiency):
        """
        Collect and return validation errors for both inputs.
        """
        errors = []
        if resume_validity == "No":
            errors.append(f"Invalid Resume: {resume_sufficiency}")
        elif resume_sufficiency == "Insufficient":
            errors.append(f"Insufficient Resume: {resume_sufficiency}")

        if job_validity == "No":
            errors.append(f"Invalid Job Description: {job_sufficiency}")
        elif job_sufficiency == "Insufficient":
            errors.append(f"Insufficient Job Description: {job_sufficiency}")

        return errors


class AnalysisService:
    """
    Handles compatibility evaluation, suggestions, and bullet point generation.
    """

    def __init__(self, llm_helper):
        self.llm_helper = llm_helper

    def analyze(self, resume_text, job_description):
        """
        Perform compatibility evaluation, suggestions, and bullet point generation.
        """
        compatibility_chain = self.llm_helper.create_chain(
            COMPATIBILITY_TEMPLATE, ["resume_text", "job_description"]
        )
        suggestions_chain = self.llm_helper.create_chain(
            SUGGESTIONS_TEMPLATE, ["resume_text", "job_description"]
        )
        bullet_points_chain = self.llm_helper.create_chain(
            BULLET_POINTS_TEMPLATE, ["job_description"]
        )

        # Run the chains
        compatibility = self.llm_helper.invoke_chain(
            compatibility_chain, resume_text=resume_text, job_description=job_description
        )
        suggestions = self.llm_helper.invoke_chain(
            suggestions_chain, resume_text=resume_text, job_description=job_description
        )
        bullet_points = self.llm_helper.invoke_chain(
            bullet_points_chain, job_description=job_description
        )

        return {
            "compatibility_evaluation": compatibility,
            "suggestions": suggestions,
            "bullet_points": bullet_points,
        }


class InterviewResearchService:
    """
    Handles retrieving and analyzing interview-related information using SERP API and LLM.
    """

    def __init__(self, llm_helper, serp_api_key):
        self.llm_helper = llm_helper
        self.serp_api_key = serp_api_key

    def search_interview_info(self, company_name, job_title):
        """
        Use the SERP API to fetch interview-related information.
        """
        query = f"{company_name} {job_title} interview process questions experiences"
        params = {
            "q": query,
            "key": self.serp_api_key,
            "num": 10
        }
        response = requests.get(SERP_API_URL, params=params)
        if response.status_code == 200:
            return response.json().get("organic_results", [])
        else:
            raise ValueError(f"SERP API failed with status code: {response.status_code}")

    def parse_search_results(self, search_results):
        """
        Formats SERP API results for an LLM prompt.
        """
        if not search_results:
            return "No relevant search results found."
        return "\n\n".join(
            f"Result {i + 1}: {r.get('title', 'No title')}\nSnippet: {r.get('snippet', 'No snippet')}\nURL: {r.get('link', 'No link')}"
            for i, r in enumerate(search_results)
        )

    def analyze_interview_data(self, company_name, job_title, search_results):
        """
        Analyze SERP search results using LLM for interview insights.
        """
        formatted_results = self.parse_search_results(search_results)

        chain = self.llm_helper.create_chain(
            SEARCH_INTERVIEW_INFO_TEMPLATE, ["company_name", "job_title", "search_results"]
        )
        return self.llm_helper.invoke_chain(
            chain, company_name=company_name, job_title=job_title, search_results=formatted_results
        )


def run_full_analysis(resume_text, job_description, serp_api_key, openai_api_key):
    """
    Combines validation, compatibility analysis, and interview research into a single workflow.
    """
    llm_helper = LLMHelper(api_key=openai_api_key)
    validation_service = ValidationService(llm_helper)
    analysis_service = AnalysisService(llm_helper)
    interview_service = InterviewResearchService(llm_helper, serp_api_key)

    # Step 1: Validate inputs
    errors = validation_service.validate(resume_text, job_description)
    if errors:
        return {"error": "Validation failed for one or both inputs.", "details": errors}

    # Step 2: Analyze resume-job description compatibility
    analysis_results = analysis_service.analyze(resume_text, job_description)

    # Step 3: Extract company name and job title
    print("Extracting company name and job title from the job description...")
    try:
        company_name, job_title = llm_helper.extract_company_and_job_title(job_description)
        if company_name == "Unknown" or job_title == "Unknown":
            raise ValueError("Failed to extract company name or job title from the job description.")
    except Exception as e:
        return {"error": "Extraction failed.", "details": str(e)}
    print(f"Extracted Company Name: {company_name}, Job Title: {job_title}")

    # Step 4: Search and analyze interview insights
    search_results = interview_service.search_interview_info(company_name, job_title)
    interview_insights = interview_service.analyze_interview_data(company_name, job_title, search_results)

    return {
        "validation_results": "Valid inputs.",
        "analysis": analysis_results,
        "interview_insights": interview_insights,
    }
