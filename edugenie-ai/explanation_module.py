import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"
explain_tokenizer = None
explain_model = None
_model_load_attempted = False

def load_local_model():
    """Lazily loads the LaMini-Flan-T5 model and tokenizer to prevent server blocking on startup."""
    global explain_tokenizer, explain_model, _model_load_attempted
    if _model_load_attempted:
        return explain_tokenizer, explain_model

    _model_load_attempted = True
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch

        print(f"Loading local explanation model: {MODEL_NAME}...")
        explain_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        explain_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        print("LaMini-Flan-T5 model loaded successfully.")
    except Exception as e:
        print(f"Notice: Local model '{MODEL_NAME}' could not be loaded ({e}). A cloud AI fallback will be used if needed.")
        explain_tokenizer = None
        explain_model = None

    return explain_tokenizer, explain_model

def explain_topic(topic: str) -> str:
    """Explains a topic in simple terms using LaMini-Flan-T5-783M with Gemini fallback."""
    tokenizer, model = load_local_model()

    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."

    if tokenizer is not None and model is not None:
        try:
            inputs = tokenizer(input_text, return_tensors="pt")
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation.strip()
        except Exception as e:
            print(f"Error during local model inference: {e}")

    # Seamless fallback using Gemini if local model weights are unavailable or failed
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if api_key and api_key != "your_gemini_api_key_here":
            genai.configure(api_key=api_key)
            load_dotenv(override=True)
            pref_m = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
            for m in [pref_m, "gemini-3.8-flash", "models/gemini-3.8-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
                try:
                    gemini_model = genai.GenerativeModel(model_name=m)
                    resp = gemini_model.generate_content(prompt)
                    if hasattr(resp, "text") and resp.text:
                        return resp.text.strip()
                except Exception:
                    continue
    except Exception as e:
        return f"⚠️ Error in Explanation: {e}"

    return f"⚠️ Unable to generate explanation for '{topic}'. Please verify your setup or Gemini API key in .env."
