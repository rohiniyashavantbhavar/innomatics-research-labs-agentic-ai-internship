# AI Resume Screening System

An AI-powered system that evaluates resumes against a job description using LLMs.

---

## Features
- Skill extraction (skills, experience, tools)
- Resume-job matching
- Fit score (0–100)
- Explainable results
- LangSmith tracing for debugging

---

## Tech Stack
- Python  
- LangChain  
- HuggingFace  
- LangSmith  

---

## Pipeline
Resume → Extraction → Matching → Scoring → Explanation

---

## How to Run
```bash
pip install -r requirements.txt
python main.py

Add API keys in main.py:
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "your_key"
os.environ["LANGCHAIN_API_KEY"] = "your_key"
