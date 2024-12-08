# app/nlp/resume_suggestion.py

import openai

# Initialize with your OpenAI API key
openai.api_key = 'your-api-key-here'  # Replace with your actual key


def generate_job_suggestions(resume_text, job_description_text):
    """
    Generates job suggestions based on resume and job description text.

    :param resume_text: A string containing the text of the resume.
    :param job_description_text: A string containing the text of the job description.
    :return: A string containing the generated job suggestions.
    """
    # Prepare inputs for the model
    prompt = (f"Given the following resume text:\n{resume_text}\n\n"
              f"And the following job description text:\n{job_description_text}\n\n"
              "Suggest how well the resume fits the job description. "
              "Provide any relevant suggestions to tailor his resume to increase chances of getting an interview.")

    try:
        # Interact with GPT model
        response = openai.Completion.create(
            engine="text-davinci-003",  # Specify the correct engine
            prompt=prompt,
            max_tokens=150  # Adjust tokens based on response length needs
        )

        suggestions = response.choices[0].text.strip()
        return suggestions
    except Exception as e:
        return f"An error occurred: {e}"

# Usage example (would be outside of this module):
# resume = "Text from the resume"
# job_description = "Text from the job description"
# print(generate_job_suggestions(resume, job_description))
