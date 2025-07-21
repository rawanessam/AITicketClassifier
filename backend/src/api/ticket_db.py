import json
import os
from dotenv import load_dotenv
import os
from pathlib import Path

### Script to save ticket data an LLM reponse to .json db
load_dotenv()

config = os.getenv("CONFIG_FILE")
src_path = os.getcwd()
### Process config file
config_dict = json.loads(open(f"{config}").read())

DB_PATH = config_dict["DB_path"]

#DB_PATH = "DB.json"
def save_ticket(ticket_id: str, user_data: dict, llm_response: dict):
    """
    Save ticket data and LLM response to a local JSON file.
    """
    entry = {
        "ticket_id": ticket_id,
        "user_data": user_data,
        "llm_response": llm_response
    }

    # Load existing data
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            try:
                db = json.load(f)
            except json.JSONDecodeError:
    
                db = []
    else:
        file_path = Path(DB_PATH)
        dir_path = file_path.parent
        if not os.path.exists(dir_path):
            dir_path.mkdir(parents=True)
        db = []

    # Append new entry
    db.append(entry)

    # Save back
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)
