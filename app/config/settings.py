# app/config/settings.py

import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

def get_gemini_api_key() -> str:
    """
    Returns the Gemini API key loaded from environment/.env.
    Raises a clear error if it's missing.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. "
            "Create a .env file in the project root with line: "
            "GEMINI_API_KEY=your_key_here"
        )
    return api_key
