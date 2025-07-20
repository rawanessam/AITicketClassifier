from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import traceback
import json

app = FastAPI()

engine_loaded = True

try:
    exec(open("src/models/engine.py").read(), globals())
    if "prompt_llm" not in globals():
        engine_loaded = False
        raise ImportError("prompt_llm function not found after executing engine.py")
except Exception as e:
    traceback.print_exc()
    engine_loaded = False  
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
    if not engine_loaded:
        return JSONResponse(
            status_code=503,
            content={"detail": "LLM engine not initialized. Please check backend configuration."}
        )
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
    if not engine_loaded:
        raise HTTPException(status_code=503, detail="LLM engine not initialized. Cannot process requests.")
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Issue description cannot be empty.")


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
        try:
            raw_response = prompt_llm(user_input=text)
            parsed = json.loads(raw_response)
            print(parsed)
        except json.JSONDecodeError:
            traceback.print_exc()
            raise HTTPException(status_code=502, detail="Invalid JSON from LLM.")
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=502, detail="LLM call failed.")

        # print("Received ticket data:")
        # print(ticket_data)
        return JSONResponse(content=parsed)
    except HTTPException as e:
        raise e

    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."}
        )