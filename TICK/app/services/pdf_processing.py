from fastapi import HTTPException
import PyPDF2


def summarize_text(client, messages):
    """
    Summarize the chunk of text using OpenAI's chat-based API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while summarizing text: {str(e)}")


def load_pdf_pages(client, pdf_file):
    """
    Load all pages from a PDF and return a list of text from each page.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pages = [pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))]
        return pages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while reading PDF: {str(e)}")


def generate_mcq_from_summary(mcqs_text):
    """
    Parses the summary to extract MCQs. Expects standard formatting.
    """
    try:
        questions = []
        options = []
        correct_answers = []

        lines = mcqs_text.strip().split("\n")

        question = ""
        option_a = ""
        option_b = ""
        option_c = ""
        option_d = ""
        correct_answer = None

        for line in lines:
            if line.startswith("Q"):
                if question:
                    questions.append(question)
                    options.append([option_a, option_b, option_c, option_d])
                    correct_answers.append(correct_answer)

                question = line.strip()
                option_a = option_b = option_c = option_d = ""
                correct_answer = None

            elif line.startswith("a)"):
                option_a = line.strip()
            elif line.startswith("b)"):
                option_b = line.strip()
            elif line.startswith("c)"):
                option_c = line.strip()
            elif line.startswith("d)"):
                option_d = line.strip()
            elif "Correct answer:" in line:
                correct_answer = line.split(":")[-1].strip().lower()[0]

        if question:
            questions.append(question)
            options.append([option_a, option_b, option_c, option_d])
            correct_answers.append(correct_answer)

        if not questions or not options or not correct_answers:
            raise ValueError("Summary does not contain valid questions, options, or answers.")

        return questions, options, correct_answers

    except Exception as e:
        raise ValueError(f"Error parsing MCQ: {mcqs_text}")
