import os
import traceback
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_learning_recommendations(topic: str) -> str:
    """Generates structured, step-by-step learning paths from beginner to advanced with resources."""
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        return "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file."

    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (books, tutorials, videos).
Include beginner, intermediate, and advanced levels if needed.
"""
    genai.configure(api_key=api_key)
    pref_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    candidate_models = [pref_model, "gemini-3.8-flash", "models/gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    last_error = None

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            print("[EduGenie] Gemini learning path response received.")

            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return response.parts[0].text.strip()
            else:
                return "❌ Could not extract content from Gemini response."
        except Exception as e:
            last_error = e
            continue

    traceback.print_exc()
    return f"❌ Error occurred: {str(last_error)}"
