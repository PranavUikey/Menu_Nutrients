import re
import json

def extract_json_array(text: str):
    try:
        text = text.replace("“", '"').replace("”", '"').strip()
        match = re.search(r"\[\s*\".*?\"\s*\]", text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON array found.")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Could not parse JSON array: {e}")

def extract_json_object(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found.")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Could not parse JSON object: {e}")
