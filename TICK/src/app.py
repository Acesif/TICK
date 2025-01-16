from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Dict

# Load environment variables
load_dotenv()
api_key = os.getenv("api_key")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create FastAPI instance
app = FastAPI()

# Temporary storage for uploaded PDF files (in memory for this example)
pdf_storage: Dict[str, list] = {}


def summarize_text(text_chunk):
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


def load_pdf_pages(pdf_file):
    """
    Load all pages from a PDF and return a list of text from each page.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pages = [pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))]
        return pages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while reading PDF: {str(e)}")


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file and store its pages in memory.
    """
    try:
        # Extract pages and store in memory
        pdf_pages = load_pdf_pages(file.file)
        pdf_id = file.filename  # Using filename as an identifier for simplicity
        pdf_storage[pdf_id] = pdf_pages

        return {"message": "PDF uploaded successfully", "pdf_id": pdf_id, "total_pages": len(pdf_pages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/summarize")
async def summarize_page(pdf_id: str = Form(...), page_number: int = Form(...)):
    """
    Endpoint to summarize a specific page of a stored PDF.
    Accepts pdf_id and page_number as form data.
    """
    try:
        # Check if the PDF exists in storage
        if pdf_id not in pdf_storage:
            raise HTTPException(status_code=404, detail="PDF not found. Please upload the PDF first.")

        pdf_pages = pdf_storage[pdf_id]

        # Check if the requested page number is valid
        if page_number < 1 or page_number > len(pdf_pages):
            raise HTTPException(status_code=400, detail="Invalid page number.")

        # Get the requested page text
        page_text = pdf_pages[page_number - 1]  # Page numbers are 1-based

        # Summarize the page text
        summary = summarize_text(page_text)

        return {"pdf_id": pdf_id, "page_number": page_number, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
