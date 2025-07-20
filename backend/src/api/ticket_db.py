import json
import os

DB_PATH = "ticket_db.json"

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
        db = []

    # Append new entry
    db.append(entry)

    # Save back
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)
