"""GoldenHour AI backend: POST /extract  ->  symptom JSON.

Run locally:  uvicorn main:app --reload
The API key is read from an environment variable and NEVER goes in the website.
"""
import os
import time
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from logic import MAX_CHARS, SYSTEM, clean, parse_llm_output

app = FastAPI(title="GoldenHour AI backend")

# After deploying the website, set ALLOWED_ORIGINS to its address, e.g. https://yourname.github.io
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=["POST"], allow_headers=["Content-Type"])

# Copy the exact model name from the Groq console (console.groq.com) and set LLM_MODEL.
# The default below may be retired by Groq, so check it if you get a "model not found" error.
MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

# Very small rate limit (per IP, per minute) to protect your API budget.
hits = defaultdict(list)
LIMIT_PER_MIN = 10


class Req(BaseModel):
    text: str
    lang: str = "en"


def call_llm(text: str) -> str:
    """The ONLY place that talks to the LLM. To use another provider, change just this function."""
    from groq import Groq  # pip install groq; reads GROQ_API_KEY from the environment
    client = Groq()
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
        temperature=0,
        max_tokens=300,
    )
    return r.choices[0].message.content


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/extract")
def extract(req: Req, request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    hits[ip] = [t for t in hits[ip] if now - t < 60]
    if len(hits[ip]) >= LIMIT_PER_MIN:
        raise HTTPException(status_code=429, detail="Too many requests")
    hits[ip].append(now)

    text = req.text.strip()[:MAX_CHARS]
    if not text:
        return clean({})
    try:
        return parse_llm_output(call_llm(text))
    except Exception:
        # If the LLM fails, the website still works with its keyword backstop.
        raise HTTPException(status_code=502, detail="LLM unavailable")
