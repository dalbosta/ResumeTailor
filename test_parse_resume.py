# test_parse_resume.py

from app.nlp.resume_parser import parse_resume


def test_parse_resume():
    # Specify the path to your resume file
    file_path = r'C:\Users\derek\PycharmProjects\ResumeTailor\data\ALBOSTA_RESUME_24.pdf'  # Change to your actual file name and extension

    # Call the parse_resume function
    try:
        resume_text = parse_resume(file_path)
        print("Parsed resume text:\n", resume_text)
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    test_parse_resume()
