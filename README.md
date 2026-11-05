# GoldenHour AI

**Emergency guidance for families during a suspected stroke or heart attack, in English, Tamil and Hindi.**

Team: SD CODES (solo, Team Lead: Sai Deeksha S) | Build The AI For YOU 2026

- Live app: https://deeksh258.github.io/goldenhour-ai/
- Backend (Render): https://goldenhour-ai.onrender.com/docs

## The problem
In a stroke or heart attack, minutes matter. The family member beside the patient is often unsure what they are seeing, panics, delays the call to 108, and cannot explain clearly to the ambulance or hospital.

## What GoldenHour AI does
GoldenHour AI does not treat anyone. It shortens the time lost before treatment: faster recognition, a better 108 call, and a clearer handover.

## What works today
- Language selector: English, Tamil, Hindi
- Always-visible **Call 108** button
- Six quick-tap symptom buttons, or free-text and voice description
- **AI symptom reading (Groq) on a Render-hosted backend**, for free-text descriptions
- Safety rules in plain code decide the result: EMERGENCY, NOT_CLEAR (asks yes/no/not sure follow-ups) or NO_SIGNS_REPORTED. There is deliberately no "safe" level.
- Keyword matching always runs as a backstop. The AI can only add "yes" signs, never remove them.
- Emergency screen: onset time and timer, spoken waiting steps
- Ambulance details card (driver, phone, vehicle number, ETA) for details given by the 108 operator
- Nearby hospitals from OpenStreetMap, plus an "Open hospitals in Google Maps" button
- One-page handoff of observations only (never a diagnosis), shared by WhatsApp only after consent, or printed

## How it is built
- Frontend: single-file HTML/CSS/JavaScript, hosted on GitHub Pages
- Backend: Python FastAPI (`/extract`, `/health`) hosted on **Render** (Free instance)
- AI: Groq API, model `openai/gpt-oss-20b`. The API key is stored only in Render environment settings, never in this repo.
- Rate limit: 10 requests per minute per IP
- Hospitals: OpenStreetMap Overpass API (free, no key)

## Safety design
The LLM only extracts symptoms. It never decides the outcome. Plain-code rules do. The handoff lists observations only.

## Built during the sprint (1-5 Nov 2026)
- Hospital lookup from OpenStreetMap and Google Maps button (removed all sample hospitals)
- Greatly expanded Tamil, Hindi and English-letter keyword lists, with Unicode normalisation
- Improved voice input with clear status and error messages
- Ambulance details card
- Backend deployed on Render and connected to Groq

## Known limits and next steps
- Free Render instance sleeps when idle, so the first AI request can take 30-50 seconds. Keyword matching still works meanwhile.
- Keyword rules cannot handle negation or unusual wording. Some Tamil spellings, such as "maaradaippu", are not recognised yet.
- Tamil and Hindi text has not been reviewed by native speakers. Symptom rules and waiting steps have not been reviewed by a doctor. This is not a medical device.
- Hospital data is OpenStreetMap volunteer data. It does not show which hospitals treat stroke or heart attacks.
- There is no real ambulance tracking. Details are entered from the 108 operator.
- Voice input depends on the browser (best in Chrome).
- Planned: more spellings and phrasings, doctor and native-speaker review, verified stroke-ready hospital data.
- The Kaggle stroke dataset is not used and no risk-prediction model is built.

## Research
- About 6,99,000 stroke deaths in India in 2019 (7.4% of all deaths): India State-Level Disease Burden Initiative Neurological Disorders Collaborators, Lancet Global Health 2021. https://doi.org/10.1016/S2214-109X(21)00164-9
- Existing tools are mostly state-run, professional-facing or hospital-side. We focus on the family, in regional languages.

## Acknowledgements and AI assistance
AI assistance: **Claude (Anthropic)**. I tested and edited it myself. Third-party tools: GitHub Pages, Render, Groq API, OpenStreetMap, Google Maps links, browser speech features.

## Run locally
```
cd backend
pip install -r requirements.txt
set GROQ_API_KEY=your_key
set LLM_MODEL=openai/gpt-oss-20b
uvicorn main:app --reload
```
Open `index.html` in a browser. Set `API_URL` at the top to your backend address.
