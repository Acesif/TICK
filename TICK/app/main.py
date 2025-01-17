from fastapi import FastAPI, File, UploadFile, Form
from openai import OpenAI
from dotenv import load_dotenv
from app.services.pdf_processing import *
import os
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
api_key = os.getenv("api_key")
client = OpenAI(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_storage: Dict[str, list] = {}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file and store its pages in memory.
    """
    try:
        pdf_pages = load_pdf_pages(client, file.file)
        pdf_id = file.filename
        pdf_storage[pdf_id] = pdf_pages

        return {
            "pdf_id": pdf_id,
            "total_pages": len(pdf_pages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/summarize")
async def summarize_page(pdf_id: str = Form(...), page_number: int = Form(...)):
    """
    Endpoint to summarize a specific page of a stored PDF.
    Accepts pdf_id and page_number as form data.
    """
    try:
        if pdf_id not in pdf_storage:
            raise HTTPException(status_code=404, detail="PDF not found. Please upload the PDF first.")

        pdf_pages = pdf_storage[pdf_id]
        if page_number < 1 or page_number > len(pdf_pages):
            raise HTTPException(status_code=400, detail="Invalid page number.")
        page_text = pdf_pages[page_number - 1]
        summary = summarize_text(client, page_text)

        return {"pdf_id": pdf_id, "page_number": page_number, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

"""
todo: 

1. ask the user questions based on the summary provided
2. give points or marks based on the number of questions gotten correct
3. return the points

"""