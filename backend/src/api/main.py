from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import traceback
import json
from dotenv import load_dotenv
from .reponse_validation import validate_llm_output
from .ticket_db import save_ticket
import os

app = FastAPI()
load_dotenv()
engine_loaded = True
config = os.getenv("CONFIG_FILE")
src_path = os.getcwd()
try:
    config_dict = json.loads(open(f"{src_path}/{config}").read())
except:
    config_dict = json.loads(open(f"App/config/docker_config").read())
prompt_script = config_dict["llm_prompting_script"]

try:
    try:
        exec(open(f"{src_path}/{prompt_script}").read(), globals())
    except:
        exec(open(f"{prompt_script}").read(), globals())
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
            raw_response = prompt_llm(user_input=text) # type: ignore
            parsed = json.loads(raw_response)
            
        except json.JSONDecodeError:
            traceback.print_exc()
            raise HTTPException(status_code=502, detail="Invalid JSON from LLM.")
        except Exception:
            traceback.print_exc()
            raise HTTPException(status_code=502, detail="LLM call failed.")
        try: 
            parsed = validate_llm_output(parsed)
        except ValueError:
            raise HTTPException(status_code=504, detail="LLM malformed output")
        # print("Received ticket data:")
        # print(ticket_data)
        save_ticket(ticket_id, ticket_data,parsed)
        return JSONResponse(content=parsed)
    except HTTPException as e:
        raise e

    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."}
        )