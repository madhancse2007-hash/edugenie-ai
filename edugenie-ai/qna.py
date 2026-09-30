import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_gemini_model():
    """Configures and returns a Gemini GenerativeModel with resilient fallback."""
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
    
    preferred_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    return preferred_model

def answer_question_with_gemini(question: str) -> str:
    """Answers user question using Google Gemini model."""
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        return "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file."

    model_name = get_gemini_model()
    # Candidate models with gemini-3.8-flash prioritized
    candidate_models = [model_name, "gemini-3.8-flash", "models/gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    # De-duplicate while preserving order
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

    last_error = None
    for candidate in models_to_try:
        try:
            model = genai.GenerativeModel(model_name=candidate)
            response = model.generate_content(question)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return response.parts[0].text.strip()
        except Exception as e:
            last_error = e
            continue

    return f"⚠️ Error in QnA: {last_error}"
