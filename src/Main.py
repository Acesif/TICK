import PyPDF2
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)

def chunk_text(text, chunk_size=2000):
    """
    Split text into manageable chunks based on chunk_size to avoid token limits.
    """
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def summarize_text(text_chunk):
    """
    Summarize the chunk of text using OpenAI's chat-based API.
    """
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful school teacher."},
            {"role": "user", "content": f"Explain this in great detail: {text_chunk}"}
        ]
    )
    return response.choices[0].message.content

def summarize_pdf(pdf_path):
    pdf_file = open(pdf_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    full_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        full_text += page_text

    chunks = chunk_text(full_text)

    summaries = []
    for chunk in chunks:
        summary = summarize_text(chunk)
        summaries.append(summary)
    return summaries


def ask_question(context, question):
    """
    Allow the user to ask questions based on the context (PDF summary).
    """

    conversation_history = [
        {
            "role": "system",
            "content":
            """
                You are a helpful school teacher. 
                Answer as if you are explaining it to a 15 year old but only based on the provided content of the PDF.
                Do not include any outside knowledge. If the question is outside the PDF's context, inform the user that you cannot answer.
            """
            # Do not include any outside knowledge. If the question is outside the PDF's context, inform the user that you cannot answer.
        }
    ]
    for summary in context:
        conversation_history.append({"role": "assistant", "content": summary})

    conversation_history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )

    return response.choices[0].message.content

def main(pdf_path):
    summaries = summarize_pdf(pdf_path)

    # full_summary = "\n".join(summaries)
    # print("Summary of PDF:\n", full_summary)

    while True:
        user_question = input("\nAsk a question about the PDF (or type 'exit' to quit): ")
        if user_question.lower() == "exit":
            break

        answer = ask_question(summaries, user_question)
        print("\nAnswer:", answer)


# Run the program
main('../resources/SSO Integration.pdf')
