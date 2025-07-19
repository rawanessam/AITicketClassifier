from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
import os
from datetime import datetime
import json

app = FastAPI(title="IT Support Portal API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TicketRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None
    issueDescription: str

class TicketResponse(BaseModel):
    success: bool
    message: str
    ticketId: str
    submittedAt: datetime

# In-memory storage (replace with database in production)
tickets_db = []

# Directory for file uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "IT Support Portal API", "status": "running"}

@app.post("/api/tickets", response_model=TicketResponse)
async def create_ticket(
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    issueDescription: str = Form(...),
    files: List[UploadFile] = File(default=[])
):
    try:
        # Generate unique ticket ID
        ticket_id = f"IT-{str(uuid.uuid4())[:8].upper()}"
        
        # Process file uploads
        uploaded_files = []
        for file in files:
            if file.filename:
                # Create unique filename
                file_extension = os.path.splitext(file.filename)[1]
                unique_filename = f"{ticket_id}_{uuid.uuid4().hex[:8]}{file_extension}"
                file_path = os.path.join(UPLOAD_DIR, unique_filename)
                
                # Save file
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                uploaded_files.append({
                    "original_name": file.filename,
                    "saved_name": unique_filename,
                    "file_path": file_path,
                    "size": len(content)
                })
        
        # Create ticket record
        ticket = {
            "ticketId": ticket_id,
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phone": phone,
            "issueDescription": issueDescription,
            "attachments": uploaded_files,
            "submittedAt": datetime.now(),
            "status": "open"
        }
        
        # Store ticket (in production, save to database)
        tickets_db.append(ticket)
        
        # Log ticket creation
        print(f"New ticket created: {ticket_id}")
        print(f"User: {firstName} {lastName} ({email})")
        print(f"Issue: {issueDescription[:100]}...")
        print(f"Attachments: {len(uploaded_files)} files")
        
        return TicketResponse(
            success=True,
            message="Ticket submitted successfully",
            ticketId=ticket_id,
            submittedAt=ticket["submittedAt"]
        )
        
    except Exception as e:
        print(f"Error creating ticket: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create ticket")

@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Get ticket details by ID"""
    ticket = next((t for t in tickets_db if t["ticketId"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("/api/tickets")
async def list_tickets():
    """List all tickets (for admin use)"""
    return {
        "tickets": tickets_db,
        "total": len(tickets_db)
    }

@app.delete("/api/tickets/{ticket_id}")
async def delete_ticket(ticket_id: str):
    """Delete a ticket"""
    global tickets_db
    ticket = next((t for t in tickets_db if t["ticketId"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Remove associated files
    for attachment in ticket.get("attachments", []):
        try:
            os.remove(attachment["file_path"])
        except FileNotFoundError:
            pass
    
    # Remove ticket from database
    tickets_db = [t for t in tickets_db if t["ticketId"] != ticket_id]
    
    return {"message": "Ticket deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
