from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
app = FastAPI()
exec(open("src/models/engine.py").read())

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
    print(prompt_llm(user_input =ticket_data["data"]['issue_description']))
    return ticket_data