from fastapi import HTTPException
import PyPDF2

def summarize_text(client, text_chunk):
    """
    Summarize the chunk of text using OpenAI's chat-based API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful school teacher. Explain everything as if the user is an amateur."},
                {"role": "user", "content": f"Explain this in great detail by breaking down each jargon into their meanings: {text_chunk}"}
            ]
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