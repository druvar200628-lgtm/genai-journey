from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pypdf import PdfReader
import os
import json
import uvicorn
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

# Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
ENV_PATH = PROJECT_DIR / ".env"
PDF_PATH = BASE_DIR / "druva_resume.pdf"
FRONTEND_HTML_PATH = PROJECT_DIR / "frontend" / "html" / "index.html"

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH)
load_dotenv()  # fallback to current working directory

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key kaha hai bhai! Please set GROQ_API_KEY in your .env file.")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

app = FastAPI(title="Druva R - AI Interview Assistant", version="2.0")

# Enable CORS for seamless frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

resume_schema = Resume.model_json_schema()

class chatRequest(BaseModel):
    question: str

# In-memory cache for parsed resume to avoid re-parsing on every chat call
_cached_resume: Resume | None = None

def ask_candidtae(question: str, resume: Resume) -> str:
    system_prompt = f"""
You are an AI assistant professionally representing the candidate, {resume.name or 'the candidate'}, during a job interview.

Candidate Resume Information:
{resume.model_dump_json(indent=2)}

Rules:
1. Answer in first-person ("I", "my") as the candidate being interviewed by HR or an engineering manager.
2. Answer truthfully using ONLY the provided resume information.
3. Never hallucinate or make up details not present in the resume.
4. If asked about something unavailable in the resume, reply politely:
   "I don't have that specific information mentioned on my resume, but I would be glad to discuss it further or learn more."
5. Be professional, articulate, confident, and concise. Format points clearly using bullet points when discussing projects or achievements.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def parse_resume(resume_text: str) -> Resume:
    system_prompt = f"""
You are an expert resume parser.

Extract information from the resume based on its meaning,
not only based on exact section headings.

Different resumes may use different headings:
- Experience, Professional Experience, Work History, Employment, Internships
- Projects, Technical Projects, Academic Projects
- Education, Academic Background
- Skills, Technical Skills, Core CS

Return ONLY valid JSON matching this schema:
{resume_schema}

Important rules:
1. Do not invent information.
2. If a value is not available, return null.
3. If a list has no information, return an empty list.
4. Include internships inside experiences.
5. Extract skills mentioned across the entire resume.
"""
    user_prompt = f"""
Parse the following resume:

{resume_text}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    return Resume(**data)

def read_pdf(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Resume PDF file not found at: {file_path}")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def get_or_parse_resume() -> Resume:
    global _cached_resume
    if _cached_resume is None:
        if not PDF_PATH.exists():
            raise HTTPException(status_code=404, detail=f"PDF not found at {PDF_PATH}")
        resume_text = read_pdf(PDF_PATH)
        _cached_resume = parse_resume(resume_text)
    return _cached_resume

# Endpoints
@app.get("/")
def home():
    if FRONTEND_HTML_PATH.exists():
        return FileResponse(FRONTEND_HTML_PATH)
    return {
        "message": "AI Resume Assistant Backend is running",
        "endpoints": {
            "candidate": "/candidate",
            "chat": "/chat (POST)",
            "reload": "/reload (POST)"
        }
    }

@app.get("/candidate")
def get_candidate():
    """Returns candidate profile and extracted resume data for the frontend."""
    resume = get_or_parse_resume()
    return resume.model_dump()

@app.post("/chat")
def chat(request: chatRequest):
    """Processes HR questions using the candidate's resume context."""
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    resume = get_or_parse_resume()
    answer = ask_candidtae(request.question.strip(), resume)
    return {
        "answer": answer,
        "candidate": resume.name
    }

@app.post("/reload")
def reload_resume():
    """Forces re-parsing of the resume PDF."""
    global _cached_resume
    _cached_resume = None
    resume = get_or_parse_resume()
    return {
        "message": "Resume successfully reloaded and parsed.",
        "candidate": resume.name
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": model,
        "resume_cached": _cached_resume is not None
    }

if __name__ == "__main__":
    uvicorn.run("chatBot:app", host="127.0.0.1", port=8000, reload=True)
