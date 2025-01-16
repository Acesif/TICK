import PyPDF2
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = OpenAI(api_key=api_key)


def summarize_text(text_chunk):
    """
    Summarize the chunk of text using OpenAI's chat-based API.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful school teacher. Explain everything as if the user is an amateur"},
            {"role": "user", "content": f"Explain this in great detail by breaking down each jargon into their meanings: {text_chunk}"}
        ]
    )
    return response.choices[0].message.content


def summarize_pdf_page(page_text):
    """
    Summarize a single page of text.
    """
    return summarize_text(page_text)


def load_pdf_pages(pdf_path):
    """
    Load all pages from a PDF and return a list of text from each page.
    """
    pdf_file = open(pdf_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    pages = [pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))]
    pdf_file.close()
    return pages


def main(pdf_path):
    pages = load_pdf_pages(pdf_path)
    page_index = 0

    while page_index < len(pages):

        if page_index == 0:
            print(f"\nExplaining page {page_index}:\n")
            page_summary = summarize_pdf_page(pages[page_index])
            print(page_summary)
            page_index += 1

        user_input = input("\nType 'next' to explain the next page or 'exit' to quit: ").lower()

        if user_input == 'exit':
            print("Exiting program.")
            break

        if user_input == 'next':
            print(f"\nExplaining page {page_index}:\n")
            page_summary = summarize_pdf_page(pages[page_index])
            print(page_summary)
            page_index += 1

        else:
            print("Invalid input. Please type 'next' or 'exit'.")

    if page_index >= len(pages):
        print("\nYou have reached the end of the document.")


# Run the program
main('../resources/SSO Integration.pdf')
