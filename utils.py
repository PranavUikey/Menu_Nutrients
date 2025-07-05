import json
import re

def extract_json_array(text):
    """
    Extract and return a JSON array from a given text.
    Example: ["Dish 1", "Dish 2"]
    """
    try:
        text = text.replace("“", '"').replace("”", '"').strip()
        match = re.search(r"\[\s*\".*?\"\s*\]", text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON array found.")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Could not parse JSON array: {e}")


def extract_json_object(text):
    """
    Extract and return a JSON object from a given text.
    Attempts to fix missing closing braces if needed.
    """
    try:
        # Extract the most likely JSON object from the text
        match = re.search(r"\{.*", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found.")

        json_text = match.group(0)

        # Count braces to detect imbalance
        open_braces = json_text.count("{")
        close_braces = json_text.count("}")

        if open_braces > close_braces:
            json_text += "}" * (open_braces - close_braces)

        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Could not parse JSON object: {e}")
