from models import prompt_llm
from api import app
from fastapi import  UploadFile, File, Form
from typing import List, Optional

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
    # Example: store or process ticket
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
    
    return ticket_data
