import os
import re
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
        return api_key
    return None

def clean_json_block(text: str) -> str:
    """Removes Markdown ```json code fences and strips whitespace."""
    # Try exact markdown fence matching first
    cleaned = re.sub(r"^```(?:json)?\s*\n(.*?)\n```$", r"\1", text.strip(), flags=re.DOTALL)
    if cleaned != text.strip():
        return cleaned.strip()

    # If surrounding fences exist anywhere
    match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Find raw JSON list if present
    match_list = re.search(r"(\[\s*\{.*\}\s*\])", text, re.DOTALL)
    if match_list:
        return match_list.group(1).strip()

    return text.strip()

def generate_quiz(text: str) -> list:
    """Generates 3 multiple-choice questions with 4 options and answers from a text/topic."""
    api_key = get_api_key()
    if not api_key:
        return [{"error": "⚠️ Gemini API key is missing. Please set your GEMINI_API_KEY in the .env file."}]

    prompt = f"""
You are a quiz generator.

From the following passage or topic, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
    pref_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    candidate_models = [pref_model, "gemini-3.8-flash", "models/gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    last_error = None

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            quiz_text = response.text.strip() if hasattr(response, "text") else ""

            cleaned_text = clean_json_block(quiz_text)
            parsed_quiz = json.loads(cleaned_text)

            if isinstance(parsed_quiz, list) and len(parsed_quiz) > 0:
                return parsed_quiz
        except Exception as e:
            last_error = e
            continue

    safe_err = str(last_error).encode('ascii', 'replace').decode('ascii')
    print(f"[EduGenie] Error in Quiz Generation: {safe_err}")
    return [{"error": f"⚠️ Error in Quiz Generation: {last_error}"}]
