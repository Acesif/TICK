from pydantic import BaseModel

class SummarizeRequest(BaseModel):
    pdf_id: str
    page_number: int