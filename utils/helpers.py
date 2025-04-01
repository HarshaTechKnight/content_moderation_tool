import re
from typing import Dict, Any

def clean_text(text: str) -> str:
    """Clean and preprocess text for analysis."""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user @ references and '#' from hashtags
    text = re.sub(r'\@\w+|\#', '', text)
    # Remove special characters
    text = re.sub(r'\W', ' ', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def format_moderation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format the moderation result for API response."""
    return {
        "status": "flagged" if result["flagged"] else "approved",
        "categories": result["categories"],
        "scores": {k: float(v) for k, v in result["scores"].items()},
        "explanation": result.get("explanation", ""),
        "moderation_type": result.get("moderation_type", "unknown")
    }