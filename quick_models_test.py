# quick_models_test.py
import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=api_key)

print("Models visible to this API key:")
for m in genai.list_models():
    print("-", m.name)
