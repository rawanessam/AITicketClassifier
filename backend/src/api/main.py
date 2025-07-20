from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from ..models import promt_llm
from openai import OpenAIError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust port if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/submit-ticket")
async def submit_ticket(
    ticket_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    text: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    try:
        ticket_data = {
            "ticket_id": ticket_id,
            "message": "Ticket received",
            "data": {
                
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "issue_description": text,
                "attachments": [f.filename for f in files] if files else [],
            }
    }
        print("Received ticket data:")
        print(ticket_data)
        try:
            response = promt_llm(user_input=ticket_data["data"]["issue_description"])
        except OpenAIError as e:
            logger.error("OpenAI API error: %s", str(e))
            raise HTTPException(status_code=502, detail="OpenAI service is temporarily unavailable.")
        return response
    except:
        logger.exception("Unexpected server error")
        raise HTTPException(status_code=500, detail="Internal server error")

