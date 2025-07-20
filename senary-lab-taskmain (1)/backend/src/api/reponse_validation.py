import json
from typing import Any, Dict

def validate_llm_output(llm_output: str) -> Dict[str, Any]:
   
    
    parsed =llm_output
   
    if not isinstance(parsed, dict):
        raise ValueError("LLM output must be a JSON object.")

    required_keys = ["feedback_text", "category", "urgency_score"]
    for key in required_keys:
        if key not in parsed:
            raise ValueError(f"Missing required field in LLM output: {key}")

    if not isinstance(parsed["feedback_text"], str):
        raise ValueError("feedback_text must be a string.")

    if not isinstance(parsed["category"], str):
        raise ValueError("category must be a string.")

    if parsed["urgency_score"] is not None and not isinstance(parsed["urgency_score"], int):
        raise ValueError("urgency_score must be an integer or null.")

    return llm_output

#validate_llm_output("")
