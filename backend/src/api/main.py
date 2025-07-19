from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

app = FastAPI()

# Enable CORS for frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust port if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit-ticket")
async def submit_ticket(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    issue_description: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    # Example: store or process ticket
    return {
        "message": "Ticket received",
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "issue_description": issue_description,
            "attachments": [f.filename for f in files] if files else [],
        }
    }
