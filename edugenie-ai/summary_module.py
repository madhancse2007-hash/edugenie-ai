import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def summarize_text(text: str) -> str:
    """Summarizes long educational text or passages in simple, concise language."""
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        return "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file."

    prompt = f"Summarize the following text in simple language:\n\n{text}"
    pref_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    candidate_models = [pref_model, "gemini-3.8-flash", "models/gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    last_error = None

    genai.configure(api_key=api_key)

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return response.parts[0].text.strip()
        except Exception as e:
            last_error = e
            continue

    return f"⚠️ Error in Summary: {last_error}"
