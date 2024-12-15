from openai import OpenAI
from secrets import OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY  # Ensure the API key is set correctly
)


def generate_resume_suggestions(resume_text, job_description_text):
    """
    Generates resume suggestions based on resume and job description text.

    :param resume_text: A string containing the text of the resume.
    :param job_description_text: A string containing the text of the job description.
    :return: A string containing the generated job suggestions.
    """
    # Prepare inputs for the model
    prompt = (f"Given the following resume text:\n{resume_text}\n\n"
              f"And the following job description text:\n{job_description_text}\n\n"
              "Suggest how well the resume fits the job description. "
              "Provide any relevant suggestions to tailor the resume to increase chances of getting an interview.")

    try:
        # Use the OpenAI client to call the chat.completions API
        chat_completion = client.chat.completions.create(
            model="gpt-4o",  # Replace with the model version you intend to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides resume suggestions."},
                {"role": "user", "content": prompt}
            ]
        )

        # Access the message content directly using dot notation
        suggestions = chat_completion.choices[0].message.content.strip()
        return suggestions
    except Exception as e:
        return f"An error occurred: {e}"
