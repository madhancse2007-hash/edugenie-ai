from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie AI",
    description="Google Gemini Powered Educational Assistant",
    version="1.0.0"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static and template directories exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Root Endpoint: Web Interface
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EduGenie AI"}

# Q&A - GET API using Gemini
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# Explanation - POST API (supports both with and without trailing slash)
@app.post("/explain/")
@app.post("/explain")
async def explain_api(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON in request body."}, status_code=400)
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

# Summarization - POST API (supports both with and without trailing slash)
@app.post("/summarize/")
@app.post("/summarize")
async def summarize_api(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON in request body."}, status_code=400)
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}

# Quiz Generation - POST API (supports both with and without trailing slash)
@app.post("/quiz")
@app.post("/quiz/")
async def quiz_api(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON in request body."}, status_code=400)
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})

# Learning Recommendations - GET API
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
