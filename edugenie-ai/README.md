# EduGenie: Google Gemini Powered Learning Assistant 🧠✨

EduGenie is an AI-powered educational assistant designed to simplify learning for students of all academic levels. It combines cloud-based generative AI (Google Gemini) for reasoning, question-answering, quizzes, summarization, and curriculum planning with an optional local lightweight model (`MBZUAI/LaMini-Flan-T5-783M`) for concept simplification.

---

## 🏗️ System Architecture

```text
                               +-------------------------------------+
                               |           User Opens Web UI         |
                               |         http://127.0.0.1:8000       |
                               +------------------+------------------+
                                                  |
                                                  v
                               +-------------------------------------+
                               |        Frontend (HTML5 + CSS3)      |
                               |    Interactive Forms & Quiz Engine  |
                               +------------------+------------------+
                                                  |
                                                  v  (AJAX Fetch)
                               +-------------------------------------+
                               |           FastAPI Backend           |
                               |               (main.py)             |
                               +--+-------+--------+-------+-------+-+
                                  |       |        |       |       |
            +---------------------+       |        |       |       +---------------------+
            |                             |        |       |                             |
            v                             v        v       v                             v
+-----------------------+              +-----------------------+              +-----------------------+
|  Explanation Module   |              |   Q&A, Quiz, Summary  |              |  Learning Path Module |
|     (/explain/)       |              |  (/qa, /quiz, /sum..) |              | (/learn/recommend..)  |
|  LaMini-Flan-T5-783M  |              |    Google Gemini      |              |    Google Gemini      |
|  (Local Hugging Face) |              |   (1.5 Pro / Flash)   |              |   (1.5 Pro / Flash)   |
+-----------------------+              +-----------------------+              +-----------------------+
```

---

## 📁 Project Directory Structure

```text
EduGenie/
├── main.py                  # FastAPI application entrypoint & routing
├── explanation_module.py    # Concept explanation logic (LaMini-Flan-T5 / Gemini fallback)
├── qna.py                   # Question answering with Google Gemini
├── quiz_module.py           # MCQ generation & JSON parsing engine
├── summary_module.py        # Text & paragraph summarization
├── learning_path.py         # Step-by-step personalized learning curriculum
├── templates/
│   └── index.html           # Modern responsive web UI
├── static/
│   └── style.css            # Custom CSS styles matching project design
├── requirements.txt         # Project dependencies
├── .env.example             # Environment variable template
├── .env                     # Your local API configuration (gitignored)
└── README.md                # Documentation and setup instructions
```

---

## ⚙️ Prerequisites

1. **Python 3.10+** (Python 3.10 or 3.11 recommended)
2. **Google Gemini API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google Account
   - Click **Create API Key** and copy your key.

---

## 🚀 Setup & Installation in VS Code

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Go to **File** > **Open Folder...** and select the `edugenie-ai` folder.
3. Open the integrated terminal in VS Code using the shortcut:
   - **Windows / Linux**: `Ctrl` + `~` (backtick)
   - **macOS**: `Cmd` + `~`

---

### Step 2: Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

**On Windows (Command Prompt `cmd`):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Required Dependencies

Upgrade `pip` and install all requirements:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Configure Your Gemini API Key

1. Copy `.env.example` to `.env`:
   - On Windows: `copy .env.example .env`
   - On macOS/Linux: `cp .env.example .env`
2. Open the `.env` file in VS Code and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   GEMINI_MODEL=models/gemini-1.5-pro
   ```

---

### Step 5: Start the EduGenie Application

Run the server using Uvicorn:
```bash
uvicorn main:app --reload
```

You should see:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

---

## 🧪 Testing the Application

### 1. Web UI Features:
- **Ask EduGenie a Question (`/qa`)**:
  - Enter: `Which is the largest ocean?`
  - Click **Get Answer** -> Displays concise answer from Gemini.
- **Need an Explanation? (`/explain`)**:
  - Enter: `Photosynthesis` or `Quantum computing`
  - Click **Explain** -> Explains topic clearly for school students.
- **Summarize a Paragraph (`/summarize`)**:
  - Paste any lengthy paragraph.
  - Click **Summarize** -> Returns a concise, easy-to-understand version.
- **Generate a Quiz (`/quiz`)**:
  - Enter: `Pythagoras theorem` or `Solar System`
  - Click **Generate Quiz** -> Renders 3 MCQs with 4 options each.
  - Select your answer and click **Check Answer** -> Instant feedback: `✅ Correct!` or `❌ Incorrect. Correct answer: ...`.
- **Get Learning Recommendations (`/learn/recommendations`)**:
  - Enter: `SQL` or `Machine Learning`
  - Click **Get Recommendations** -> Outputs a structured roadmap (Beginner, Intermediate, Advanced) with recommended resources.

---

### 2. Interactive Swagger / OpenAPI Documentation
EduGenie provides auto-generated API documentation:
- Swagger UI: **`http://127.0.0.1:8000/docs`**
- ReDoc: **`http://127.0.0.1:8000/redoc`**

---

## 🛠️ API Endpoints Summary

| Endpoint | Method | Input Parameters / Payload | Description |
|---|---|---|---|
| `/` | GET | None | Serves the HTML frontend interface |
| `/health` | GET | None | Server health status check |
| `/qa` | GET | `?question=<query>` | Gemini Q&A answering |
| `/explain/` | POST | `{"topic": "<topic>"}` | Concept explanation module |
| `/summarize/` | POST | `{"text": "<passage>"}` | Text summarization module |
| `/quiz` | POST | `{"text": "<passage_or_topic>"}` | 3 MCQs quiz generator in JSON |
| `/learn/recommendations` | GET | `?topic=<topic>` | Structured adaptive learning path |

---

## 💡 Notes on AI Models
- **Google Gemini**: Uses `models/gemini-1.5-pro` (or resilient fallbacks to `gemini-1.5-flash` / `gemini-2.5-flash` depending on your AI Studio quota and region).
- **LaMini-Flan-T5-783M**: Automatically loads locally when available via Hugging Face Transformers. If running in lightweight or resource-limited environments, it seamlessly falls back to cloud inference so you never face crashes.
