from fastapi import FastAPI, File, UploadFile, Form
from openai import OpenAI
from dotenv import load_dotenv
from app.services.pdf_processing import *
import os
from typing import Dict, List
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
async def upload_pdf(
        file: UploadFile = File(...)
):
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


last_page_memory: Dict[str, str] = {}

@app.post("/summarize")
async def summarize_page(
        pdf_id: str = Form(...),
        page_number: int = Form(...)
):
    """
    Endpoint to summarize a specific page of a stored PDF.
    (with continuity from previous pages)
    Accepts pdf_id and page_number as form data.
    """
    try:
        if pdf_id not in pdf_storage:
            raise HTTPException(status_code=404, detail="PDF not found. Please upload the PDF first.")

        pdf_pages = pdf_storage[pdf_id]
        if page_number < 1 or page_number > len(pdf_pages):
            raise HTTPException(status_code=400, detail="Invalid page number.")

        current_page_text = pdf_pages[page_number - 1]
        previous_page_text = last_page_memory.get(pdf_id, "")

        messages = [
            {"role": "system",
             "content": "You are a helpful school teacher. Explain everything as if the user is an amateur."},
            {"role": "user",
             "content": f"(if this page is a cover page or a table of contents, just say so and don't summarise it. If it isn't ignore this bracket.). Here is the context from the previous page: {previous_page_text}"},
            {"role": "user",
             "content": f"Now explain the current page in detail by breaking down each jargon into their meanings: {current_page_text}"}
        ]

        summary = summarize_text(client, messages)
        last_page_memory[pdf_id] = current_page_text

        return {
            "pdf_id": pdf_id,
            "page_number": page_number,
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


mcq_answers_storage: Dict[str, List[int]] = {}

@app.post("/generate-mcq")
async def generate_mcq(
        pdf_id: str = Form(...),
        page_number: int = Form(...)
):
    """
    Generate multiple-choice questions (MCQs) for a specific page.
    """
    try:
        if pdf_id not in pdf_storage:
            raise HTTPException(status_code=404, detail="PDF not found. Please upload the PDF first.")

        pdf_pages = pdf_storage[pdf_id]
        if page_number < 1 or page_number > len(pdf_pages):
            raise HTTPException(status_code=400, detail="Invalid page number.")

        current_page_text = pdf_pages[page_number - 1]

        summary_message = [
            {"role": "system",
             "content": "You are a helpful school teacher. Explain everything as if the user is an amateur."},
            {"role": "user", "content": f"Summarize this text: {current_page_text}"}
        ]

        summary = summarize_text(client, summary_message)

        if not summary or len(summary.split()) < 20:
            raise HTTPException(status_code=400, detail="Summary does not contain enough content to generate MCQs.")

        mcq_message = [
            {"role": "system",
             "content": "You are a helpful school teacher. Generate 4 multiple-choice questions (MCQs) with their correct answers based on the following summary."},
            {"role": "user",
             "content": f"Summary: {summary}\n\nGenerate 4 multiple-choice questions (MCQs) with their correct answers. Format: \nQ1: [Question]\na) [Option 1]\nb) [Option 2]\nc) [Option 3]\nd) [Option 4]\nCorrect answer: [number of correct option]"}
        ]

        mcqs_text = summarize_text(client, mcq_message)

        questions, options, correct_answers = generate_mcq_from_summary(mcqs_text)

        if not questions or not options or not correct_answers:
            raise HTTPException(status_code=500, detail="Failed to generate valid MCQs from the summary.")

        mcq_answers_storage[f"{pdf_id}_{page_number}"] = correct_answers

        mcq_response = []
        for i in range(len(questions)):
            mcq_response.append({
                "question": questions[i],
                "options": options[i],
                "correct_ans": correct_answers[i]
            })

        return {
            "pdf_id": pdf_id,
            "page_number": page_number,
            "mcqs": mcq_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")