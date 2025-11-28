# app/llm/client.py

import google.generativeai as genai
from app.config.settings import get_gemini_api_key

# Configure Gemini once, using key from .env / environment
genai.configure(api_key=get_gemini_api_key())

def get_llm_client(model_name: str = "models/gemini-2.5-flash"):
    """
    Returns a configured Gemini GenerativeModel instance.
    Default model: models/gemini-2.5-flash
    """
    return genai.GenerativeModel(model_name)
